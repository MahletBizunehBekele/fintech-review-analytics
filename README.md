# Fintech Review Analytics

## Overview

This project analyzes customer reviews from Ethiopian banking mobile applications using NLP and sentiment analysis techniques.

Banks analyzed:
- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

## Data Collection

Reviews were collected from the Google Play Store using the google-play-scraper library.

Collected fields:
- review text
- rating
- review date
- bank name
- source

A minimum of 400 reviews per bank were targeted.

## Preprocessing

The preprocessing pipeline:
- removed duplicate reviews
- removed missing values
- normalized dates to YYYY-MM-DD format
- removed empty reviews

## Technologies

- Python
- pandas
- google-play-scraper
- GitHub Actions