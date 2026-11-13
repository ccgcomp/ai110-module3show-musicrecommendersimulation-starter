# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version is a small content-based music recommender. It reads 18 songs from a CSV, compares each one to a user's taste profile (favorite genre, favorite mood, target energy), gives every song a score with a short list of reasons, and prints the top matches.

---

## How The System Works

### How real recommenders work

Apps like Spotify and YouTube mix two main ideas. **Collaborative filtering** looks at what other people did: if people who play the same songs as you also play song X, it recommends X to you, even without knowing anything about the song itself. **Content-based filtering** looks at the song's own features (genre, mood, tempo, energy, how acoustic it sounds) and finds songs close to what you already like. Real systems combine both, and also use history like skips, replays, and playlists. My project is **content-based only**, since I have no listening history from other users.

### Input data vs. user preferences vs. ranking

- **Input data (the catalog):** `data/songs.csv`, 18 songs. Each `Song` has: `id`, `title`, `artist`, `genre`, `mood`, `energy` (0 to 1), `tempo_bpm`, `valence` (how positive it sounds), `danceability`, and `acousticness`.
- **User preferences (the taste profile):** a `UserProfile` / preference dictionary with `favorite_genre`, `favorite_mood`, `target_energy` (0 to 1), and `likes_acoustic`. This is what the user tells the system. It is not learned from history.
- **Ranking:** every song gets a numeric score against the profile, then the songs are sorted from highest to lowest score and the top `k` are returned with the reasons for each score.

Only genre, mood, and energy are used in scoring right now. The other attributes are loaded but not used.

### Algorithm Recipe

For each song, the score is the sum of:

1. **+2.0** if the song's genre equals the user's favorite genre.
2. **+1.0** if the song's mood equals the user's favorite mood.
3. **Energy closeness:** `1.0 - |song energy - target energy|`, which is between 0 and +1.0. A song that matches the target exactly gets the full +1.0, and a song on the opposite end of the scale gets about 0.

The maximum possible score is **4.0**. Each rule that fires adds a reason like `genre match (+2.0)`. Songs are sorted by score, highest first, and the top `k` are returned.

### Expected bias

Genre is worth the most points, so the system will favor songs that match the user's genre even when a song in another genre is a much better fit on mood and energy. Because the catalog is tiny (most genres have exactly one song), a genre match will often be the only song of that genre, and a user whose favorite genre is missing from the catalog never gets the +2.0 for any song. Exact string matching also means "indie pop" gets no credit for a "pop" preference.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



