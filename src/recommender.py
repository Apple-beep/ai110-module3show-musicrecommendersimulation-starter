"""Core scoring, ranking, and diversity logic for VibeRank."""

import csv
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Mapping, Tuple


SongDict = Dict[str, Any]
Recommendation = Tuple[SongDict, float, str]

ARTIST_REPEAT_PENALTY = 10.0
GENRE_REPEAT_PENALTY = 3.0


@dataclass
class Song:
    """Represent one song and all recommendation features."""

    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: float = 50.0
    release_decade: int = 2020
    instrumentalness: float = 0.0
    speechiness: float = 0.0
    duration_sec: float = 210.0


@dataclass
class UserProfile:
    """Represent a listener's current music preferences."""

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_popularity: float = 70.0
    preferred_decade: int = 2020
    target_instrumentalness: float = 0.20
    target_speechiness: float = 0.10
    target_duration_sec: float = 220.0


class RankingStrategy(ABC):
    """Define feature weights for one ranking mode."""

    name: str

    @abstractmethod
    def get_weights(self) -> Dict[str, float]:
        """Return feature weights that total 100 points."""


class BalancedStrategy(RankingStrategy):
    """Balance categorical, audio, and contextual song features."""

    name = "balanced"

    def get_weights(self) -> Dict[str, float]:
        """Return balanced feature weights."""
        return {
            "genre": 20.0,
            "mood": 15.0,
            "energy": 15.0,
            "acousticness": 10.0,
            "popularity": 10.0,
            "release_decade": 8.0,
            "instrumentalness": 8.0,
            "speechiness": 7.0,
            "duration": 7.0,
        }


class GenreFirstStrategy(RankingStrategy):
    """Prioritize an exact genre match."""

    name = "genre-first"

    def get_weights(self) -> Dict[str, float]:
        """Return genre-first feature weights."""
        return {
            "genre": 35.0,
            "mood": 10.0,
            "energy": 10.0,
            "acousticness": 8.0,
            "popularity": 8.0,
            "release_decade": 8.0,
            "instrumentalness": 7.0,
            "speechiness": 7.0,
            "duration": 7.0,
        }


class MoodFirstStrategy(RankingStrategy):
    """Prioritize an exact mood match."""

    name = "mood-first"

    def get_weights(self) -> Dict[str, float]:
        """Return mood-first feature weights."""
        return {
            "genre": 10.0,
            "mood": 35.0,
            "energy": 10.0,
            "acousticness": 8.0,
            "popularity": 8.0,
            "release_decade": 8.0,
            "instrumentalness": 7.0,
            "speechiness": 7.0,
            "duration": 7.0,
        }


class EnergyFirstStrategy(RankingStrategy):
    """Prioritize similarity to the target energy level."""

    name = "energy-first"

    def get_weights(self) -> Dict[str, float]:
        """Return energy-first feature weights."""
        return {
            "genre": 10.0,
            "mood": 10.0,
            "energy": 35.0,
            "acousticness": 10.0,
            "popularity": 8.0,
            "release_decade": 7.0,
            "instrumentalness": 7.0,
            "speechiness": 6.0,
            "duration": 7.0,
        }


STRATEGIES: Dict[str, RankingStrategy] = {
    strategy.name: strategy
    for strategy in (
        BalancedStrategy(),
        GenreFirstStrategy(),
        MoodFirstStrategy(),
        EnergyFirstStrategy(),
    )
}


class Recommender:
    """Rank Song objects for a UserProfile."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(
        self,
        user: UserProfile,
        k: int = 5,
        mode: str = "balanced",
        diversify: bool = False,
    ) -> List[Song]:
        """Return the top k Song objects for a user."""
        song_dicts = [asdict(song) for song in self.songs]
        results = recommend_songs(
            asdict(user),
            song_dicts,
            k=k,
            mode=mode,
            diversify=diversify,
        )
        songs_by_id = {song.id: song for song in self.songs}
        return [songs_by_id[result[0]["id"]] for result in results]

    def explain_recommendation(
        self,
        user: UserProfile,
        song: Song,
        mode: str = "balanced",
    ) -> str:
        """Explain how a Song object earned its score."""
        _, reasons = score_song(asdict(user), asdict(song), mode=mode)
        return "; ".join(reasons)


def get_strategy(mode: str) -> RankingStrategy:
    """Return the requested ranking strategy or raise a clear error."""
    normalized_mode = mode.strip().lower()
    strategy = STRATEGIES.get(normalized_mode)

    if strategy is None:
        valid_modes = ", ".join(sorted(STRATEGIES))
        raise ValueError(
            f"Unknown ranking mode '{mode}'. Choose from: {valid_modes}."
        )

    weights = strategy.get_weights()
    if abs(sum(weights.values()) - 100.0) > 0.001:
        raise ValueError(
            f"Strategy '{normalized_mode}' weights must total 100."
        )

    return strategy


def _validate_unit_interval(value: float, field_name: str) -> None:
    """Validate a normalized feature value."""
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{field_name} must be between 0.0 and 1.0.")


def load_songs(csv_path: str) -> List[SongDict]:
    """Load songs from CSV and convert numerical fields."""
    required_columns = {
        "id",
        "title",
        "artist",
        "genre",
        "mood",
        "energy",
        "tempo_bpm",
        "valence",
        "danceability",
        "acousticness",
        "popularity",
        "release_decade",
        "instrumentalness",
        "speechiness",
        "duration_sec",
    }

    songs: List[SongDict] = []

    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)

        if reader.fieldnames is None:
            raise ValueError("The CSV file does not have a header row.")

        missing_columns = required_columns - set(reader.fieldnames)
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"Missing required CSV columns: {missing}")

        for row_number, row in enumerate(reader, start=2):
            try:
                song: SongDict = {
                    "id": int(row["id"]),
                    "title": row["title"].strip(),
                    "artist": row["artist"].strip(),
                    "genre": row["genre"].strip().lower(),
                    "mood": row["mood"].strip().lower(),
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                    "popularity": float(row["popularity"]),
                    "release_decade": int(row["release_decade"]),
                    "instrumentalness": float(row["instrumentalness"]),
                    "speechiness": float(row["speechiness"]),
                    "duration_sec": float(row["duration_sec"]),
                }
            except (KeyError, TypeError, ValueError) as error:
                raise ValueError(
                    f"Invalid value in {csv_path} on row {row_number}: {error}"
                ) from error

            if not song["title"] or not song["artist"]:
                raise ValueError(
                    f"Missing title or artist in {csv_path} on row {row_number}."
                )

            for normalized_field in (
                "energy",
                "valence",
                "danceability",
                "acousticness",
                "instrumentalness",
                "speechiness",
            ):
                _validate_unit_interval(
                    float(song[normalized_field]),
                    normalized_field,
                )

            if not 0.0 <= float(song["popularity"]) <= 100.0:
                raise ValueError(
                    f"popularity must be between 0 and 100 on row {row_number}."
                )
            if float(song["tempo_bpm"]) <= 0:
                raise ValueError(
                    f"tempo_bpm must be positive on row {row_number}."
                )
            if float(song["duration_sec"]) <= 0:
                raise ValueError(
                    f"duration_sec must be positive on row {row_number}."
                )

            songs.append(song)

    return songs


def _similarity(value: float, target: float, scale: float = 1.0) -> float:
    """Return normalized closeness between a value and a target."""
    if scale <= 0:
        raise ValueError("Similarity scale must be positive.")
    return max(0.0, 1.0 - abs(value - target) / scale)


def _numeric_preference(
    user_prefs: Mapping[str, Any],
    key: str,
    default: float,
) -> float:
    """Read a numeric user preference with a default value."""
    return float(user_prefs.get(key, default))


def score_song(
    user_prefs: Mapping[str, Any],
    song: Mapping[str, Any],
    mode: str = "balanced",
) -> Tuple[float, List[str]]:
    """Score one song and return its score and transparent reasons."""
    strategy = get_strategy(mode)
    weights = strategy.get_weights()

    favorite_genre = str(
        user_prefs.get(
            "favorite_genre",
            user_prefs.get("genre", ""),
        )
    ).strip().lower()
    favorite_mood = str(
        user_prefs.get(
            "favorite_mood",
            user_prefs.get("mood", ""),
        )
    ).strip().lower()

    target_energy = _numeric_preference(
        user_prefs,
        "target_energy",
        float(user_prefs.get("energy", 0.5)),
    )
    likes_acoustic = bool(user_prefs.get("likes_acoustic", False))
    target_popularity = _numeric_preference(
        user_prefs,
        "target_popularity",
        70.0,
    )
    preferred_decade = _numeric_preference(
        user_prefs,
        "preferred_decade",
        2020.0,
    )
    target_instrumentalness = _numeric_preference(
        user_prefs,
        "target_instrumentalness",
        0.20,
    )
    target_speechiness = _numeric_preference(
        user_prefs,
        "target_speechiness",
        0.10,
    )
    target_duration = _numeric_preference(
        user_prefs,
        "target_duration_sec",
        220.0,
    )

    _validate_unit_interval(target_energy, "target_energy")
    _validate_unit_interval(
        target_instrumentalness,
        "target_instrumentalness",
    )
    _validate_unit_interval(target_speechiness, "target_speechiness")
    if not 0.0 <= target_popularity <= 100.0:
        raise ValueError("target_popularity must be between 0 and 100.")
    if target_duration <= 0:
        raise ValueError("target_duration_sec must be positive.")

    song_genre = str(song["genre"]).strip().lower()
    song_mood = str(song["mood"]).strip().lower()
    song_energy = float(song["energy"])
    song_acousticness = float(song["acousticness"])
    song_popularity = float(song.get("popularity", 50.0))
    song_decade = float(song.get("release_decade", 2020))
    song_instrumentalness = float(song.get("instrumentalness", 0.0))
    song_speechiness = float(song.get("speechiness", 0.0))
    song_duration = float(song.get("duration_sec", 210.0))

    score = 0.0
    reasons: List[str] = [f"mode: {strategy.name}"]

    genre_points = weights["genre"] if song_genre == favorite_genre else 0.0
    score += genre_points
    genre_label = "match" if genre_points else "mismatch"
    reasons.append(
        f"genre {genre_label}: {song_genre} (+{genre_points:.2f})"
    )

    mood_points = weights["mood"] if song_mood == favorite_mood else 0.0
    score += mood_points
    mood_label = "match" if mood_points else "mismatch"
    reasons.append(
        f"mood {mood_label}: {song_mood} (+{mood_points:.2f})"
    )

    energy_similarity = _similarity(song_energy, target_energy)
    energy_points = energy_similarity * weights["energy"]
    score += energy_points
    reasons.append(
        f"energy similarity {energy_similarity:.2f} "
        f"(+{energy_points:.2f})"
    )

    if likes_acoustic:
        acoustic_similarity = song_acousticness
        acoustic_label = "acoustic preference"
    else:
        acoustic_similarity = 1.0 - song_acousticness
        acoustic_label = "non-acoustic preference"
    acoustic_points = acoustic_similarity * weights["acousticness"]
    score += acoustic_points
    reasons.append(
        f"{acoustic_label} (+{acoustic_points:.2f})"
    )

    popularity_similarity = _similarity(
        song_popularity,
        target_popularity,
        scale=100.0,
    )
    popularity_points = popularity_similarity * weights["popularity"]
    score += popularity_points
    reasons.append(
        f"popularity similarity {popularity_similarity:.2f} "
        f"(+{popularity_points:.2f})"
    )

    decade_similarity = _similarity(
        song_decade,
        preferred_decade,
        scale=50.0,
    )
    decade_points = decade_similarity * weights["release_decade"]
    score += decade_points
    reasons.append(
        f"decade similarity {decade_similarity:.2f} "
        f"(+{decade_points:.2f})"
    )

    instrumental_similarity = _similarity(
        song_instrumentalness,
        target_instrumentalness,
    )
    instrumental_points = (
        instrumental_similarity * weights["instrumentalness"]
    )
    score += instrumental_points
    reasons.append(
        f"instrumentalness similarity {instrumental_similarity:.2f} "
        f"(+{instrumental_points:.2f})"
    )

    speechiness_similarity = _similarity(
        song_speechiness,
        target_speechiness,
    )
    speechiness_points = speechiness_similarity * weights["speechiness"]
    score += speechiness_points
    reasons.append(
        f"speechiness similarity {speechiness_similarity:.2f} "
        f"(+{speechiness_points:.2f})"
    )

    duration_similarity = _similarity(
        song_duration,
        target_duration,
        scale=240.0,
    )
    duration_points = duration_similarity * weights["duration"]
    score += duration_points
    reasons.append(
        f"duration similarity {duration_similarity:.2f} "
        f"(+{duration_points:.2f})"
    )

    return round(score, 2), reasons


def diversify_rankings(
    ranked_songs: List[Recommendation],
    k: int,
) -> List[Recommendation]:
    """Rerank results to reduce repeated artists and genres."""
    remaining = list(ranked_songs)
    selected: List[Recommendation] = []
    artist_counts: Dict[str, int] = {}
    genre_counts: Dict[str, int] = {}

    while remaining and len(selected) < max(0, k):
        adjusted_candidates: List[Recommendation] = []

        for song, base_score, explanation in remaining:
            adjusted_score = base_score
            extra_reasons: List[str] = []

            artist = str(song["artist"])
            genre = str(song["genre"])
            artist_count = artist_counts.get(artist, 0)
            genre_count = genre_counts.get(genre, 0)

            if artist_count:
                artist_penalty = ARTIST_REPEAT_PENALTY * artist_count
                adjusted_score -= artist_penalty
                extra_reasons.append(
                    f"artist repetition penalty (-{artist_penalty:.2f})"
                )

            if genre_count:
                genre_penalty = GENRE_REPEAT_PENALTY * genre_count
                adjusted_score -= genre_penalty
                extra_reasons.append(
                    f"genre repetition penalty (-{genre_penalty:.2f})"
                )

            complete_explanation = explanation
            if extra_reasons:
                complete_explanation += "; " + "; ".join(extra_reasons)

            adjusted_candidates.append(
                (
                    song,
                    round(max(0.0, adjusted_score), 2),
                    complete_explanation,
                )
            )

        adjusted_candidates.sort(
            key=lambda result: (
                -result[1],
                str(result[0]["title"]).lower(),
            )
        )
        best = adjusted_candidates[0]
        selected.append(best)

        selected_song = best[0]
        selected_artist = str(selected_song["artist"])
        selected_genre = str(selected_song["genre"])
        artist_counts[selected_artist] = (
            artist_counts.get(selected_artist, 0) + 1
        )
        genre_counts[selected_genre] = (
            genre_counts.get(selected_genre, 0) + 1
        )

        remaining = [
            result
            for result in remaining
            if result[0]["id"] != selected_song["id"]
        ]

    return selected


def recommend_songs(
    user_prefs: Mapping[str, Any],
    songs: List[SongDict],
    k: int = 5,
    mode: str = "balanced",
    diversify: bool = True,
) -> List[Recommendation]:
    """Rank all songs and return the top k explained results."""
    scored_songs: List[Recommendation] = []

    for song in songs:
        score, reasons = score_song(
            user_prefs,
            song,
            mode=mode,
        )
        scored_songs.append(
            (song, score, "; ".join(reasons))
        )

    ranked_songs = sorted(
        scored_songs,
        key=lambda result: (
            -result[1],
            str(result[0]["title"]).lower(),
        ),
    )

    if diversify:
        return diversify_rankings(ranked_songs, k)

    return ranked_songs[: max(0, k)]