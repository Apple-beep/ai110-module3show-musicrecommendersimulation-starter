import csv
from dataclasses import asdict, dataclass
from typing import Dict, List, Tuple


GENRE_WEIGHT = 35.0
MOOD_WEIGHT = 25.0
ENERGY_WEIGHT = 25.0
ACOUSTIC_WEIGHT = 15.0


@dataclass
class Song:
    """Represent one song and its recommendation features."""

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


@dataclass
class UserProfile:
    """Represent a listener's current music preferences."""

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """Rank Song objects for a UserProfile."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs sorted by recommendation score."""
        scored_songs = [
            (song, score_song(asdict(user), asdict(song))[0])
            for song in self.songs
        ]

        ranked_songs = sorted(
            scored_songs,
            key=lambda item: (-item[1], item[0].title.lower()),
        )

        return [song for song, _ in ranked_songs[: max(0, k)]]

    def explain_recommendation(
        self,
        user: UserProfile,
        song: Song,
    ) -> str:
        """Explain how a song earned its recommendation score."""
        _, reasons = score_song(asdict(user), asdict(song))
        return "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
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
    }

    songs: List[Dict] = []

    with open(
        csv_path,
        newline="",
        encoding="utf-8-sig",
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        if reader.fieldnames is None:
            raise ValueError("The CSV file does not have a header row.")

        missing_columns = required_columns - set(reader.fieldnames)

        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"Missing required CSV columns: {missing}")

        for row_number, row in enumerate(reader, start=2):
            try:
                song = {
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
                }
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"Invalid value in {csv_path} "
                    f"on row {row_number}: {error}"
                ) from error

            songs.append(song)

    return songs


def score_song(
    user_prefs: Dict,
    song: Dict,
) -> Tuple[float, List[str]]:
    """Score one song and return its numeric score and reasons."""
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

    target_energy = float(
        user_prefs.get(
            "target_energy",
            user_prefs.get("energy", 0.5),
        )
    )

    likes_acoustic = bool(
        user_prefs.get("likes_acoustic", False)
    )

    if not 0.0 <= target_energy <= 1.0:
        raise ValueError(
            "target_energy must be between 0.0 and 1.0."
        )

    song_genre = str(song["genre"]).strip().lower()
    song_mood = str(song["mood"]).strip().lower()
    song_energy = float(song["energy"])
    song_acousticness = float(song["acousticness"])

    score = 0.0
    reasons: List[str] = []

    if song_genre == favorite_genre:
        score += GENRE_WEIGHT
        reasons.append(
            f"genre match: {song_genre} "
            f"(+{GENRE_WEIGHT:.2f})"
        )
    else:
        reasons.append(
            f"genre mismatch: {song_genre} (+0.00)"
        )

    if song_mood == favorite_mood:
        score += MOOD_WEIGHT
        reasons.append(
            f"mood match: {song_mood} "
            f"(+{MOOD_WEIGHT:.2f})"
        )
    else:
        reasons.append(
            f"mood mismatch: {song_mood} (+0.00)"
        )

    energy_difference = abs(
        song_energy - target_energy
    )

    energy_similarity = max(
        0.0,
        1.0 - energy_difference,
    )

    energy_points = (
        energy_similarity * ENERGY_WEIGHT
    )

    score += energy_points

    reasons.append(
        f"energy similarity {energy_similarity:.2f} "
        f"(+{energy_points:.2f})"
    )

    if likes_acoustic:
        acoustic_points = (
            song_acousticness * ACOUSTIC_WEIGHT
        )
        acoustic_label = "acoustic preference"
    else:
        acoustic_points = (
            (1.0 - song_acousticness)
            * ACOUSTIC_WEIGHT
        )
        acoustic_label = "non-acoustic preference"

    score += acoustic_points

    reasons.append(
        f"{acoustic_label} "
        f"(+{acoustic_points:.2f})"
    )

    return round(score, 2), reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
) -> List[Tuple[Dict, float, str]]:
    """Rank every song and return the top k explained results."""
    scored_songs: List[
        Tuple[Dict, float, str]
    ] = []

    for song in songs:
        score, reasons = score_song(
            user_prefs,
            song,
        )

        explanation = "; ".join(reasons)

        scored_songs.append(
            (song, score, explanation)
        )

    ranked_songs = sorted(
        scored_songs,
        key=lambda result: (
            -result[1],
            result[0]["title"].lower(),
        ),
    )

    return ranked_songs[: max(0, k)]