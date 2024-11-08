import pandas as pd
import os
from pathlib import Path

current_dir = Path(__file__).parent


def process_binance_data(filename):
    columns = [
        "open_timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_timestamp",
        "ignore_1",
        "ignore_2",
        "ignore_3",
        "ignore_4",
        "ignore_5",
    ]

    df = pd.read_csv(filename, header=None, names=columns)

    df["open_timestamp"] = pd.to_datetime(df["open_timestamp"], unit="ms")
    df["close_timestamp"] = pd.to_datetime(df["close_timestamp"], unit="ms")

    return df


dfs = []

for filename in os.listdir(current_dir / "raw"):
    dfs.append(process_binance_data(current_dir / f"raw/{filename}"))

combined_df = pd.concat(dfs, ignore_index=True)
combined_df["price"] = (combined_df["open"] + combined_df["close"]) / 2
combined_df["timestamp"] = combined_df["open_timestamp"]
combined_df = combined_df[["timestamp", "price"]]
combined_df.to_csv("parsed.csv", index=False)
