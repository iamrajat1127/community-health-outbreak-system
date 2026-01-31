import pandas as pd

ENRICHED_PATH = "data/enriched/enriched_chats.csv"

df = pd.read_csv(ENRICHED_PATH)

symptom_cols = [c for c in df.columns if c.startswith("symptom_")]
disease_cols = [c for c in df.columns if c.startswith("disease_")]

df["timestamp"] = pd.to_datetime(df["timestamp"])

# choose a city/date you saw flagged
city = "Pune"
state = "Maharashtra"
date = "2023-08-13"

day_df = df[
    (df["city"] == city) &
    (df["state"] == state) &
    (df["timestamp"].dt.date.astype(str) == date)
].copy()

print(f"\n--- Top signals for {city}, {state} on {date} ---\n")

if len(day_df) == 0:
    print("No messages found for that city/date.")
else:
    symptom_sum = day_df[symptom_cols].sum().sort_values(ascending=False)
    disease_sum = day_df[disease_cols].sum().sort_values(ascending=False)

    print("Top symptoms:")
    print(symptom_sum.head(10))

    print("\nTop disease mentions:")
    print(disease_sum.head(10))

    print("\nSample messages:")
    print(day_df["text"].head(5).to_string(index=False))
