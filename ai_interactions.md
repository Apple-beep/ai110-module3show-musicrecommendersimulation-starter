# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

> I asked the AI assistant to examine the starter song dataset and generate 10 additional fictional songs while preserving the existing CSV structure. The goal was to increase the catalog from 10 to 20 songs and introduce genres and moods that were missing from the starter data.


**Prompts used:**

> The attached songs.csv contains 10 fictional songs with the headers id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, and acousticness. Generate 10 additional fictional songs in valid CSV format. Continue the IDs from 11 through 20, preserve the headers, introduce missing genres and moods, keep normalized features between 0.0 and 1.0, and use realistic tempo values.

**What did the agent generate or change?**

> The AI proposed 10 new songs representing hip-hop, EDM, classical, folk, R&B, metal, reggae, country, Latin, and blues. It also proposed new moods such as confident, euphoric, peaceful, romantic, aggressive, joyful, nostalgic, celebratory, and sad.

**What did you verify or fix manually?**

I verified that:

- Every song had exactly 10 CSV fields.
- IDs were unique and continued from 11 through 20.
- Energy, valence, danceability, and acousticness stayed between 0.0 and 1.0.
- Tempo values were positive and reasonable.
- Titles and artist names did not contain unescaped commas.
- New genres and moods expanded the diversity of the catalog.
- The CSV loaded successfully using Python's `csv.DictReader`.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
