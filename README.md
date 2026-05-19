# Fintech Review Analytics

## Overview

This project analyzes customer reviews from Ethiopian banking mobile applications to uncover customer satisfaction drivers, recurring complaints, and feature requests using NLP and sentiment analysis techniques. The project simulates a real-world fintech analytics workflow for Omega Consultancy, supporting data-driven product recommendations for Ethiopian banks.

Banks analyzed:
- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

---

## Data Collection

Reviews were collected from the Google Play Store using the `google-play-scraper` Python library.

Collected fields:
- review text
- star rating (1–5)
- review date
- bank name
- review source

The scraping pipeline targeted a minimum of 400 reviews per bank. Reviews were collected using the `Sort.NEWEST` option to capture recent customer feedback.

---

## Preprocessing

The preprocessing pipeline:
- removed duplicate reviews
- removed rows with missing review text or ratings
- filtered empty reviews
- normalized dates to `YYYY-MM-DD` format
- serialized the cleaned dataset into CSV format

The cleaned dataset is excluded from Git version control through `.gitignore`.

---

## Sentiment and Thematic Analysis

Sentiment analysis was performed using the Hugging Face transformer model:

```python
distilbert-base-uncased-finetuned-sst-2-english