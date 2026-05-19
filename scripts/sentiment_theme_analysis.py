from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import spacy
import re

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("data/raw/bank_reviews_clean.csv")

# create review ids
df.reset_index(inplace=True)
df.rename(columns={"index": "review_id"}, inplace=True)

# =========================
# LOAD SPACY
# =========================

nlp = spacy.load("en_core_web_sm")

# =========================
# TEXT PREPROCESSING
# =========================

def preprocess_text(text):

    text = str(text).lower()

    # remove special chars
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    doc = nlp(text)

    tokens = []

    for token in doc:

        if token.is_stop:
            continue

        if token.is_punct:
            continue

        if len(token.text.strip()) == 0:
            continue

        tokens.append(token.lemma_)

    return " ".join(tokens)

df["cleaned_review"] = df["review"].apply(preprocess_text)

print("Text preprocessing complete.")

# =========================
# SENTIMENT ANALYSIS
# =========================

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

labels = []
scores = []

for text in df["review"]:

    try:

        result = classifier(text[:512])[0]

        score = result["score"]
        label = result["label"]

        # create neutral threshold
        if score < 0.60:
            label = "NEUTRAL"

        labels.append(label)
        scores.append(score)

    except:

        labels.append("NEUTRAL")
        scores.append(0.0)

df["sentiment_label"] = labels
df["sentiment_score"] = scores

print("Sentiment analysis complete.")

# =========================
# TF-IDF KEYWORD EXTRACTION
# =========================

vectorizer = TfidfVectorizer(
    max_features=50,
    ngram_range=(1,2)
)

X = vectorizer.fit_transform(df["cleaned_review"])

keywords = vectorizer.get_feature_names_out()

print("\nTop Keywords:")
print(keywords)

# =========================
# THEME DEFINITIONS
# =========================

themes = {

    "Login Issues": [
        "login",
        "password",
        "otp",
        "authenticate",
        "signin"
    ],

    "Performance": [
        "slow",
        "crash",
        "freeze",
        "load",
        "bug"
    ],

    "Transactions": [
        "transfer",
        "payment",
        "transaction",
        "send"
    ],

    "UI/UX": [
        "interface",
        "design",
        "easy",
        "navigation",
        "ui"
    ],

    "Customer Support": [
        "support",
        "service",
        "help",
        "response"
    ]
}

# =========================
# THEME ASSIGNMENT
# =========================

def assign_theme(text):

    text = str(text).lower()

    for theme, words in themes.items():

        for word in words:

            if word in text:
                return theme

    return "Other"

df["identified_theme"] = df["cleaned_review"].apply(assign_theme)

print("Theme assignment complete.")

# =========================
# SENTIMENT BY BANK
# =========================
import matplotlib.pyplot as plt
bank_sentiment = (
    df.groupby(["bank", "sentiment_label"])
    .size()
    .unstack(fill_value=0)
)

bank_sentiment.plot(
    kind="bar",
    figsize=(8,5)
)

plt.title("Sentiment Distribution by Bank")

plt.xlabel("Bank")

plt.ylabel("Number of Reviews")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig("sentiment_by_bank.png")

print("Bank sentiment visualization saved.")

# =========================
# SAVE RESULTS
# =========================

final_df = df[
    [
        "review_id",
        "bank",
        "review",
        "rating",
        "date",
        "sentiment_label",
        "sentiment_score",
        "identified_theme"
    ]
]

final_df.to_csv(
    "data/raw/analyzed_reviews.csv",
    index=False
)

print("\nAnalysis complete.")
print(final_df.head())


print("\nSentiment by Bank:")
print(
    df.groupby("bank")["sentiment_score"].mean()
)

print("\nThemes:")
print(
    df["identified_theme"].value_counts()
)


sentiment_counts = df["sentiment_label"].value_counts()
plt.figure(figsize=(6,4))
sentiment_counts.plot(kind="bar")
plt.title("Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")
plt.tight_layout()
plt.savefig("sentiment_distribution.png")
print("Visualization saved.")