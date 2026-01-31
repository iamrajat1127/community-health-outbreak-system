import pandas as pd
import numpy as np

INPUT_PATH = "data/features/city_day_features.csv"
OUTPUT_PATH = "data/features/outbreak_flags.csv"

df = pd.read_csv(INPUT_PATH)
df["date"] = pd.to_datetime(df["date"])

# For each city, compute z-score on weighted_symptoms
def zscore(group):
    x = group["weighted_symptoms"].astype(float)
    mu = x.mean()
    sigma = x.std(ddof=0) if x.std(ddof=0) != 0 else 1.0
    group["z_score"] = (x - mu) / sigma
    group["outbreak_flag"] = (group["z_score"] >= 2.0).astype(int)  # threshold
    return group

df = df.groupby(["city", "state"], group_keys=False).apply(zscore)

df.to_csv(OUTPUT_PATH, index=False)
print(f"Saved outbreak flags to: {OUTPUT_PATH}")
