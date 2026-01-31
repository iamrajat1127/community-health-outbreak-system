import json
import pandas as pd

with open("data/raw/synthetic_health_chats.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)
df.to_csv("data/raw/synthetic_health_chats.csv", index=False)

print("CSV file created successfully!")
