"""
Command line runner for the Music Recommender Simulation.

Run from the repo root with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs

PROFILES = {
    "Default (Pop / Happy)": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92},
    "Conflicting (Sad but high energy)": {"genre": "classical", "mood": "sad", "energy": 0.9},
}

# Experiment: double the energy weight, halve the genre weight.
EXPERIMENT_WEIGHTS = {"genre": 1.0, "mood": 1.0, "energy": 2.0}


def show(title: str, user_prefs: dict, songs: list, weights=None, k: int = 5) -> None:
    """Print the top k recommendations for one profile."""
    print(f"=== {title} ===")
    print(f"Profile: genre={user_prefs['genre']}, mood={user_prefs['mood']}, energy={user_prefs['energy']}")
    for rank, (song, score, explanation) in enumerate(recommend_songs(user_prefs, songs, k, weights), 1):
        print(f"{rank}. {song['title']} ({song['genre']}/{song['mood']}) - Score: {score:.2f}")
        print(f"   Because: {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs.\n")

    for title, prefs in PROFILES.items():
        show(title, prefs, songs)

    print("##### EXPERIMENT: genre weight 1.0 (halved), energy weight 2.0 (doubled) #####\n")
    for title in ("High-Energy Pop", "Conflicting (Sad but high energy)"):
        show(title + " [experiment]", PROFILES[title], songs, EXPERIMENT_WEIGHTS)


if __name__ == "__main__":
    main()
