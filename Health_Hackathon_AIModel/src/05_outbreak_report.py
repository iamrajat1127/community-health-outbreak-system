# import pandas as pd

# INPUT_PATH = "data/features/outbreak_flags.csv"
# OUTPUT_PATH = "data/features/outbreak_report.csv"

# df = pd.read_csv(INPUT_PATH)
# df["date"] = pd.to_datetime(df["date"])

# # keep only flagged rows
# outbreaks = df[df["outbreak_flag"] == 1].copy()

# # sort by strongest signal first
# outbreaks = outbreaks.sort_values(["z_score"], ascending=False)

# # add intensity bucket for UI colors
# def intensity(z):
#     if z >= 4: return "red"
#     if z >= 3: return "orange"
#     if z >= 2: return "yellow"
#     return "green"

# outbreaks["intensity"] = outbreaks["z_score"].apply(intensity)

# outbreaks.to_csv(OUTPUT_PATH, index=False)
# print("Saved outbreak report:", OUTPUT_PATH)

# print("\nTop flagged outbreaks:\n")
# print(outbreaks[["date","city","state","weighted_symptoms","weighted_diseases","z_score","intensity"]].head(20))

###########################################################################################################################

import pandas as pd

INPUT_PATH = "data/features/outbreak_flags.csv"
OUTPUT_PATH = "data/features/outbreak_report.csv"

df = pd.read_csv(INPUT_PATH)
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# add intensity bucket for UI colors
def intensity(z):
    if z >= 4: return "red"
    if z >= 3: return "orange"
    if z >= 2: return "yellow"
    return "green"

df["intensity"] = df["z_score"].apply(intensity)

# First try: real flagged outbreaks
outbreaks = df[df["outbreak_flag"] == 1].copy()

if len(outbreaks) == 0:
    print(" No outbreak_flag==1 rows found. Creating a prototype report using TOP z_score rows instead.")
    # Take top suspicious rows (helps prototype even with small data)
    outbreaks = df.sort_values("z_score", ascending=False).head(25).copy()
    outbreaks["outbreak_flag"] = 1  # mark them for prototype/demo

# sort by strongest signal first
outbreaks = outbreaks.sort_values("z_score", ascending=False)

outbreaks.to_csv(OUTPUT_PATH, index=False)
print(" Saved outbreak report:", OUTPUT_PATH)
print(outbreaks[["date","city","state","weighted_symptoms","weighted_diseases","z_score","outbreak_flag","intensity"]].head(15))
