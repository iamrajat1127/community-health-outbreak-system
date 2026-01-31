import pandas as pd
import json

ENRICHED_PATH = "data/enriched/enriched_chats.csv"
OUTBREAKS_PATH = "data/features/map_outbreaks.json"
OUTPUT_PATH = "data/features/city_date_explanations.json"

df = pd.read_csv(ENRICHED_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df["date"] = df["timestamp"].dt.date.astype(str)

# normalize for matching
df["city_norm"] = df["city"].astype(str).str.strip().str.lower()
df["state_norm"] = df["state"].astype(str).str.strip().str.lower()

symptom_cols = [c for c in df.columns if c.startswith("symptom_")]
disease_cols = [c for c in df.columns if c.startswith("disease_")]

# Load map outbreaks so we only build explanations for points you show on the map
with open(OUTBREAKS_PATH, "r", encoding="utf-8") as f:
    outbreaks = json.load(f)

explanations = {}

for r in outbreaks:
    city = str(r["city"]).strip().lower()
    state = str(r["state"]).strip().lower()
    date = str(r["date"])

    key = f"{city}|{state}|{date}"

    day_df = df[(df["city_norm"] == city) & (df["state_norm"] == state) & (df["date"] == date)].copy()
    if len(day_df) == 0:
        explanations[key] = {
            "top_symptoms": [],
            "top_diseases": [],
            "sample_messages": [],
            "note": "No messages found for this city/date in enriched_chats.csv"
        }
        continue

    # Sum weighted signals (already weighted in your enriched step)
    symptom_sum = day_df[symptom_cols].sum().sort_values(ascending=False)
    disease_sum = day_df[disease_cols].sum().sort_values(ascending=False)

    top_symptoms = [(s.replace("symptom_", ""), float(v)) for s, v in symptom_sum.head(8).items() if v > 0]
    top_diseases = [(d.replace("disease_", ""), float(v)) for d, v in disease_sum.head(6).items() if v > 0]

    # Sample messages (keep original text)
    sample_messages = day_df["text"].dropna().astype(str).head(5).tolist()

    explanations[key] = {
        "top_symptoms": top_symptoms,
        "top_diseases": top_diseases,
        "sample_messages": sample_messages
    }

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(explanations, f, indent=2)

print("Saved explanations JSON:", OUTPUT_PATH)
print("Example keys:", list(explanations.keys())[:5])
