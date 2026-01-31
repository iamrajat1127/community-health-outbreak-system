import pandas as pd

INPUT_PATH = "data/cleaned/cleaned_chats.csv"
OUTPUT_PATH = "data/enriched/enriched_chats.csv"

# Simple keyword dictionaries (prototype)
SYMPTOMS = {
    "fever": ["fever", "high fever", "temperature"],
    "cough": ["cough", "dry cough"],
    "sore_throat": ["sore throat", "throat pain"],
    "headache": ["headache"],
    "joint_pain": ["joint pain", "body ache", "bodyache"],
    "rash": ["rash", "rashes"],
    "diarrhea": ["diarrhea", "loose motions", "loose motion"],
    "vomiting": ["vomiting", "throwing up"],
    "fatigue": ["tired", "fatigue", "weak"],
    "chills": ["chills", "shivering"]
}

DISEASES = {
    "dengue": ["dengue", "ns1"],
    "malaria": ["malaria"],
    "chikungunya": ["chikungunya"],
    "typhoid": ["typhoid"],
    "covid": ["covid", "coronavirus"],
    "tuberculosis": ["tb", "tuberculosis"],
    "gastroenteritis": ["gastroenteritis", "stomach infection"],
    "h1n1_swine_flu": ["swine flu", "h1n1"],
    "jaundice": ["jaundice"],
    "seasonal_flu": ["viral flu", "flu"]
}

def contains_any(text: str, keywords: list[str]) -> bool:
    return any(k in text for k in keywords)

df = pd.read_csv(INPUT_PATH)

# symptom flags
for s, keys in SYMPTOMS.items():
    df[f"symptom_{s}"] = df["cleaned_text"].astype(str).apply(lambda x: int(contains_any(x, keys)))

# disease flags
for d, keys in DISEASES.items():
    df[f"disease_{d}"] = df["cleaned_text"].astype(str).apply(lambda x: int(contains_any(x, keys)))

# trust weight: verified higher than unverified
df["trust_weight"] = df["section"].apply(lambda x: 1.0 if x == "verified" else 0.4)

df.to_csv(OUTPUT_PATH, index=False)
print(f"Saved enriched data to: {OUTPUT_PATH}")
