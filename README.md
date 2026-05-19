# Customer Experience Analytics for Ethiopian Fintech Apps

> **Omega Consultancy** | Analyst: Mahlet Bekele | May 2026

A end-to-end NLP pipeline that scrapes Google Play Store reviews for three Ethiopian banks — **CBE**, **BOA**, and **Dashen** — performs sentiment and thematic analysis, stores results in PostgreSQL, and produces stakeholder-ready insights and visualizations.

---

## Project Structure

```
.
├── data/
│   └── raw/                        # CSV files (git-ignored)
├── scripts/
│   ├── scrape_reviews.py           # Task 1: Google Play scraper
│   ├── sentiment_theme_analysis.py # Task 2: Sentiment + theme pipeline
│   ├── load_to_postgres.py         # Task 3: PostgreSQL ingestion
│   └── visualizations.py           # Task 4: Matplotlib charts
├── sql/
│   ├── schema.sql                  # DB schema (DDL)
│   └── verification_queries.sql    # Data integrity checks
├── outputs/                        # Generated plots
├── reports/
│   └── Omega_Consultancy_Final_Report.pdf
├── .github/
│   └── workflows/
│       └── unittests.yml           # CI/CD pipeline
├── requirements.txt
└── README.md
```

---

## Quickstart

### 1. Clone & install dependencies

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Scrape reviews

```bash
python scripts/scrape_reviews.py
# Output: data/raw/bank_reviews_clean.csv
```

### 3. Run sentiment & thematic analysis

```bash
python scripts/sentiment_theme_analysis.py
# Output: data/raw/analyzed_reviews.csv
```

### 4. Set up PostgreSQL database

**Prerequisites:** PostgreSQL installed and running locally.

```bash
# Create the database
psql -U postgres -c "CREATE DATABASE bank_reviews;"

# Apply schema
psql -U postgres -d bank_reviews -f sql/schema.sql
```

Create a `.env` file in the project root:

```
DB_PASSWORD=your_postgres_password
```

### 5. Load data into PostgreSQL

```bash
python scripts/load_to_postgres.py
# Inserts all reviews with correct bank_id foreign keys
```

### 6. Verify data integrity

```bash
psql -U postgres -d bank_reviews -f sql/verification_queries.sql
```

Expected results:

| Bank   | Review Count | Avg Rating |
|--------|-------------|------------|
| CBE    | ~790        | ~3.85 ★    |
| BOA    | ~585        | ~3.00 ★    |
| Dashen | ~445        | ~3.97 ★    |

### 7. Generate visualizations

```bash
python scripts/visualizations.py
# Saves PNG charts to outputs/
```

---

## Database Schema

### Entity Relationship

```
banks (1) ──────< reviews (many)
bank_id (PK)         review_id (PK)
bank_name            bank_id (FK → banks.bank_id)
app_name             review_text
                     rating
                     review_date
                     sentiment_label
                     sentiment_score
                     identified_theme
                     source
```

### `banks` table

| Column    | Type         | Constraint  | Description                    |
|-----------|--------------|-------------|--------------------------------|
| bank_id   | SERIAL       | PRIMARY KEY | Auto-incrementing surrogate key |
| bank_name | VARCHAR(100) | NOT NULL    | Short name (CBE, BOA, Dashen)  |
| app_name  | VARCHAR(200) | NOT NULL    | Full Google Play app name      |

### `reviews` table

| Column           | Type         | Constraint             | Description                        |
|------------------|--------------|------------------------|------------------------------------|
| review_id        | SERIAL       | PRIMARY KEY            | Auto-incrementing surrogate key    |
| bank_id          | INTEGER      | FK → banks(bank_id)    | Links review to bank               |
| review_text      | TEXT         | NOT NULL               | Raw review content                 |
| rating           | INTEGER      | NOT NULL               | Star rating (1–5)                  |
| review_date      | DATE         | NOT NULL               | Review submission date (YYYY-MM-DD)|
| sentiment_label  | VARCHAR(20)  |                        | POSITIVE / NEGATIVE / NEUTRAL      |
| sentiment_score  | FLOAT        |                        | DistilBERT confidence score (0–1)  |
| identified_theme | VARCHAR(100) |                        | Assigned theme from keyword match  |
| source           | VARCHAR(50)  |                        | Data origin (Google Play)          |

---

## Pipeline Overview

| Task | Description                         | Key Tools                              | Status  |
|------|-------------------------------------|----------------------------------------|---------|
| 1    | Data collection & preprocessing     | google-play-scraper, pandas            | ✅ Done |
| 2    | Sentiment & thematic analysis       | DistilBERT, spaCy, TF-IDF              | ✅ Done |
| 3    | PostgreSQL database engineering     | psycopg2, python-dotenv                | ✅ Done |
| 4    | Insights, visualizations & report   | Matplotlib, ReportLab                  | ✅ Done |

---

## Environment Variables

| Variable      | Description                     |
|---------------|---------------------------------|
| `DB_PASSWORD` | PostgreSQL password for postgres user |

Store in a `.env` file (never commit this file — it is git-ignored).

---

## Notes

- `data/` is listed in `.gitignore` — CSV files are never committed to the repository.
- All scripts are idempotent: re-running `load_to_postgres.py` uses `ON CONFLICT DO NOTHING` to avoid duplicate bank entries.
- Review text is truncated to 512 tokens before DistilBERT inference to comply with model sequence limits.
- See `reports/Omega_Consultancy_Final_Report.pdf` for the full stakeholder report.