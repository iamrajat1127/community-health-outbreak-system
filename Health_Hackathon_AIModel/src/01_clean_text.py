import json
import re
import pandas as pd

INPUT_PATH = "data/raw/synthetic_health_chats.json"
OUTPUT_PATH = "data/cleaned/cleaned_chats.csv"

def clean_text(t: str) -> str:
    t = t.lower()
    t = re.sub(r"http\\S+", "", t)          # remove urls
    t = re.sub(r"[^a-z0-9\\s,.!?]", " ", t) # keep basic punctuation
    t = re.sub(r"\\s+", " ", t).strip()
    return t

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)
df["cleaned_text"] = df["text"].apply(clean_text)

df.to_csv(OUTPUT_PATH, index=False)
print(f"Saved cleaned data to: {OUTPUT_PATH}")
