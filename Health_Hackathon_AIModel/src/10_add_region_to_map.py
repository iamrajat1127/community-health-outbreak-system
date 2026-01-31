import pandas as pd
import json

MAP_PATH = "data/features/map_outbreaks.json"
STATE_REGION = "data/raw/state_to_region.csv"
OUT_PATH = "data/features/map_outbreaks_with_region.json"

regions = pd.read_csv(STATE_REGION)
regions["state_norm"] = regions["state"].astype(str).str.strip().str.lower()

with open(MAP_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

for r in data:
    st = str(r["state"]).strip().lower()
    match = regions[regions["state_norm"] == st]
    r["region"] = match["region"].iloc[0] if len(match) else "Unknown"

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Saved:", OUT_PATH)
