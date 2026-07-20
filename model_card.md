# 🎧 Model Card: VibeRank 1.0

## 1. Model Name

**VibeRank 1.0**

VibeRank is a small content-based music recommendation simulation that ranks songs according to a listener's stated preferences.

---

## 2. Intended Use

VibeRank is designed for classroom exploration of how recommendation systems transform structured data into personalized predictions.

The system recommends fictional songs by comparing their musical attributes with a user profile. It assumes that the listener can describe their current preferences using:

- One favorite genre
- One favorite mood
- A target energy level
- An acoustic or non-acoustic preference

This project is not intended for production use or for making complete claims about a person's musical identity. Real listeners may enjoy multiple genres, change preferences depending on context, or want music that is intentionally different from their usual taste.

---

## 3. How the Model Works

VibeRank uses content-based filtering. Instead of comparing the user with other listeners, it compares the user's stated preferences directly with the attributes of each song.

Each song is evaluated using four scoring components:

| Feature | Maximum Points |
|---|---:|
| Genre match | 35 |
| Mood match | 25 |
| Energy similarity | 25 |
| Acoustic preference | 15 |
| **Total** | **100** |

Genre and mood use exact matching. A song receives the full number of points when its genre or mood matches the user profile.

Energy uses numerical similarity. Songs receive more points when their energy value is closer to the user's target energy. This prevents the model from simply rewarding songs for being more energetic.

Acousticness is handled according to the user's preference. If the user likes acoustic music, songs with higher acousticness receive more points. If the user prefers non-acoustic music, songs with lower acousticness receive more points.

The system scores every song, sorts the catalog from highest score to lowest score, and returns the top results. Each recommendation also includes an explanation showing how many points came from each feature.

The starter project originally contained placeholder functions. I implemented CSV loading, numerical type conversion, weighted scoring, explanation generation, sorting, and command-line output.

---

## 4. Data

The catalog contains **20 fictional songs**.

The original starter dataset contained 10 songs. I added 10 more songs to increase the number of represented genres and moods.

The catalog includes the following genres:

- Pop
- Lofi
- Rock
- Ambient
- Jazz
- Synthwave
- Indie pop
- Hip-hop
- EDM
- Classical
- Folk
- R&B
- Metal
- Reggae
- Country
- Latin
- Blues

The moods include:

- Happy
- Chill
- Intense
- Relaxed
- Moody
- Focused
- Confident
- Euphoric
- Peaceful
- Warm
- Romantic
- Aggressive
- Joyful
- Nostalgic
- Celebratory
- Sad

Each song contains:

- ID
- Title
- Artist
- Genre
- Mood
- Energy
- Tempo in beats per minute
- Valence
- Danceability
- Acousticness

The current scoring system uses genre, mood, energy, and acousticness. Tempo, valence, and danceability are stored in the dataset but are not yet included in the default score.

The feature values were manually assigned for this simulation. They were not calculated by analyzing real audio files.

---

## 5. Strengths

The model performs well when the dataset contains a song that matches most or all of the user's preferences.

For example, `Sunrise City` is a strong recommendation for the High-Energy Pop profile because it matches the requested genre and mood, has energy close to the user's target, and has low acousticness.

The numerical energy comparison works better than an exact-match rule. A song with energy of `0.82` can still strongly match a target energy of `0.80`.

The generated explanations make the system transparent. A user can see exactly why a song ranked highly and how much each feature contributed to the score.

The different test profiles also produced noticeably different results. High-energy profiles favored energetic and non-acoustic songs, while the Chill Lofi profile favored calm songs with greater acousticness.

---

## 6. Limitations and Bias

The recommender uses exact text matching for genre and mood. Related genres such as `pop` and `indie pop` are treated as completely different. This caused `Rooftop Lights` to receive no genre points for the pop profile, even though many listeners would consider indie pop closely related to pop.

The dataset contains only 20 fictional songs, and most genres have only one example. This means some user profiles have very few realistic choices, and one song may automatically dominate a genre.

Fixed feature weights can create unintuitive recommendations when preferences conflict. The Conflicting Classical Workout profile ranked a peaceful, low-energy classical song first because its genre and acousticness points outweighed its poor mood and energy match.

The model may also create a filter bubble because it repeatedly rewards songs that match the user's existing preferences. It does not deliberately encourage discovery or introduce unfamiliar genres.

The system does not consider:

- Lyrics or language
- Listening history
- Likes, skips, or replays
- Artist preferences
- Time of day
- Activity or location
- Cultural context
- Changes in musical taste
- Whether the user wants familiar or surprising music

---

## 7. Evaluation

I evaluated the recommender using four different user profiles:

1. High-Energy Pop
2. Chill Lofi
3. Deep Intense Rock
4. Conflicting Classical Workout

I checked whether the top songs matched my expectations and whether changing the user preferences produced meaningful changes in the rankings.

### High-Energy Pop

This profile requested:

- Genre: pop
- Mood: happy
- Target energy: 0.80
- Non-acoustic music

```text
1. Sunrise City by Neon Echo
   Score: 96.80
   Reasons: genre match (+35.00), mood match (+25.00),
   energy similarity (+24.50), non-acoustic preference (+12.30)

2. Gym Hero by Max Pulse
   Score: 71.00
   Reasons: genre match (+35.00), mood mismatch (+0.00),
   energy similarity (+21.75), non-acoustic preference (+14.25)

3. Rooftop Lights by Indigo Parade
   Score: 58.75
   Reasons: genre mismatch (+0.00), mood match (+25.00),
   energy similarity (+24.00), non-acoustic preference (+9.75)

4. City Cipher by Rhyme District
   Score: 37.30
   Reasons: genre mismatch (+0.00), mood mismatch (+0.00),
   energy similarity (+23.50), non-acoustic preference (+13.80)

5. Electric Horizon by Nova Circuit
   Score: 35.80
   Reasons: genre mismatch (+0.00), mood mismatch (+0.00),
   energy similarity (+21.25), non-acoustic preference (+14.55)
```

`Sunrise City` ranked first because it matched all major preferences.

`Gym Hero` ranked second even though its mood was intense because it matched the pop genre, had energy near the user's target, and strongly matched the non-acoustic preference.

`Rooftop Lights` matched the happy mood and target energy, but its `indie pop` genre did not count as an exact match for `pop`.

### Chill Lofi

This profile requested:

- Genre: lofi
- Mood: chill
- Target energy: 0.35
- Acoustic music

```text
1. Library Rain by Paper Lanterns
   Score: 97.90
   Reasons: genre match (+35.00), mood match (+25.00),
   energy similarity (+25.00), acoustic preference (+12.90)

2. Midnight Coding by LoRoom
   Score: 93.90
   Reasons: genre match (+35.00), mood match (+25.00),
   energy similarity (+23.25), acoustic preference (+10.65)

3. Focus Flow by LoRoom
   Score: 70.45
   Reasons: genre match (+35.00), mood mismatch (+0.00),
   energy similarity (+23.75), acoustic preference (+11.70)

4. Spacewalk Thoughts by Orbit Bloom
   Score: 62.05
   Reasons: genre mismatch (+0.00), mood match (+25.00),
   energy similarity (+23.25), acoustic preference (+13.80)

5. Coffee Shop Stories by Slow Stereo
   Score: 37.85
   Reasons: genre mismatch (+0.00), mood mismatch (+0.00),
   energy similarity (+24.50), acoustic preference (+13.35)
```

`Library Rain` ranked first because it matched the genre and mood, exactly matched the target energy, and had high acousticness.

Compared with High-Energy Pop, the Chill Lofi results shifted toward lower-energy and more acoustic music.

`Spacewalk Thoughts` reached fourth place even though it was ambient because it matched the chill mood, low energy, and acoustic preference.

### Deep Intense Rock

This profile requested:

- Genre: rock
- Mood: intense
- Target energy: 0.92
- Non-acoustic music

```text
1. Storm Runner by Voltline
   Score: 98.25
   Reasons: genre match (+35.00), mood match (+25.00),
   energy similarity (+24.75), non-acoustic preference (+13.50)

2. Gym Hero by Max Pulse
   Score: 64.00
   Reasons: genre mismatch (+0.00), mood match (+25.00),
   energy similarity (+24.75), non-acoustic preference (+14.25)

3. Electric Horizon by Nova Circuit
   Score: 38.80
   Reasons: genre mismatch (+0.00), mood mismatch (+0.00),
   energy similarity (+24.25), non-acoustic preference (+14.55)

4. Iron Pulse by Gravel Crown
   Score: 38.15
   Reasons: genre mismatch (+0.00), mood mismatch (+0.00),
   energy similarity (+23.75), non-acoustic preference (+14.40)

5. City Cipher by Rhyme District
   Score: 37.30
   Reasons: genre mismatch (+0.00), mood mismatch (+0.00),
   energy similarity (+23.50), non-acoustic preference (+13.80)
```

`Storm Runner` ranked first because it matched every major preference.

Compared with Chill Lofi, the results shifted toward higher-energy and less acoustic songs.

`Gym Hero` ranked second despite being pop because it matched the intense mood and was extremely close to the target energy.

### Conflicting Classical Workout

This adversarial profile requested:

- Genre: classical
- Mood: aggressive
- Target energy: 0.95
- Acoustic music

```text
1. Quiet Constellations by Elena Vale
   Score: 56.45
   Reasons: genre match (+35.00), mood mismatch (+0.00),
   energy similarity (+6.75), acoustic preference (+14.70)

2. Iron Pulse by Gravel Crown
   Score: 50.10
   Reasons: genre mismatch (+0.00), mood match (+25.00),
   energy similarity (+24.50), acoustic preference (+0.60)

3. Old Highway Home by June Hollow
   Score: 27.80
   Reasons: genre mismatch (+0.00), mood mismatch (+0.00),
   energy similarity (+14.75), acoustic preference (+13.05)

4. Autumn Porch by Willow Roads
   Score: 26.85
   Reasons: genre mismatch (+0.00), mood mismatch (+0.00),
   energy similarity (+12.75), acoustic preference (+14.10)

5. Salsa Skyline by Ritmo Solar
   Score: 26.00
   Reasons: genre mismatch (+0.00), mood mismatch (+0.00),
   energy similarity (+23.75), acoustic preference (+2.25)
```

No song matched all four preferences.

`Quiet Constellations` ranked first because its classical genre and high acousticness contributed almost 50 points. However, it had a peaceful mood and very low energy.

`Iron Pulse` ranked second because it matched the aggressive mood and target energy, but it was metal and almost completely non-acoustic.

This was the most surprising result. It showed that the model can produce a mathematically valid ranking that may still feel inappropriate to a listener.

### Profile Comparisons

The High-Energy Pop and Chill Lofi profiles produced clearly different results. The pop profile favored energetic, electronically produced music, while the lofi profile favored calm and acoustic songs.

The Chill Lofi and Deep Intense Rock profiles showed opposite patterns. Chill Lofi favored lower energy and higher acousticness, while Deep Intense Rock favored high energy and low acousticness.

The Conflicting Classical Workout profile showed that the recommender cannot understand which preference is truly most important unless the weights explicitly define that priority.

### Mood-Removal Experiment

I temporarily changed the mood weight from 25 points to 0 points and reran all four profiles.

For High-Energy Pop, `Rooftop Lights` dropped out of the top five because its happy mood no longer contributed 25 points. High-energy songs with low acousticness moved above it.

For Chill Lofi, `Spacewalk Thoughts` dropped out of the top five because its chill mood had been one of its strongest matches. `Focus Flow` also moved above `Midnight Coding` because energy and acousticness became more important than mood.

For Deep Intense Rock, `Gym Hero` dropped from 64.00 to 39.00 because its intense mood no longer earned points.

For Conflicting Classical Workout, `Iron Pulse` dropped out of the top five because its aggressive mood had previously contributed 25 points.

Removing mood made the recommendations more dependent on genre, energy, and acousticness. The results were different, but they were less aligned with the emotional experience requested by the user.

After completing the experiment, I restored the original mood weight to 25 points and reran the automated tests. Both tests passed.

---

## 8. Future Work

A future version could give partial credit to related genres instead of requiring exact text matches. For example, `indie pop` could receive some genre points for a `pop` profile.

The system could use tempo, valence, and danceability, which are already stored in the dataset.

Additional improvements could include:

- Supporting multiple favorite genres and moods
- Allowing users to control feature weights
- Creating Genre-First, Mood-First, and Energy-First modes
- Penalizing repeated artists
- Rewarding genre and mood diversity
- Adding a discovery mode
- Learning from likes, skips, and replays
- Expanding and balancing the dataset
- Extracting feature values from real audio
- Using context such as activity or time of day

A diversity rule could reserve one recommendation for a related but unfamiliar genre. This could reduce filter bubbles and help listeners discover new music.

---

## 9. Personal Reflection

This project showed me that recommendation systems do not directly know whether a song is good. They turn selected features into numerical scores and rank the results according to rules created by the designer.

The experiments showed that feature weights act like hidden priorities. A recommendation can be mathematically correct while still feeling wrong to a real listener.

I was surprised by how much removing one feature changed the rankings. This helped me understand why real recommendation systems require larger datasets, user feedback, multiple ranking signals, diversity controls, and regular evaluation for bias.