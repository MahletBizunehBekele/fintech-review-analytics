import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/raw/analyzed_reviews.csv")

plt.style.use("default")

bank_sentiment = (
    df.groupby(["bank", "sentiment_label"])
    .size()
    .unstack(fill_value=0)
)

bank_sentiment.plot(
    kind="bar",
    figsize=(8,5),
    edgecolor="black"
)

plt.title("Sentiment Distribution by Bank")

plt.xlabel("Bank")

plt.ylabel("Number of Reviews")

plt.xticks(rotation=0)

plt.legend(title="Sentiment")

plt.tight_layout()

plt.savefig("outputs/sentiment_by_bank.png")

plt.close()

plt.figure(figsize=(8,5))

for bank in df["bank"].unique():

    subset = df[df["bank"] == bank]

    plt.hist(
        subset["rating"],
        bins=5,
        alpha=0.6,
        label=bank
    )

plt.title("Rating Distribution by Bank")

plt.xlabel("Star Rating")

plt.ylabel("Frequency")

plt.legend()

plt.tight_layout()

plt.savefig("outputs/rating_distribution.png")

plt.close()


theme_counts = (
    df["identified_theme"]
    .value_counts()
)

plt.figure(figsize=(8,5))

theme_counts.plot(
    kind="barh",
    edgecolor="black"
)

plt.title("Theme Frequency Distribution")

plt.xlabel("Number of Reviews")

plt.ylabel("Theme")

plt.tight_layout()

plt.savefig("outputs/theme_frequency.png")

plt.close()


avg_rating = (
    df.groupby("bank")["rating"]
    .mean()
)

plt.figure(figsize=(6,4))

avg_rating.plot(
    kind="bar",
    edgecolor="black"
)

plt.title("Average Rating by Bank")

plt.xlabel("Bank")

plt.ylabel("Average Rating")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig("outputs/average_rating.png")

plt.close()