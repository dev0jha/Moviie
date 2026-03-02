# MOVIIE — Movie Recommendation CLI

**MOVIIE** is a Python-based command-line application that recommends movies based on a **content-based filtering** approach.  
It uses **TF‑IDF** on movie overviews and **cosine similarity** to find movies similar to a title you enter.

The project includes an interactive, styled terminal UI (built with **Rich**) and works with the included TMDB 5000 dataset CSV files.

---

## Features

- Search a movie title and get **top recommendations**
- **Random movie pick** (with option to fetch recommendations for it)
- Browse the **top 20 movies** from the dataset
- Clean, interactive CLI interface using **Rich**

---

## Tech Stack

- **Python 3**
- **pandas** for dataset handling
- **scikit-learn** for TF‑IDF vectorization + cosine similarity
- **Rich** for terminal UI (menus, tables, panels)

Dependencies (as pinned in `requirements.txt`):
- joblib, numpy, pandas, scikit-learn, scipy, threadpoolctl, python-dateutil, pytz, six, tzdata

---

## Project Structure

```text
Moviie/
├─ main.py
├─ requirements.txt
├─ cli/
│  └─ interface.py
├─ recommender/
│  └─ content_based.py
└─ data/
   ├─ tmdb_5000_movies.csv
   └─ tmdb_5000_credits.csv
```

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/dev0jha/Moviie.git
   cd Moviie
   ```

2. **(Recommended) Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Run the CLI app:

```bash
python main.py
```

You’ll see a menu with options to:
1. Search & get recommendations
2. Random movie pick
3. Browse top movies
4. Exit

---

## How Recommendations Work (Brief)

The recommender loads movie data from:

- `data/tmdb_5000_movies.csv`

Then it:
1. Uses the **overview** text of each movie
2. Builds TF‑IDF vectors (`TfidfVectorizer(stop_words="english")`)
3. Computes similarity with **cosine similarity**
4. Returns the most similar titles to the movie you entered

---

## Dataset

This repo includes:
- `data/tmdb_5000_movies.csv`
- `data/tmdb_5000_credits.csv`

These files are used as the local dataset source for recommendations (no API key required).

---

## Notes / Troubleshooting

- If a movie title isn’t found, try adjusting spelling/capitalization to match dataset titles.
- The quality of recommendations depends on the richness of the movie **overview** text.

---

## License

Add a license here (e.g., MIT) if you plan to make the repository open-source formally.
