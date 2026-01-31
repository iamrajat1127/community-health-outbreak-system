import pandas as pd

INPUT_PATH = "data/enriched/enriched_chats.csv"
OUTPUT_PATH = "data/features/city_day_features.csv"

df = pd.read_csv(INPUT_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

symptom_cols = [c for c in df.columns if c.startswith("symptom_")]
disease_cols  = [c for c in df.columns if c.startswith("disease_")]

# Weighted symptom & disease counts
for c in symptom_cols + disease_cols:
    df[c] = df[c] * df["trust_weight"]

agg = df.groupby(["city", "state", df["timestamp"].dt.date]).agg(
    total_msgs=("chat_id", "count"),
    weighted_symptoms=(symptom_cols[0], "sum"),
).reset_index()

# add total weighted symptom sum across all symptom columns
agg["weighted_symptoms"] = df.groupby(["city", "state", df["timestamp"].dt.date])[symptom_cols].sum().sum(axis=1).values
agg["weighted_diseases"] = df.groupby(["city", "state", df["timestamp"].dt.date])[disease_cols].sum().sum(axis=1).values

agg.rename(columns={"timestamp": "date"}, inplace=True)

agg.to_csv(OUTPUT_PATH, index=False)
print(f"Saved features to: {OUTPUT_PATH}")
