import pandas as pd
import json

OUTBREAK_REPORT = "data/features/outbreak_report.csv"
CITY_LATLON = "data/raw/city_latlon.csv"
OUTPUT_JSON = "data/features/map_outbreaks.json"

outbreaks = pd.read_csv(OUTBREAK_REPORT)
cities = pd.read_csv(CITY_LATLON)

merged = outbreaks.merge(cities, on=["city","state"], how="left")

# drop rows without coordinates (for now)
merged = merged.dropna(subset=["lat","lon"])

records = merged[["date","city","state","lat","lon","z_score","intensity","weighted_symptoms","weighted_diseases"]].to_dict(orient="records")

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2)

print("Saved map json:", OUTPUT_JSON)

########################################################################################################################

# import pandas as pd
# import json
# import os

# OUTBREAK_REPORT = "data/features/outbreak_report.csv"
# CITY_LATLON = "data/raw/city_latlon.csv"
# OUTPUT_JSON = "data/features/map_outbreaks.json"

# print("Reading:", OUTBREAK_REPORT)
# outbreaks = pd.read_csv(OUTBREAK_REPORT)

# print("Rows in outbreak_report:", len(outbreaks))
# if len(outbreaks) == 0:
#     print("❌ outbreak_report.csv is empty (no flagged outbreaks).")
#     exit()

# print("Reading:", CITY_LATLON)
# cities = pd.read_csv(CITY_LATLON)

# # normalize strings to avoid mismatch
# for col in ["city", "state"]:
#     outbreaks[col] = outbreaks[col].astype(str).str.strip().str.lower()
#     cities[col] = cities[col].astype(str).str.strip().str.lower()

# merged = outbreaks.merge(cities, on=["city", "state"], how="left")

# missing_coords = merged["lat"].isna().sum()
# print("Rows missing coordinates after merge:", missing_coords, "out of", len(merged))

# # show which cities are missing coordinates
# if missing_coords > 0:
#     missing = merged[merged["lat"].isna()][["city", "state"]].drop_duplicates()
#     print("\nCities missing lat/lon in city_latlon.csv:\n", missing.to_string(index=False))

# merged = merged.dropna(subset=["lat", "lon"])

# records = merged[["date","city","state","lat","lon","z_score","intensity","weighted_symptoms","weighted_diseases"]].to_dict(orient="records")

# with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
#     json.dump(records, f, indent=2)

# print("\n✅ Saved JSON:", OUTPUT_JSON)
# print("✅ Absolute path:", os.path.abspath(OUTPUT_JSON))
# print("✅ Records written:", len(records))
