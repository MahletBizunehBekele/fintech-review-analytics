from google_play_scraper import reviews, Sort
import pandas as pd

apps = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "Dashen": "com.dashen.dashensuperapp"
}

all_reviews = []

for bank, app_id in apps.items():

    print(f"Scraping reviews for {bank}...")

    result, _ = reviews(
        app_id,
        lang="en",
        country="et",
        sort=Sort.NEWEST,
        count=500
    )

    print(f"Collected {len(result)} reviews.")

    for r in result:

        all_reviews.append({
            "review": r["content"],
            "rating": r["score"],
            "date": r["at"].strftime("%Y-%m-%d"),
            "bank": bank,
            "source": "Google Play"
        })

df = pd.DataFrame(all_reviews)

print("\nBefore preprocessing:")
print(df.shape)

# remove duplicates
df.drop_duplicates(subset=["review"], inplace=True)

# remove missing values
df.dropna(subset=["review", "rating"], inplace=True)

# remove empty reviews
df = df[df["review"].str.strip() != ""]

print("\nAfter preprocessing:")
print(df.shape)

print(df.head())

# save cleaned dataset
df.to_csv("data/raw/bank_reviews_clean.csv", index=False)

print("\nClean dataset saved successfully.")