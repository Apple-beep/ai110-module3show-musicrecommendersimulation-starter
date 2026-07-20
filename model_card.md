# 🎧 Model Card: VibeRank 2.0

## 1. Model Name

**VibeRank 2.0**

VibeRank is a content-based music recommendation simulation with selectable ranking strategies, diversity reranking, and transparent explanations.

---

## 2. Goal and Intended Use

### Goal

VibeRank suggests songs that may match a listener's current preferences.

It compares each song with:

- Favorite genre
- Favorite mood
- Target energy
- Acoustic preference
- Target popularity
- Preferred decade
- Target instrumentalness
- Target speechiness
- Target duration

### Intended use

VibeRank is designed for classroom exploration.

It can be used to:

- Demonstrate content-based recommendation
- Compare user profiles
- Study feature weights
- Compare ranking strategies
- Explore diversity and filter bubbles
- Practice transparent AI documentation

### Non-intended use

VibeRank should not be used as a commercial recommendation service.

It should not be used to make strong claims about a person's identity or complete musical taste. The data is fictional, small, and manually created.

---

## 3. Data

The system uses `data/songs.csv`.

The catalog contains **20 fictional songs** and **15 columns**.

### Basic attributes

- ID
- Title
- Artist
- Genre
- Mood
- Energy
- Tempo
- Valence
- Danceability
- Acousticness

### Five additional AI-assisted attributes

- Popularity
- Release decade
- Instrumentalness
- Speechiness
- Duration in seconds

Popularity ranges from 0 to 100.

Energy, valence, danceability, acousticness, instrumentalness, and speechiness range from 0.0 to 1.0.

The catalog includes pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, EDM, classical, folk, R&B, metal, reggae, country, Latin, and blues.

### Data limitations

Most genres contain only one song. The feature values are manually assigned and are not extracted from real recordings.

The catalog is too small to represent the full variety of music or listeners.

---

## 4. Algorithm Summary

VibeRank uses content-based filtering.

It scores every song against the user profile. It then sorts the songs and applies a diversity reranking step.

The default score uses nine components:

1. Genre match
2. Mood match
3. Energy similarity
4. Acoustic preference
5. Popularity similarity
6. Release-decade similarity
7. Instrumentalness similarity
8. Speechiness similarity
9. Duration similarity

Genre and mood use exact matching.

Numerical features use similarity. A song earns more points when its value is closer to the user's target.

Every strategy provides feature weights that total 100 points.

The scoring function returns a numeric score and a list of reasons. The reasons explain every component of the score.

---

## 5. Ranking Strategies

VibeRank uses the **Strategy design pattern**.

The shared `RankingStrategy` interface allows several weighting systems to be used without changing the scoring loop.

### Balanced

Balanced mode spreads weight across all nine features.

### Genre-first

Genre-first mode gives the largest weight to an exact genre match.

### Mood-first

Mood-first mode gives the largest weight to an exact mood match.

### Energy-first

Energy-first mode gives the largest weight to energy similarity.

Users select a strategy in `main.py`:

```bash
python -m src.main --mode balanced
python -m src.main --mode genre-first
python -m src.main --mode mood-first
python -m src.main --mode energy-first
```

This modular structure makes it easier to add another strategy later.

---

## 6. Diversity, Novelty, and Fairness

VibeRank applies diversity reranking after base scoring.

The system applies:

- A 10-point penalty for a repeated artist
- A 3-point penalty for a repeated genre

The penalty increases when the artist or genre has already appeared more than once.

Each penalty appears in the recommendation explanation.

### Why this helps

Without reranking, one artist or genre can dominate the top results. The penalty creates space for other artists and genres.

This can reduce a narrow filter bubble and improve exposure to different music.

### Tradeoff

Diversity is not automatically the same as relevance. A slightly lower-scoring song may move above a closer match.

Users can disable the feature:

```bash
python -m src.main --no-diversity
```

---

## 7. Explanation and Transparency

Each result contains:

- The selected strategy
- Genre points
- Mood points
- Energy points
- Acoustic points
- Popularity points
- Decade points
- Instrumentalness points
- Speechiness points
- Duration points
- Any artist or genre repetition penalty

The CLI displays these reasons in a formatted table.

This makes the model easier to inspect than a recommendation with only a title and unexplained score.

---

## 8. Evaluation Process

I evaluated the recommender with four profiles:

1. High-Energy Pop
2. Chill Lofi
3. Deep Intense Rock
4. Conflicting Classical Workout

I checked:

- Whether all 20 songs loaded
- Whether numeric fields had correct types
- Whether scores were consistent
- Whether rankings changed between profiles
- Whether ranking modes changed scores
- Whether diversity changed repeated-artist results
- Whether every explanation matched the calculation
- Whether automated tests passed

### High-Energy Pop

```text
1. Sunrise City - 97.55
2. Gym Hero - 78.23
3. Rooftop Lights - 73.53
4. Salsa Skyline - 61.04
5. City Cipher - 60.07
```

`Sunrise City` ranked first because it matched the requested pop genre and happy mood. It also closely matched energy, popularity, decade, instrumentalness, speechiness, and duration.

`Gym Hero` remained strong because it matched pop and several numeric targets. Its final result included a genre repetition penalty because a pop song had already been selected.

### Chill Lofi

```text
1. Library Rain - 98.06
2. Midnight Coding - 91.85
3. Spacewalk Thoughts - 71.08
4. Focus Flow - 64.15
5. Autumn Porch - 56.01
```

This profile shifted toward low-energy, acoustic, and instrumental songs.

`Library Rain` ranked first because its lofi genre, chill mood, energy, acousticness, instrumentalness, and duration closely matched the profile.

Compared with High-Energy Pop, the output contained calmer and more acoustic music.

### Deep Intense Rock

```text
1. Storm Runner - 98.50
2. Gym Hero - 74.69
3. Iron Pulse - 63.13
4. Salsa Skyline - 59.14
5. Electric Horizon - 58.45
```

This profile favored high energy and low acousticness.

`Storm Runner` matched the requested rock genre and intense mood. It also closely matched the numeric targets.

Compared with Chill Lofi, the results moved toward faster and more aggressive songs.

### Conflicting Classical Workout

```text
1. Quiet Constellations - 64.36
2. Iron Pulse - 58.92
3. Autumn Porch - 50.86
4. Focus Flow - 50.82
5. Spacewalk Thoughts - 50.51
```

This adversarial profile requested classical, aggressive, high-energy, and acoustic music.

No song matched all requirements.

`Quiet Constellations` matched classical and strong instrumentalness, but it poorly matched the requested energy and mood.

`Iron Pulse` matched aggressive mood and high energy, but it did not match classical or acoustic preferences.

This showed that the model can produce a mathematically consistent compromise that still feels imperfect to a person.

---

## 9. Experiments

### Mood removal

I temporarily changed the mood weight to zero.

Songs that depended on a mood match dropped in the ranking. This showed that mood was a meaningful signal rather than decorative metadata.

The original weight was restored after the experiment.

### Strategy comparison

I ran the same profile under balanced, genre-first, mood-first, and energy-first modes.

The scores changed because each strategy treated the features differently.

Genre-first made exact genre matches harder to overcome. Mood-first favored emotional alignment. Energy-first allowed songs from different genres to compete when their energy was close to the target.

### Diversity comparison

I compared results with diversity enabled and disabled.

With diversity enabled, repeated artists and genres received penalties. This could move a different artist higher in the list.

The explanation showed the exact penalty, making the reranking transparent.

---

## 10. Observed Behavior and Biases

### Exact-label bias

`pop` and `indie pop` are treated as different labels.

The system does not know that related genres may share musical qualities.

### Small-data bias

Most genres have one example. A genre match can therefore make one song dominate that category.

### Manual-feature bias

The attribute values were created manually. Different values could change the rankings.

### Weight bias

Weights express the designer's priorities. A score may appear objective even though the weights are selected by a person.

### Popularity bias

Popularity is one scoring feature. A user who targets high popularity may receive more mainstream songs.

### Filter-bubble risk

Content-based systems can repeatedly recommend what a user already likes.

The diversity component reduces repetition, but it does not eliminate filter bubbles.

### Context limitations

The system does not understand:

- Lyrics
- Language
- Culture
- Time of day
- Activity
- Social setting
- Long-term listening history
- Changes in taste
- Why the user requested a particular mood

---

## 11. Strengths

- The CSV loads with validation.
- All scores are numeric and deterministic.
- Four user profiles work without errors.
- Four ranking modes are selectable.
- Five new attributes affect scoring.
- Every score has an explanation.
- Diversity penalties are visible.
- Terminal tables improve readability.
- Tests cover core and stretch features.
- The code preserves both object-oriented and functional interfaces.

---

## 12. Ideas for Improvement

1. Add partial credit for related genres and moods.
2. Learn weights from real user feedback.
3. Expand the catalog with balanced genre coverage.
4. Extract features from real audio.
5. Add language and lyrical themes.
6. Let users control diversity strength.
7. Add a novelty preference.
8. Measure recommendation quality with user studies.
9. Compare the recommender with collaborative filtering.
10. Add persistent likes, skips, and replay history.

---

## 13. Personal Reflection

My biggest learning moment was seeing how strongly weights controlled the rankings.

The model does not understand music the way a person does. It follows rules and calculates similarities.

I was surprised that a simple weighted formula could still feel personalized. Different profiles produced clearly different recommendations from the same catalog.

AI tools helped me brainstorm features, scoring formulas, design patterns, diversity logic, tests, and documentation.

I still needed to review the generated work. I checked the CSV ranges, confirmed Python types, verified that weights totaled 100, ran multiple profiles, compared modes, inspected penalties, and ran the tests.

The mood-removal experiment was a useful reminder that output must be checked. The first attempt restored the weight too early. The terminal explanation revealed that mood points were still being awarded, so I corrected the experiment.

If I continued the project, I would use real audio features, learn from user feedback, add related-genre similarity, and test whether users actually prefer the diverse reranked results.