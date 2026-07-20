"""Run VibeRank with selectable strategies and transparent tables."""

import argparse
from typing import Any, Dict, List

from tabulate import tabulate

from .recommender import STRATEGIES, load_songs, recommend_songs


USER_PROFILES: Dict[str, Dict[str, Any]] = {
    "high-energy-pop": {
        "label": "High-Energy Pop",
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "likes_acoustic": False,
        "target_popularity": 85.0,
        "preferred_decade": 2020,
        "target_instrumentalness": 0.05,
        "target_speechiness": 0.08,
        "target_duration_sec": 215.0,
    },
    "chill-lofi": {
        "label": "Chill Lofi",
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
        "target_popularity": 60.0,
        "preferred_decade": 2020,
        "target_instrumentalness": 0.80,
        "target_speechiness": 0.04,
        "target_duration_sec": 185.0,
    },
    "deep-intense-rock": {
        "label": "Deep Intense Rock",
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.92,
        "likes_acoustic": False,
        "target_popularity": 78.0,
        "preferred_decade": 2010,
        "target_instrumentalness": 0.08,
        "target_speechiness": 0.07,
        "target_duration_sec": 240.0,
    },
    "conflicting-classical-workout": {
        "label": "Conflicting Classical Workout",
        "favorite_genre": "classical",
        "favorite_mood": "aggressive",
        "target_energy": 0.95,
        "likes_acoustic": True,
        "target_popularity": 50.0,
        "preferred_decade": 2020,
        "target_instrumentalness": 0.90,
        "target_speechiness": 0.02,
        "target_duration_sec": 250.0,
    },
}


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(
        description=(
            "Run the VibeRank music recommender with selectable "
            "ranking strategies."
        )
    )
    parser.add_argument(
        "--mode",
        choices=sorted(STRATEGIES),
        default="balanced",
        help="Choose how song features are weighted.",
    )
    parser.add_argument(
        "--profile",
        choices=["all", *USER_PROFILES.keys()],
        default="all",
        help="Run one evaluation profile or all profiles.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of recommendations to display.",
    )
    parser.add_argument(
        "--no-diversity",
        action="store_true",
        help="Disable artist and genre repetition penalties.",
    )
    return parser.parse_args()


def _profile_for_scoring(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Remove display-only fields from a profile."""
    return {
        key: value
        for key, value in profile.items()
        if key != "label"
    }


def display_recommendations(
    profile: Dict[str, Any],
    songs: List[Dict[str, Any]],
    mode: str,
    k: int,
    diversify: bool,
) -> None:
    """Display one profile's recommendations in a formatted table."""
    user_prefs = _profile_for_scoring(profile)
    recommendations = recommend_songs(
        user_prefs,
        songs,
        k=k,
        mode=mode,
        diversify=diversify,
    )

    print("\n" + "=" * 100)
    print(f"Profile: {profile['label']}")
    print(f"Ranking mode: {mode}")
    print(f"Diversity reranking: {'on' if diversify else 'off'}")
    print("=" * 100)
    print(
        "Preferences: "
        f"genre={user_prefs['favorite_genre']}, "
        f"mood={user_prefs['favorite_mood']}, "
        f"energy={user_prefs['target_energy']:.2f}, "
        f"acoustic={user_prefs['likes_acoustic']}, "
        f"popularity={user_prefs['target_popularity']:.0f}, "
        f"decade={user_prefs['preferred_decade']}"
    )

    rows = []
    for rank, (song, score, explanation) in enumerate(
        recommendations,
        start=1,
    ):
        rows.append(
            [
                rank,
                song["title"],
                song["artist"],
                song["genre"],
                f"{score:.2f}",
                explanation,
            ]
        )

    print(
        tabulate(
            rows,
            headers=[
                "Rank",
                "Song",
                "Artist",
                "Genre",
                "Score",
                "Reasons",
            ],
            tablefmt="grid",
            maxcolwidths=[5, 20, 18, 13, 8, 70],
        )
    )


def main() -> None:
    """Load the catalog and run the selected evaluation profiles."""
    args = parse_args()

    if args.top_k < 1:
        raise SystemExit("--top-k must be at least 1.")

    songs = load_songs("data/songs.csv")
    print(f"\nLoaded songs: {len(songs)}")

    if args.profile == "all":
        selected_profiles = list(USER_PROFILES.values())
    else:
        selected_profiles = [USER_PROFILES[args.profile]]

    for profile in selected_profiles:
        display_recommendations(
            profile=profile,
            songs=songs,
            mode=args.mode,
            k=args.top_k,
            diversify=not args.no_diversity,
        )


if __name__ == "__main__":
    main()