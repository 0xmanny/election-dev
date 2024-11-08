import os
import json
from pathlib import Path

headers = "market,timestamp,probability"
combined = []

current_dir = Path(__file__).parent

for filename in os.listdir(current_dir / "raw"):
    market = filename.split(".")[0]
    with open(current_dir / f"raw/{filename}") as f:
        data = json.load(f)

    parsed_data = []
    for entry in data.get("history"):
        timestamp, probability = entry.get("t"), entry.get("p")
        parsed_data.append(f"{market},{timestamp},{probability}")

    combined.extend(parsed_data)

with open(current_dir / "parsed.csv", "w") as f:
    f.write(headers + "\n")
    for line in combined:
        f.write(line + "\n")
