# AI Interactions Log

This file documents how AI tools supported the stretch features and what I verified manually.

---

## 1. Agentic Workflow: Additional Song Attributes

### Task given to the AI

I asked the AI assistant to expand the existing 20-song CSV with five additional meaningful attributes and update the Python project so those attributes affected scoring.

### Prompt used

> Review this music recommender project. Add five meaningful song attributes to every CSV row: popularity from 0 to 100, release_decade, instrumentalness from 0.0 to 1.0, speechiness from 0.0 to 1.0, and duration_sec. Preserve all existing songs and columns. Update the Song dataclass, CSV loader, user profiles, scoring logic, explanations, and tests. Make each new attribute contribute to the recommendation score. Keep every ranking strategy at a total of 100 points.

### Generated changes

The AI proposed:

- Five new CSV columns:
  - `popularity`
  - `release_decade`
  - `instrumentalness`
  - `speechiness`
  - `duration_sec`
- Values for all 20 fictional songs
- Matching target preferences in each user profile
- Similarity formulas for each new numeric feature
- Score explanations that show the points earned from each attribute
- Tests that verify the new columns load with the correct Python types

### Manual verification

I manually verified that:

- The CSV still contains exactly 20 songs.
- Every row has exactly 15 fields.
- Popularity values are between 0 and 100.
- Instrumentalness and speechiness values are between 0.0 and 1.0.
- Release decades are valid integers.
- Duration values are positive.
- All numerical fields are converted to `int` or `float`.
- Every new attribute appears in the scoring explanations.
- Every ranking strategy totals exactly 100 points.
- The full test suite passes.

---

## 2. Strategy Design Pattern

### Pattern used

I used the **Strategy pattern**.

### Prompt used

> I need multiple selectable ranking modes without copying the full recommendation algorithm. Compare a long if/elif block with the Strategy design pattern. Implement separate strategies for balanced, genre-first, mood-first, and energy-first ranking. Each strategy should return feature weights that total 100. The command-line program must let the user select a mode.

### How AI helped

The AI explained that the ranking loop should remain unchanged while interchangeable strategy classes provide different feature weights. This was cleaner than placing many conditional branches inside `score_song`.

### How the pattern appears in the code

- `RankingStrategy` defines the shared interface.
- `BalancedStrategy` balances all song features.
- `GenreFirstStrategy` places the largest weight on genre.
- `MoodFirstStrategy` places the largest weight on mood.
- `EnergyFirstStrategy` places the largest weight on energy similarity.
- `STRATEGIES` stores the available strategy objects.
- `score_song` selects a strategy using the `mode` argument.
- `main.py` exposes the selection through `--mode`.

### Manual verification

I ran:

```bash
python -m src.main --mode balanced
python -m src.main --mode genre-first
python -m src.main --mode mood-first
python -m src.main --mode energy-first
```

I confirmed that the displayed mode changed and that scores or rankings changed between strategies.

---

## 3. Diversity, Novelty, and Fairness

### Prompt used

> Add a transparent diversity reranking step after base song scoring. Penalize repeated artists by 10 points and repeated genres by 3 points while selecting the top results. Preserve deterministic ranking and add every penalty to the explanation text. Include a switch that disables diversity for comparison.

### Generated changes

The AI proposed a greedy reranking function called `diversify_rankings`. It evaluates the remaining candidates after every selection and applies:

- Artist repetition penalty: `-10` points for each prior appearance
- Genre repetition penalty: `-3` points for each prior appearance

The CLI includes `--no-diversity` so the behavior can be compared with and without reranking.

### Manual verification

I verified that:

- A repeated artist can move lower in the final list.
- A repeated genre receives a smaller penalty.
- The adjusted score is shown in the table.
- The explanation includes the exact penalty.
- Disabling diversity restores normal score sorting.
- A unit test checks both artist and genre penalties.

---

## 4. Formatted Summary Table

### Prompt used

> Replace the vertical recommendation output with a readable terminal table using `tabulate`. Include rank, song, artist, genre, adjusted score, and the complete explanation. Wrap long explanations so the output remains readable.

### Generated changes

The AI added:

- `tabulate>=0.9.0` to `requirements.txt`
- A grid-style terminal table
- Columns for rank, song, artist, genre, score, and reasons
- Wrapped explanation text for transparency

### Manual verification

I installed the requirements and ran the program from the repository root. I confirmed that the table displays all requested columns and that the reasons include the original score components and any diversity penalties.

---

## 5. General AI Use and Human Review

AI tools helped with brainstorming, code structure, edge cases, and documentation. I did not accept the output without checking it.

I manually:

- Reviewed every formula
- Validated the CSV
- Compared multiple user profiles
- Tested every ranking mode
- Compared diversity on and off
- Ran automated tests
- Corrected an earlier experiment when the mood weight had already been restored before the experimental run