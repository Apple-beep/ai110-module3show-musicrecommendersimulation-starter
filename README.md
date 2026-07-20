# 🎵 VibeRank 2.0: Music Recommender Simulation

## Project Summary

VibeRank is a content-based music recommender built for classroom exploration. It loads a structured song catalog, compares every song with a user profile, calculates transparent numeric scores, reranks the results for diversity, and displays the recommendations in a terminal table.

The project includes all required features and four stretch features:

- 20-song CSV dataset
- Transparent weighted scoring
- Explanations for every score
- Four user profiles
- Five AI-assisted song attributes
- Four Strategy-pattern ranking modes
- Artist and genre diversity penalties
- A formatted `tabulate` results table

---

## How Music Recommendation Systems Work

Real systems such as Spotify and YouTube use two broad types of information.

### Input data

Input data describes the available content. For music, it may include:

- Genre
- Mood
- Tempo
- Energy
- Danceability
- Acousticness
- Popularity
- Release period
- Audio characteristics

### User data and preferences

A service may learn from:

- Likes
- Skips
- Replays
- Search history
- Playlist additions
- Listening duration
- Followed artists
- Explicit preferences

### Scoring and ranking

A recommendation system does not simply select a song at random. It gives each candidate a relevance score, sorts the candidates, and selects the highest-ranked results.

The process is:

```text
Song dataset + user preferences
              |
              v
       Score every song
              |
              v
    Apply diversity reranking
              |
              v
      Return top results
```

Input data, user preferences, and ranking are different parts of the system:

1. **Input data** describes songs.
2. **User preferences** describe what the listener wants.
3. **Scoring** measures how well one song fits.
4. **Ranking** compares all scores and chooses the top songs.

### Collaborative and content-based filtering

Collaborative filtering recommends content based on the behavior of similar users. It requires interaction data from many people.

Content-based filtering recommends songs based on their attributes. VibeRank uses content-based filtering because it can work with a small catalog and a single user profile.

---

## Dataset

The dataset is stored in `data/songs.csv`.

It contains **20 fictional songs** and **15 columns**.

### Original attributes

- `id`
- `title`
- `artist`
- `genre`
- `mood`
- `energy`
- `tempo_bpm`
- `valence`
- `danceability`
- `acousticness`

### Five stretch attributes

- `popularity`: value from 0 to 100
- `release_decade`: decade such as 1990, 2000, 2010, or 2020
- `instrumentalness`: value from 0.0 to 1.0
- `speechiness`: value from 0.0 to 1.0
- `duration_sec`: song duration in seconds

All numerical fields are converted to Python `int` or `float` values when the CSV loads.

The catalog contains pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, EDM, classical, folk, R&B, metal, reggae, country, Latin, and blues.

---

## User Profile

Each profile contains:

- Favorite genre
- Favorite mood
- Target energy
- Acoustic preference
- Target popularity
- Preferred release decade
- Target instrumentalness
- Target speechiness
- Target duration

The project includes four profiles:

1. High-Energy Pop
2. Chill Lofi
3. Deep Intense Rock
4. Conflicting Classical Workout

---

## Scoring Algorithm

Every ranking strategy provides weights that total **100 points**.

The score uses:

- Exact genre match
- Exact mood match
- Energy similarity
- Acoustic preference
- Popularity similarity
- Release-decade similarity
- Instrumentalness similarity
- Speechiness similarity
- Duration similarity

For a numerical feature, VibeRank rewards closeness to the target.

```text
similarity = max(0, 1 - absolute_difference / scale)
feature points = similarity × feature weight
```

For acousticness:

```text
If the user likes acoustic music:
    similarity = song acousticness

Otherwise:
    similarity = 1 - song acousticness
```

The function returns:

```python
(score, reasons)
```

The reasons show exactly where the score came from.

---

## Multiple Ranking Modes

VibeRank uses the **Strategy design pattern**.

Available strategies:

- `balanced`
- `genre-first`
- `mood-first`
- `energy-first`

Each class provides different feature weights while the scoring and ranking loops remain unchanged.

Run a mode with:

```bash
python -m src.main --mode balanced
python -m src.main --mode genre-first
python -m src.main --mode mood-first
python -m src.main --mode energy-first
```

Run one profile:

```bash
python -m src.main --profile high-energy-pop --mode balanced
```

Run all profiles:

```bash
python -m src.main --profile all --mode balanced
```

---

## Diversity and Fairness Reranking

A recommender can create a filter bubble by repeatedly returning the same artist or genre.

VibeRank applies:

- Artist repetition penalty: `-10` points per prior appearance
- Genre repetition penalty: `-3` points per prior appearance

The penalties are applied while selecting the final top results. Every penalty appears in the explanation.

Disable diversity for comparison:

```bash
python -m src.main --profile chill-lofi --no-diversity
```

This feature improves variety, but it may occasionally move a slightly lower-scoring song above a closer personal match.

---

## Setup

From the repository root:

```bash
pip install -r requirements.txt
```

Run the program:

```bash
python -m src.main
```

Run tests:

```bash
python -m pytest
```

---

## Formatted Recommendation Output

The CLI uses `tabulate` and displays rank, song, artist, genre, score, and reasons.

Example for the High-Energy Pop profile using balanced mode:

```text
+------+----------------+---------------+-----------+-------+--------------------------------------------------------------+
| Rank | Song           | Artist        | Genre     | Score | Reasons                                                      |
+------+----------------+---------------+-----------+-------+--------------------------------------------------------------+
| 1    | Sunrise City   | Neon Echo     | pop       | 97.55 | mode: balanced; genre match: pop (+20.00); mood match:       |
|      |                |               |           |       | happy (+15.00); energy similarity (+14.70); non-acoustic     |
|      |                |               |           |       | preference (+8.20); popularity (+9.90); decade (+8.00);      |
|      |                |               |           |       | instrumentalness (+7.92); speechiness (+6.86); duration      |
|      |                |               |           |       | (+6.97)                                                      |
+------+----------------+---------------+-----------+-------+--------------------------------------------------------------+
| 2    | Gym Hero       | Max Pulse     | pop       | 78.23 | genre match (+20.00); energy (+13.05); non-acoustic          |
|      |                |               |           |       | preference (+9.50); popularity (+9.40); decade (+8.00);      |
|      |                |               |           |       | instrumentalness (+7.76); speechiness (+6.93); duration      |
|      |                |               |           |       | (+6.59); genre repetition penalty (-3.00)                    |
+------+----------------+---------------+-----------+-------+--------------------------------------------------------------+
| 3    | Rooftop Lights | Indigo Parade | indie pop | 73.53 | mood match (+15.00); energy (+14.40); non-acoustic           |
|      |                |               |           |       | preference (+6.50); popularity (+9.70); decade (+6.40);      |
|      |                |               |           |       | instrumentalness (+7.76); speechiness (+6.86); duration      |
|      |                |               |           |       | (+6.91)                                                      |
+------+----------------+---------------+-----------+-------+--------------------------------------------------------------+
```

The live terminal output contains the complete generated explanations.

---

## Evaluation Results

Balanced mode with diversity enabled produced these top results.

### High-Energy Pop

```text
1. Sunrise City - 97.55
2. Gym Hero - 78.23
3. Rooftop Lights - 73.53
4. Salsa Skyline - 61.04
5. City Cipher - 60.07
```

### Chill Lofi

```text
1. Library Rain - 98.06
2. Midnight Coding - 91.85
3. Spacewalk Thoughts - 71.08
4. Focus Flow - 64.15
5. Autumn Porch - 56.01
```

### Deep Intense Rock

```text
1. Storm Runner - 98.50
2. Gym Hero - 74.69
3. Iron Pulse - 63.13
4. Salsa Skyline - 59.14
5. Electric Horizon - 58.45
```

### Conflicting Classical Workout

```text
1. Quiet Constellations - 64.36
2. Iron Pulse - 58.92
3. Autumn Porch - 50.86
4. Focus Flow - 50.82
5. Spacewalk Thoughts - 50.51
```

The profiles produced different outputs because their categorical targets, numeric targets, and acoustic preferences were different.

The adversarial classical-workout profile exposed a limitation. No song matched classical, aggressive, high-energy, and acoustic preferences at the same time, so the system produced a numerical compromise.

---

## AI-Assisted Development

AI tools helped:

- Generate five additional song attributes
- Propose values for all 20 songs
- Compare possible ranking designs
- Implement Strategy classes
- Brainstorm diversity reranking
- Create test cases
- Format the terminal table

The work was manually verified. The CSV structure, ranges, types, formulas, strategy totals, ranking behavior, explanations, and tests were checked.

See [`ai_interactions.md`](ai_interactions.md) for prompts and verification notes.

---

## Limitations

- The dataset is small and fictional.
- Most genres contain only one song.
- Genre and mood matching are exact.
- Related labels such as `pop` and `indie pop` receive no partial credit.
- Feature values were assigned manually rather than extracted from audio.
- The system does not learn from likes, skips, or replays.
- Diversity penalties are manually selected.
- Personal and cultural context are not represented.
- A 100-point weighted score can feel precise even when the underlying assumptions are simple.

---

## Future Improvements

- Add partial credit for related genres and moods
- Learn weights from user feedback
- Extract features from real audio
- Expand and balance the catalog
- Add language and lyrical themes
- Add a discovery or novelty preference
- Evaluate recommendation quality with real users

---

## Reflection

The project showed that recommendation systems do not directly understand whether music is good. They translate selected features into scores and rankings.

The strongest lesson was that weights behave like hidden priorities. A simple formula can feel personalized, but it can also create surprising or biased results.

AI tools accelerated brainstorming and implementation, but the generated work still required validation. The mood-removal experiment demonstrated this clearly because the first run had restored the weight too early. Reading the output revealed the mistake.

The complete reflection and evaluation are documented in [`model_card.md`](model_card.md).