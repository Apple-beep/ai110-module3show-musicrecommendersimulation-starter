"""Run the command-line music recommender simulation."""

from .recommender import (
    load_songs,
    recommend_songs,
)


def main() -> None:
    """Load the catalog and display ranked recommendations."""
    songs = load_songs("data/songs.csv")

    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(
        user_prefs,
        songs,
        k=5,
    )

    print(f"\nLoaded songs: {len(songs)}")

    print("\nUser profile")
    print("------------")
    print(
        f"Favorite genre: "
        f"{user_prefs['favorite_genre']}"
    )
    print(
        f"Favorite mood: "
        f"{user_prefs['favorite_mood']}"
    )
    print(
        f"Target energy: "
        f"{user_prefs['target_energy']:.2f}"
    )
    print(
        f"Likes acoustic: "
        f"{user_prefs['likes_acoustic']}"
    )

    print("\nTop recommendations")
    print("===================")

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


if __name__ == "__main__":
    main()