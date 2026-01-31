import pandas as pd
import matplotlib.pyplot as plt

INPUT_PATH = "data/features/outbreak_flags.csv"

df = pd.read_csv(INPUT_PATH)
df["date"] = pd.to_datetime(df["date"])

# choose one city to demo
demo_city = "Pune"
demo_state = "Maharashtra"

city_df = df[(df["city"] == demo_city) & (df["state"] == demo_state)].copy()
city_df = city_df.sort_values("date")

plt.figure()
plt.plot(city_df["date"], city_df["weighted_symptoms"], marker="o")
plt.title(f"Weighted Symptom Signal - {demo_city}, {demo_state}")
plt.xlabel("Date")
plt.ylabel("Weighted Symptoms")

# mark outbreak points
flagged = city_df[city_df["outbreak_flag"] == 1]
plt.scatter(flagged["date"], flagged["weighted_symptoms"])

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
