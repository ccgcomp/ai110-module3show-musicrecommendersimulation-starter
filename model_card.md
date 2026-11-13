# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**, a small content-based music recommender.

---

## 2. Intended Use  

It suggests songs from a small catalog based on a user's favorite genre, favorite mood, and target energy level. It assumes the user can state those three things up front, and it does not learn from listening history. This is for classroom exploration only. It is not meant for real users or for any decision about real people.

**Not intended for:** a real music app, ranking real artists, or any setting where being wrong has consequences. The catalog is invented and far too small.

---

## 3. How the Model Works  

Every song gets a score against the user's profile, and the songs with the highest scores are recommended. A song earns **2 points** if its genre matches the user's favorite genre, **1 point** if its mood matches, and up to **1 point** for energy, where the closer the song's energy is to the user's target, the more points it gets (an exact match earns the full point, a song at the other end of the scale earns about zero). The best possible score is 4. Each recommendation comes with a short list of the reasons that added points, like "genre match (+2.0)".

The starter had empty functions, so everything is new: loading the songs from the CSV, scoring a song, ranking the catalog, and printing the reasons. Only genre, mood, and energy are used. The songs also have tempo, valence, danceability, and acousticness, but those are not scored.

---

## 4. Data  

The catalog has **18 songs** in `data/songs.csv`. The starter had 10, and I added 8 (hip hop, country, r&b, metal, classical, edm, folk, and reggae songs) so that more genres and moods are represented. The new songs were drafted by Claude and approved by me. They are invented, not real songs.

- **Genres:** 15 different genres. Lofi has 3 songs and pop has 2, and the other 13 genres have exactly one song each.
- **Moods:** 12 different moods, like happy, chill, intense, sad, angry, and nostalgic. Chill has 3 songs, and happy, intense, relaxed, and sad have 2 each.
- **Missing:** no lyrics, no language or region, no artist popularity, no listening history, and nothing about how a user's taste changes with time of day or activity.

---

## 5. Strengths  

- It works well when the user's genre and mood both appear in the catalog. Chill Lofi got Library Rain (4.00) and Midnight Coding (3.93) at the top, and Deep Intense Rock got Storm Runner (3.99), which matched my intuition.
- The reasons shown with every recommendation match the real math, so I can see exactly why a song ranked where it did.
- Energy closeness gives sensible results when genre and mood run out: for the pop profile, the lower half of the list is just the songs closest in energy.

---

## 6. Limitations and Bias 

- **Genre is worth too much.** In the conflicting profile (classical, sad, but target energy 0.9), the top song was Nocturne in Rain, a slow classical piece with energy 0.20. Genre (+2.0) and mood (+1.0) together are worth so much that they beat a terrible energy score (+0.30), so a user who asked for high energy got a quiet song at number one.
- **Exact text matching.** "indie pop" earns no genre credit for a "pop" fan, so Rooftop Lights (happy, energy 0.76) ranked third for the pop profile, behind Gym Hero, a pop song with the wrong mood.
- **Tiny catalog.** 13 of the 15 genres have a single song, so for many users the #1 result is just the only song in their genre, and a genre that is not in the catalog never earns the +2.0.
- **Unused features.** `likes_acoustic` is in the profile but has no effect, and tempo, valence, and danceability are ignored.
- **Who it favors:** users whose favorite genre is lofi or pop, because those have the most songs to choose from.

---

## 7. Evaluation  

I ran five profiles through the recommender: Default (pop, happy, 0.8), High-Energy Pop (0.9), Chill Lofi (0.35), Deep Intense Rock (0.92), and a conflicting edge case (classical, sad, 0.9). I looked at whether the top result matched what I would pick by hand and whether the "Because" reasons matched the score. The full output and a comparison of every pair of profiles are in the README.

I also ran an experiment that doubled the energy weight and halved the genre weight. For the conflicting profile, Nocturne in Rain stayed number one, but its lead over number two shrank from 1.90 points to 0.62, and number two changed from Paper Boats (sad) to Storm Runner (intense rock, no sad at all). So the system started trading the user's stated mood for their energy number.

I also wrote 4 pytest tests (the 2 starter ones plus a CSV loading test and a perfect-match scoring test). All 4 pass.

**What surprised me:** for the plain pop/happy profile, Gym Hero (pop, but intense) came second ahead of Rooftop Lights (indie pop, happy). A person would probably say Rooftop Lights fits "pop, happy" better, but the genre points are bigger than the mood points.

---

## 8. Future Work  

- Use more than exact genre matching, for example treating "indie pop" as close to "pop".
- Use the features that are loaded but ignored: `likes_acoustic` with acousticness, and valence for mood.
- Add a diversity rule so the top 5 are not all the same genre or artist.
- Add many more songs, with more than one song for each genre.
- Handle users with mixed tastes, like two favorite genres.

---

## 9. Personal Reflection  

- **What I learned:** a recommender is a scoring rule plus a sort, and the weights are design choices. Changing two weights changed which songs came out in the top five, so the "taste" the system shows comes partly from my choices, not just the data.
- **Where AI helped and where I double-checked:** Claude wrote the scoring code and the draft songs, and I approved all of its default choices (weights, songs, profiles, experiment). The starter `main.py` imported `from recommender import ...`, which fails with `python -m src.main`, so that was fixed and checked by running the program. The README comparisons and the numbers in this card were checked against the real output of the run.
- **Something unexpected:** the conflicting profile still returned a quiet classical song as number one for a user who asked for high energy, because genre and mood points added up to more than the energy score could make up.
- **How this changes how I see music apps:** a recommendation that looks smart can be a few weights added together, and the weights can quietly decide who gets good results.
- **What I would try next:** use acousticness and valence in the score, and test whether a diversity rule makes the top five feel more varied.
