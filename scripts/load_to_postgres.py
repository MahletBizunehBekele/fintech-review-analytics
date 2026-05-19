import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
# =========================
# DATABASE CONNECTION
# =========================

conn = psycopg2.connect(
    host="localhost",
    database="bank_reviews",
    user="postgres",
    password=os.getenv("DB_PASSWORD"),
    port="5432"
)

cursor = conn.cursor()

# =========================
# LOAD CSV
# =========================

df = pd.read_csv("data/raw/analyzed_reviews.csv")

# =========================
# INSERT BANKS
# =========================

banks = [
    ("CBE", "Commercial Bank of Ethiopia Mobile"),
    ("BOA", "Bank of Abyssinia Mobile"),
    ("Dashen", "Dashen Super App")
]

insert_bank_query = """
INSERT INTO banks (bank_name, app_name)
VALUES (%s, %s)
ON CONFLICT DO NOTHING;
"""

for bank in banks:
    cursor.execute(insert_bank_query, bank)

conn.commit()

# =========================
# FETCH BANK IDS
# =========================

cursor.execute("SELECT bank_id, bank_name FROM banks")

bank_mapping = {
    name: bank_id
    for bank_id, name in cursor.fetchall()
}

# =========================
# INSERT REVIEWS
# =========================

insert_review_query = """
INSERT INTO reviews (
    bank_id,
    review_text,
    rating,
    review_date,
    sentiment_label,
    sentiment_score,
    identified_theme,
    source
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():

    cursor.execute(
        insert_review_query,
        (
            bank_mapping[row["bank"]],
            row["review"],
            int(row["rating"]),
            row["date"],
            row["sentiment_label"],
            float(row["sentiment_score"]),
            row["identified_theme"],
            "Google Play"
        )
    )

conn.commit()

print("Data inserted successfully.")

cursor.close()
conn.close()