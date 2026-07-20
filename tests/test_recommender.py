"""Tests for core and stretch-feature recommender behavior."""

from pathlib import Path

from src.recommender import (
    STRATEGIES,
    Recommender,
    Song,
    UserProfile,
    diversify_rankings,
    load_songs,
    recommend_songs,
    score_song,
)


DATA_PATH = Path("data/songs.csv")


def make_small_recommender() -> Recommender:
    """Create a small catalog for object-oriented compatibility tests."""
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
            popularity=80,
            release_decade=2020,
            instrumentalness=0.05,
            speechiness=0.08,
            duration_sec=210,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Other Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
            popularity=55,
            release_decade=2020,
            instrumentalness=0.8,
            speechiness=0.04,
            duration_sec=185,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score() -> None:
    """A matching pop song should outrank the lofi song."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
        target_popularity=80,
        preferred_decade=2020,
        target_instrumentalness=0.05,
        target_speechiness=0.08,
        target_duration_sec=210,
    )
    recommender = make_small_recommender()
    results = recommender.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string() -> None:
    """Object-oriented explanations should be readable text."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    recommender = make_small_recommender()
    explanation = recommender.explain_recommendation(
        user,
        recommender.songs[0],
    )

    assert isinstance(explanation, str)
    assert explanation.strip()
    assert "energy similarity" in explanation


def test_dataset_loads_twenty_songs_with_new_attributes() -> None:
    """The expanded CSV should load all original and stretch fields."""
    songs = load_songs(str(DATA_PATH))

    assert len(songs) == 20

    expected_new_fields = {
        "popularity",
        "release_decade",
        "instrumentalness",
        "speechiness",
        "duration_sec",
    }
    assert expected_new_fields.issubset(songs[0])

    assert isinstance(songs[0]["popularity"], float)
    assert isinstance(songs[0]["release_decade"], int)
    assert isinstance(songs[0]["instrumentalness"], float)
    assert isinstance(songs[0]["speechiness"], float)
    assert isinstance(songs[0]["duration_sec"], float)


def test_all_strategy_weights_total_one_hundred() -> None:
    """Every Strategy implementation should produce a 100-point score."""
    assert len(STRATEGIES) >= 2

    for strategy in STRATEGIES.values():
        assert sum(strategy.get_weights().values()) == 100.0


def test_ranking_modes_change_the_score() -> None:
    """Different strategies should produce different numeric results."""
    songs = load_songs(str(DATA_PATH))
    user = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
        "target_popularity": 85,
        "preferred_decade": 2020,
        "target_instrumentalness": 0.05,
        "target_speechiness": 0.08,
        "target_duration_sec": 215,
    }

    balanced_score, _ = score_song(
        user,
        songs[0],
        mode="balanced",
    )
    genre_score, _ = score_song(
        user,
        songs[0],
        mode="genre-first",
    )
    mood_score, _ = score_song(
        user,
        songs[0],
        mode="mood-first",
    )

    assert len({balanced_score, genre_score, mood_score}) > 1


def test_diversity_reranking_penalizes_repeated_artist_and_genre() -> None:
    """Repeated artists and genres should receive transparent penalties."""
    ranked = [
        (
            {
                "id": 1,
                "title": "First",
                "artist": "Same Artist",
                "genre": "pop",
            },
            90.0,
            "base score",
        ),
        (
            {
                "id": 2,
                "title": "Second",
                "artist": "Same Artist",
                "genre": "pop",
            },
            89.0,
            "base score",
        ),
        (
            {
                "id": 3,
                "title": "Different",
                "artist": "New Artist",
                "genre": "rock",
            },
            85.0,
            "base score",
        ),
    ]

    diversified = diversify_rankings(ranked, k=3)

    assert [result[0]["title"] for result in diversified] == [
        "First",
        "Different",
        "Second",
    ]
    assert "artist repetition penalty" in diversified[2][2]
    assert "genre repetition penalty" in diversified[2][2]
    assert diversified[2][1] < 89.0


def test_recommend_songs_returns_explained_top_five() -> None:
    """Functional recommendations should return scores and reasons."""
    songs = load_songs(str(DATA_PATH))
    user = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
        "target_popularity": 60,
        "preferred_decade": 2020,
        "target_instrumentalness": 0.8,
        "target_speechiness": 0.04,
        "target_duration_sec": 185,
    }

    results = recommend_songs(
        user,
        songs,
        k=5,
        mode="balanced",
        diversify=True,
    )

    assert len(results) == 5
    assert all(isinstance(score, float) for _, score, _ in results)
    assert all(explanation.strip() for _, _, explanation in results)
    assert all("mode: balanced" in explanation for _, _, explanation in results)