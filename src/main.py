"""Evaluate the music recommender using several user profiles."""

from typing import Dict, List

from .recommender import load_songs, recommend_songs


USER_PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.92,
        "likes_acoustic": False,
    },
    "Conflicting Classical Workout": {
        "favorite_genre": "classical",
        "favorite_mood": "aggressive",
        "target_energy": 0.95,
        "likes_acoustic": True,
    },
}


def display_recommendations(
    profile_name: str,
    user_prefs: Dict,
    songs: List[Dict],
) -> None:
    """Display the top five recommendations for one profile."""
    recommendations = recommend_songs(
        user_prefs,
        songs,
        k=5,
    )

    print("\n" + "=" * 70)
    print(f"Profile: {profile_name}")
    print("=" * 70)

    print(
        f"Genre: {user_prefs['favorite_genre']} | "
        f"Mood: {user_prefs['favorite_mood']} | "
        f"Energy: {user_prefs['target_energy']:.2f} | "
        f"Likes acoustic: {user_prefs['likes_acoustic']}"
    )

    for rank, result in enumerate(
        recommendations,
        start=1,
    ):
        song, score, explanation = result

        print(
            f"\n{rank}. {song['title']} "
            f"by {song['artist']}"
        )
        print(f"   Score: {score:.2f}/100.00")
        print(f"   Reasons: {explanation}")


def main() -> None:
    """Run the recommender for several evaluation profiles."""
    songs = load_songs("data/songs.csv")

    print(f"\nLoaded songs: {len(songs)}")

    for profile_name, user_prefs in USER_PROFILES.items():
        display_recommendations(
            profile_name,
            user_prefs,
            songs,
        )


if __name__ == "__main__":
    main()