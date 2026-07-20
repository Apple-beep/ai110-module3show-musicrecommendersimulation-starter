# 🎵 Music Recommender Simulation

## Project Summary

This project simulates a small content-based music recommendation system. It represents songs using structured features such as genre, mood, energy, tempo, valence, danceability, and acousticness. It also represents a listener's musical taste using a user profile.

The recommender compares each song with the user's preferences, calculates a weighted relevance score, ranks all songs from the strongest match to the weakest match, and returns the top recommendations. The project demonstrates how recommendation systems transform input data and user preferences into personalized predictions.

---

## How The System Works

### How Real Recommendation Systems Work

Real-world platforms such as Spotify, YouTube, and TikTok collect information about users and available content to predict what each user may enjoy next.

User behavior data may include:

- Likes
- Skips
- Replays
- Listening time
- Playlist additions
- Searches
- Shares
- Following an artist
- Previously played songs

Content data may include:

- Genre
- Mood
- Energy
- Tempo
- Artist
- Danceability
- Acousticness
- Audio characteristics

Recommendation systems commonly use collaborative filtering, content-based filtering, or a combination of both.

#### Collaborative Filtering

Collaborative filtering uses behavior from many users. It identifies users with similar listening patterns and recommends songs that similar listeners enjoyed.

For example, if two users listen to many of the same songs, the system may recommend a song that one user liked but the other user has not heard.

Collaborative filtering depends mainly on user interactions rather than directly analyzing song characteristics.

#### Content-Based Filtering

Content-based filtering compares song attributes with an individual user's preferences.

For example, if a user prefers happy pop songs with high energy, the system searches for songs whose genre, mood, and energy closely match those preferences.

This project uses content-based filtering because it can generate recommendations using song features and one user profile without requiring behavior data from thousands of users.

### Recommendation Process

The system separates the recommendation process into four main parts:

1. **Input data:** The song dataset describes all available songs.
2. **User preferences:** The user profile describes the listener's musical taste.
3. **Scoring rule:** The recommender calculates how well one song matches the user.
4. **Ranking rule:** The recommender scores every song, sorts them from highest to lowest, and returns the top results.

A simplified flow of the system is:

```text
Song Dataset + User Profile
            |
            v
     Score Every Song
            |
            v
 Sort Songs by Score
            |
            v
Return Top Recommendations
```

### Song Features

Each `Song` object uses the following features:

- `id`: A unique identifier for the song
- `title`: The name of the song
- `artist`: The artist who created or performed the song
- `genre`: The broad musical category
- `mood`: The emotional feeling associated with the song
- `energy`: The intensity of the song from 0.0 to 1.0
- `tempo_bpm`: The speed of the song in beats per minute
- `valence`: The musical positivity of the song from 0.0 to 1.0
- `danceability`: How suitable the song is for dancing
- `acousticness`: How strongly the song contains acoustic qualities

The starter dataset currently contains 10 songs. Its genres include pop, lofi, rock, ambient, jazz, synthwave, and indie pop.

The first version of the recommender will focus on:

- Genre
- Mood
- Energy
- Acousticness

Tempo, valence, and danceability can later be added to alternative ranking modes.

### User Profile Features

Each `UserProfile` stores:

- `favorite_genre`: The user's preferred musical genre
- `favorite_mood`: The user's preferred emotional mood
- `target_energy`: The user's desired song energy from 0.0 to 1.0
- `likes_acoustic`: Whether the user prefers songs with acoustic qualities

The song data and user preferences are kept separate. Song data describes the available content, while the user profile describes what the listener currently wants.

### Algorithm Recipe

Each song will receive a score out of 100 points.

| Feature | Maximum Points |
|---|---:|
| Genre match | 35 |
| Mood match | 25 |
| Energy similarity | 25 |
| Acoustic preference | 15 |
| **Total** | **100** |

#### Genre Score

A song receives 35 points when its genre matches the user's favorite genre.

```text
If song genre matches favorite genre:
    genre score = 35
Otherwise:
    genre score = 0
```

Genre receives the largest weight because it represents the user's broad musical preference.

#### Mood Score

A song receives 25 points when its mood matches the user's favorite mood.

```text
If song mood matches favorite mood:
    mood score = 25
Otherwise:
    mood score = 0
```

Mood helps represent the emotional experience the user wants.

#### Energy Similarity Score

Energy is a numerical feature, so the recommender rewards songs that are close to the user's target energy instead of simply rewarding songs with higher energy.

```text
energy difference = absolute value of(song energy - target energy)

energy similarity = 1 - energy difference

energy score = energy similarity × 25
```

For example, suppose the user's target energy is `0.80` and a song has an energy value of `0.75`.

```text
energy difference = |0.75 - 0.80|
energy difference = 0.05

energy similarity = 1 - 0.05
energy similarity = 0.95

energy score = 0.95 × 25
energy score = 23.75
```

The song receives 23.75 out of 25 energy points because its energy is very close to the user's preference.

#### Acoustic Preference Score

If the user likes acoustic music, songs with higher acousticness receive more points.

```text
acoustic score = song acousticness × 15
```

If the user does not prefer acoustic music, songs with lower acousticness receive more points.

```text
acoustic score = (1 - song acousticness) × 15
```

This allows the system to reward either acoustic or non-acoustic songs depending on the user's preference.

### Scoring Rule Versus Ranking Rule

The scoring rule and ranking rule have different responsibilities.

The scoring rule evaluates one song:

```text
How well does this song match the user?
```

The ranking rule evaluates the full catalog:

```text
Which songs have the highest scores?
```

The scoring function calculates a numeric score for each song. The recommendation function applies that scoring function to every song, sorts the songs by score, and selects the top results.

Keeping these responsibilities separate makes the program easier to understand, test, and modify. The scoring formula can change without rewriting the entire ranking process.

### Recommendation Selection

The recommender will follow these steps:

1. Load songs from `data/songs.csv`.
2. Read the user's preferences.
3. Calculate a score for each song.
4. Record the reasons each song earned points.
5. Sort all songs from highest score to lowest score.
6. Return the top three or five songs.
7. Display each recommendation with its score and explanation.

A recommendation explanation might look like:

```text
Recommended because the song matches your favorite genre,
matches your preferred mood, and has energy close to your target.
```

### Dataset Observations

The starter dataset includes the following attributes:

- Genre and mood are categorical features.
- Energy, valence, danceability, and acousticness use values from 0.0 to 1.0.
- Tempo is measured in beats per minute.
- The current catalog contains 10 songs.

The dataset is not evenly balanced. Lofi appears more often than most genres, and chill appears more often than most moods. Some genres and moods only appear once.

This imbalance could cause certain musical styles to appear more frequently in recommendations simply because the dataset contains more examples of them.

### Bias and Filter-Bubble Risk

A content-based recommender can create a filter bubble by repeatedly suggesting music that closely matches what the user already likes.

For example, a user who selects pop as their favorite genre may continue receiving pop recommendations and may rarely discover jazz, ambient, rock, or other genres.

Bias can also appear because:

- The dataset is small.
- Some genres have more songs than others.
- Mood labels are simplified.
- The system does not understand lyrics or language.
- The system does not consider cultural context.
- The user profile represents only a few preferences.
- Musical taste may change depending on activity, location, or time.

Future versions can reduce these problems by:

- Adding more songs
- Balancing genres and moods
- Limiting repeated artists
- Rewarding variety in the top results
- Adding a discovery mode
- Allowing multiple favorite genres
- Learning from likes and skips
- Using tempo, valence, and danceability
- Occasionally recommending a relevant song outside the user's usual preferences

---

## Getting Started

### Setup

1. Create a virtual environment. This step is optional but recommended.

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows:

   ```bash
   .venv\Scripts\activate
   ```

2. Install dependencies:

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

Additional tests can be added in `tests/test_recommender.py`.

---

## Sample Recommendation Output

The following recommendations were generated for a user who prefers happy, high-energy pop music with non-acoustic production.

```text
Loaded songs: 20

User profile
------------
Favorite genre: pop
Favorite mood: happy
Target energy: 0.80
Likes acoustic: False

Top recommendations
===================

1. Sunrise City by Neon Echo
   Score: 96.80/100.00
   Reasons: genre match: pop (+35.00); mood match: happy (+25.00); energy similarity 0.98 (+24.50); non-acoustic preference (+12.30)

2. Gym Hero by Max Pulse
   Score: 71.00/100.00
   Reasons: genre match: pop (+35.00); mood mismatch: intense (+0.00); energy similarity 0.87 (+21.75); non-acoustic preference (+14.25)

3. Rooftop Lights by Indigo Parade
   Score: 58.75/100.00
   Reasons: genre mismatch: indie pop (+0.00); mood match: happy (+25.00); energy similarity 0.96 (+24.00); non-acoustic preference (+9.75)

4. City Cipher by Rhyme District
   Score: 37.30/100.00
   Reasons: genre mismatch: hip-hop (+0.00); mood mismatch: confident (+0.00); energy similarity 0.94 (+23.50); non-acoustic preference (+13.80)

5. Electric Horizon by Nova Circuit
   Score: 35.80/100.00
   Reasons: genre mismatch: edm (+0.00); mood mismatch: euphoric (+0.00); energy similarity 0.85 (+21.25); non-acoustic preference (+14.55)

**Screenshot or video:** To be added after implementation.

---

## Experiments You Tried

This section will be completed after testing the recommender with multiple user profiles and scoring weights.

Planned experiments include:

- Comparing high-energy and low-energy profiles
- Changing the genre weight
- Changing the mood weight
- Adding tempo to the score
- Adding valence and danceability
- Testing acoustic and non-acoustic preferences
- Comparing results across different ranking modes

---

## Limitations and Risks

The current design has several limitations:

- It uses a very small song catalog.
- The starter dataset contains only 10 songs.
- Some genres and moods are underrepresented.
- It does not understand lyrics or language.
- It does not learn automatically from user behavior.
- It assumes the user's preferences remain fixed.
- It may repeatedly recommend similar songs.
- It may over-favor genres with more entries in the dataset.
- Its feature weights are selected manually.

These limitations will be discussed in greater detail in the model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

The final reflection will be completed after implementing and testing the recommender. It will discuss how structured data, scoring rules, and ranking algorithms turn song attributes into predictions. It will also examine how limited datasets and manually selected weights can introduce bias or reduce musical diversity.