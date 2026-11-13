# 🎵 Music Recommender Simulation

## Project Summary

This project is a small **content-based music recommender** I built for CodePath AI110 (Project 3). It reads a catalog of 18 songs from a CSV file, compares each song to a user's taste profile (favorite genre, favorite mood, and target energy), gives every song a score along with a short list of reasons, and prints the best matches.

The goal was not to build something that rivals Spotify. It was to see, in a system small enough to read in one sitting, how data turns into a ranking, and where bias can sneak in. I represented songs and a user's taste as data, wrote a scoring rule, ran it on five different user profiles, ran one experiment that changed the weights, and wrote down what the system gets right and wrong.

**What it does in one paragraph:** for each song, it adds up points: 2.0 for matching the user's favorite genre, 1.0 for matching their favorite mood, and up to 1.0 for having an energy level close to their target. The songs are then sorted by score. Every result comes with the reasons for its score (for example `genre match (+2.0)`), so you can always see why a song was picked.

**What I found:** the system works well when the user's genre and mood are both in the catalog, but genre is weighted so heavily that it can push a poor fit to the top. For a user who asked for a sad classical song with high energy, it returned a slow classical piece first. Details are in [Profiles I Tested](#profiles-i-tested), [Experiments You Tried](#experiments-you-tried), and the [model card](model_card.md).

## Features

- Loads songs from `data/songs.csv` and converts the numeric columns, with no errors on all 18 rows
- Scores any song against a user profile with `score_song`, which returns both a number and a list of reasons
- Ranks the whole catalog and returns the top `k` songs with `recommend_songs`
- Explains every recommendation in plain text that matches the real math
- Includes an object-oriented `Recommender` class (with `Song` and `UserProfile`) that uses the same scoring, so the tests and the command-line runner agree
- Supports changing the weights, which is how the energy-versus-genre experiment was run

## Project Structure

```plaintext
├── data/songs.csv          # 18 songs: the starter's 10 plus 8 I added
├── src/recommender.py      # load_songs, score_song, recommend_songs, Recommender class
├── src/main.py             # runs five profiles and the weight experiment
├── tests/test_recommender.py   # 4 pytest tests
├── model_card.md           # model card: data, algorithm, bias, evaluation, reflection
└── README.md               # this file
```

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
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app from the repo root (not from inside `src/`):

   ```bash
   python -m src.main
   ```

   This loads the songs, prints the top 5 recommendations for each of five profiles, and then reruns two of them with the experiment weights.

### Running Tests

```bash
python -m pytest -v
```

The 4 tests cover:

- `test_recommend_returns_songs_sorted_by_score`: a pop/happy/high-energy user gets the pop/happy song ahead of the lofi one
- `test_explain_recommendation_returns_non_empty_string`: every recommendation comes with a non-empty explanation
- `test_load_songs_reads_18_songs_with_numbers`: the CSV loads all 18 songs and converts `id` to an int and `energy` to a float
- `test_score_song_gives_full_points_for_perfect_match`: a song that matches on genre, mood, and energy scores exactly 4.0, with reasons that say `genre match (+2.0)` and `mood match (+1.0)`

Real output from my last run:

```
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
collected 4 items

tests/test_recommender.py::test_recommend_returns_songs_sorted_by_score PASSED [ 25%]
tests/test_recommender.py::test_explain_recommendation_returns_non_empty_string PASSED [ 50%]
tests/test_recommender.py::test_load_songs_reads_18_songs_with_numbers PASSED [ 75%]
tests/test_recommender.py::test_score_song_gives_full_points_for_perfect_match PASSED [100%]

============================== 4 passed in 0.02s ==============================
```

The tests only check the basics. They do not cover edge cases like an empty catalog or a genre that is not in the data.

---

## Sample Recommendation Output

Default profile (pop, happy, energy 0.8), copied from a real run of `python -m src.main`:

```
=== Default (Pop / Happy) ===
Profile: genre=pop, mood=happy, energy=0.8
1. Sunrise City (pop/happy) - Score: 3.98
   Because: genre match (+2.0); mood match (+1.0); energy 0.82 vs target 0.80 (+0.98)
2. Gym Hero (pop/intense) - Score: 2.87
   Because: genre match (+2.0); energy 0.93 vs target 0.80 (+0.87)
3. Rooftop Lights (indie pop/happy) - Score: 1.96
   Because: mood match (+1.0); energy 0.76 vs target 0.80 (+0.96)
4. Concrete Crown (hip hop/confident) - Score: 0.98
   Because: energy 0.78 vs target 0.80 (+0.98)
5. Night Drive Loop (synthwave/moody) - Score: 0.95
   Because: energy 0.75 vs target 0.80 (+0.95)
```

---

## Profiles I Tested

I ran four more profiles, including one conflicting edge case (classical + sad, but energy 0.9). This is the real output:

```
=== High-Energy Pop ===
Profile: genre=pop, mood=happy, energy=0.9
1. Sunrise City (pop/happy) - Score: 3.92
   Because: genre match (+2.0); mood match (+1.0); energy 0.82 vs target 0.90 (+0.92)
2. Gym Hero (pop/intense) - Score: 2.97
   Because: genre match (+2.0); energy 0.93 vs target 0.90 (+0.97)
3. Rooftop Lights (indie pop/happy) - Score: 1.86
   Because: mood match (+1.0); energy 0.76 vs target 0.90 (+0.86)
4. Storm Runner (rock/intense) - Score: 0.99
   Because: energy 0.91 vs target 0.90 (+0.99)
5. Neon Pulse (edm/energetic) - Score: 0.96
   Because: energy 0.94 vs target 0.90 (+0.96)

=== Chill Lofi ===
Profile: genre=lofi, mood=chill, energy=0.35
1. Library Rain (lofi/chill) - Score: 4.00
   Because: genre match (+2.0); mood match (+1.0); energy 0.35 vs target 0.35 (+1.00)
2. Midnight Coding (lofi/chill) - Score: 3.93
   Because: genre match (+2.0); mood match (+1.0); energy 0.42 vs target 0.35 (+0.93)
3. Focus Flow (lofi/focused) - Score: 2.95
   Because: genre match (+2.0); energy 0.40 vs target 0.35 (+0.95)
4. Spacewalk Thoughts (ambient/chill) - Score: 1.93
   Because: mood match (+1.0); energy 0.28 vs target 0.35 (+0.93)
5. Coffee Shop Stories (jazz/relaxed) - Score: 0.98
   Because: energy 0.37 vs target 0.35 (+0.98)

=== Deep Intense Rock ===
Profile: genre=rock, mood=intense, energy=0.92
1. Storm Runner (rock/intense) - Score: 3.99
   Because: genre match (+2.0); mood match (+1.0); energy 0.91 vs target 0.92 (+0.99)
2. Gym Hero (pop/intense) - Score: 1.99
   Because: mood match (+1.0); energy 0.93 vs target 0.92 (+0.99)
3. Neon Pulse (edm/energetic) - Score: 0.98
   Because: energy 0.94 vs target 0.92 (+0.98)
4. Iron Tide (metal/angry) - Score: 0.96
   Because: energy 0.96 vs target 0.92 (+0.96)
5. Sunrise City (pop/happy) - Score: 0.90
   Because: energy 0.82 vs target 0.92 (+0.90)

=== Conflicting (Sad but high energy) ===
Profile: genre=classical, mood=sad, energy=0.9
1. Nocturne in Rain (classical/sad) - Score: 3.30
   Because: genre match (+2.0); mood match (+1.0); energy 0.20 vs target 0.90 (+0.30)
2. Paper Boats (folk/sad) - Score: 1.40
   Because: mood match (+1.0); energy 0.30 vs target 0.90 (+0.40)
3. Storm Runner (rock/intense) - Score: 0.99
   Because: energy 0.91 vs target 0.90 (+0.99)
4. Gym Hero (pop/intense) - Score: 0.97
   Because: energy 0.93 vs target 0.90 (+0.97)
5. Neon Pulse (edm/energetic) - Score: 0.96
   Because: energy 0.94 vs target 0.90 (+0.96)

##### EXPERIMENT: genre weight 1.0 (halved), energy weight 2.0 (doubled) #####
```

### Comparing each pair of profiles

- **High-Energy Pop vs. Chill Lofi:** The top result flips from Sunrise City (energy 0.82) to Library Rain (energy 0.35), and the whole list moves from loud songs to quiet lofi and ambient. That makes sense: the two profiles differ on genre, mood, *and* target energy, so nothing is shared. Chill Lofi also gets a near-perfect 4.00 because the catalog has three lofi songs to pick from.
- **High-Energy Pop vs. Deep Intense Rock:** Both want high energy, so Gym Hero, Neon Pulse and Storm Runner show up in both lists. What changes is the top spot: Sunrise City for pop/happy, Storm Runner for rock/intense. After the first match, the rest of each list is just "whatever is closest in energy," which is why the lists overlap. It is correct but shows energy doing most of the work once genre and mood run out.
- **High-Energy Pop vs. Conflicting:** The same target energy (0.9) gives very different lists. The conflicting profile puts a slow classical song first (Nocturne in Rain, energy 0.20) even though it is 0.70 away from the target. Genre (+2.0) and mood (+1.0) together outweigh a terrible energy score (+0.30), so the user who asked for high energy gets a quiet song at number one.
- **Chill Lofi vs. Deep Intense Rock:** These are opposites and the lists do not share a single song. What they do have in common is that each gets a near-perfect top result (Library Rain 4.00, Storm Runner 3.99), but the lofi profile has two songs that match both genre and mood (Library Rain and Midnight Coding, 4.00 and 3.93), while rock has only one, so its second spot drops to 1.99.
- **Chill Lofi vs. Conflicting:** Chill Lofi gets a confident top 3 of songs that match on genre, while the conflicting profile only has one song that matches genre and the rest of its list is filled by energy alone (Storm Runner, Gym Hero, Neon Pulse), which have nothing to do with "sad" or "classical." That makes sense: a rare genre with one song in the catalog gives the scorer almost nothing to work with.
- **Deep Intense Rock vs. Conflicting:** Both have one song that matches genre, but Rock's pick (Storm Runner, energy 0.91) also fits the energy, while Conflicting's pick (Nocturne in Rain, 0.20) does not. Rock's top score is 3.99 and Conflicting's is 3.30, showing that the same "genre + mood match" can look equally confident while meaning very different things for energy.

---

## Experiments You Tried

**Experiment: double the energy weight, halve the genre weight.** Genre went from +2.0 to +1.0 and the energy term from 1x to 2x (so up to +2.0). Real output:

```
=== High-Energy Pop [experiment] ===
Profile: genre=pop, mood=happy, energy=0.9
1. Sunrise City (pop/happy) - Score: 3.84
   Because: genre match (+1.0); mood match (+1.0); energy 0.82 vs target 0.90 (+1.84)
2. Gym Hero (pop/intense) - Score: 2.94
   Because: genre match (+1.0); energy 0.93 vs target 0.90 (+1.94)
3. Rooftop Lights (indie pop/happy) - Score: 2.72
   Because: mood match (+1.0); energy 0.76 vs target 0.90 (+1.72)
4. Storm Runner (rock/intense) - Score: 1.98
   Because: energy 0.91 vs target 0.90 (+1.98)
5. Neon Pulse (edm/energetic) - Score: 1.92
   Because: energy 0.94 vs target 0.90 (+1.92)

=== Conflicting (Sad but high energy) [experiment] ===
Profile: genre=classical, mood=sad, energy=0.9
1. Nocturne in Rain (classical/sad) - Score: 2.60
   Because: genre match (+1.0); mood match (+1.0); energy 0.20 vs target 0.90 (+0.60)
2. Storm Runner (rock/intense) - Score: 1.98
   Because: energy 0.91 vs target 0.90 (+1.98)
3. Gym Hero (pop/intense) - Score: 1.94
   Because: energy 0.93 vs target 0.90 (+1.94)
4. Neon Pulse (edm/energetic) - Score: 1.92
   Because: energy 0.94 vs target 0.90 (+1.92)
5. Iron Tide (metal/angry) - Score: 1.88
   Because: energy 0.96 vs target 0.90 (+1.88)
```

What changed:

- **High-Energy Pop:** The top two stay the same (Sunrise City, Gym Hero), but Rooftop Lights (indie pop, happy) went from a score of 1.86 up to 2.72, which is now close to Gym Hero at 2.94. Storm Runner and Neon Pulse (no genre or mood match) went from about 0.96 to about 1.9, so the lower half of the list is now more about energy than about taste.
- **Conflicting:** Nocturne in Rain is still number one (2.60), but its lead over number two shrank from 1.90 points (3.30 vs 1.40) to 0.62 points (2.60 vs 1.98). The number two song changed from Paper Boats (sad, but low energy) to Storm Runner (high energy, no sad or classical at all). So with energy doubled, the system started trading the user's stated mood for their energy target.

This was **not** more accurate, just a different bias: energy now dominates, and a song with no genre or mood match can beat a song that matches the mood. I would keep the original weights because genre and mood are what a user actually states, and energy is a number most people could not give precisely.

---

## Limitations and Risks

The biggest weakness I found is that **genre is worth so much that it overrides everything else**. In the Conflicting profile the system put a quiet classical song at number one for someone who asked for energy 0.9, because genre (+2.0) and mood (+1.0) together are worth far more than the energy score. A related problem is exact matching: "indie pop" earns no genre credit for a "pop" fan, so Rooftop Lights (a happy, high-energy indie pop song) came in third for the pop profile, behind Gym Hero, a pop song with the wrong mood. The catalog is also tiny, with most genres having a single song, so for many users the top result is just "the one song in my genre." It also ignores tempo, valence, danceability, acousticness and `likes_acoustic`, so a user's preference for acoustic music has no effect at all.

---

## Reflection

See [**Model Card**](model_card.md) for the full write-up.

### What I learned

A recommender is just a scoring rule plus a sort, and the weights are really opinions. Changing two weights (genre +2.0 to +1.0, energy doubled) changed which songs came out in the top five, so the "taste" the system shows is partly my design choice and not only the data. Bias can show up in simple places: a rare genre with one song, exact-text matching, or a weight that is too big. A real app with millions of songs would hide these behind much more complicated math, but the same kinds of problems would still be there.

### How I used AI

Claude wrote the scoring and ranking code, drafted the 8 new songs, and helped write the docs, working from decisions I approved up front: the weights (genre 2.0, mood 1.0, energy up to 1.0), the five profiles, and the experiment. I checked its work by running the program and reading the real output, and every number and example in this README comes from an actual run. One real catch: the starter's `main.py` imported `from recommender import ...`, which fails when you run `python -m src.main`, so it was changed to `from src.recommender import ...` and confirmed by running it. I accepted all of the AI's default suggestions, so I do not have a rejected suggestion to report for this project.

### What I would try next

- Use `likes_acoustic` and the acousticness column so that setting actually does something
- Give partial genre credit for close genres (like "indie pop" for a "pop" fan) instead of exact matching only
- Add a diversity rule so the top 5 are not all one genre or artist
- Add more songs so that every genre has more than one, then re-run the profiles to see if the bias gets better or just moves
