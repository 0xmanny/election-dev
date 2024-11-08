from pathlib import Path

import numpy as np
import pandas as pd

states = [
    "arizona",
    "florida",
    "georgia",
    "michigan",
    "minnesota",
    "nevada",
    "new-hampshire",
    "north-carlonia",
    "pennsylvania",
    "texas",
    "wisconsin",
]

current_dir = Path(__file__).parent


def process_election_data(votes_file, predictions_file):
    votes_df = pd.read_csv(votes_file)
    predictions_df = pd.read_csv(predictions_file)

    state_markets = predictions_df[predictions_df["market"].str.lower().isin(states)]

    national_markets = predictions_df[predictions_df["market"] == "popular"]

    trump_df = votes_df[votes_df["candidate_id"] == "trump-d"].copy()
    trump_df["vote_pct"] = trump_df["votes"] / trump_df["total_votes"]
    trump_df["vote_pct"] = trump_df["vote_pct"].fillna(0)

    market_times = state_markets["timestamp"].unique()
    vote_times = trump_df["timestamp"].unique()
    all_timestamps = np.sort(np.unique(np.concatenate([market_times, vote_times])))

    filled_data = []

    for state in trump_df["state"].unique():
        state_data = trump_df[trump_df["state"] == state].copy()
        if len(state_data) == 0:
            continue

        template = pd.DataFrame({"timestamp": all_timestamps})
        template["state"] = state

        state_filled = pd.merge_asof(
            template, state_data, on="timestamp", by="state", direction="backward"
        )

        filled_data.append(state_filled)

    trump_df_filled = pd.concat(filled_data, ignore_index=True)

    state_markets = state_markets.sort_values(["timestamp"])
    trump_df_filled = trump_df_filled.sort_values(["timestamp"])

    state_results = pd.merge_asof(
        state_markets,
        trump_df_filled,
        left_on="timestamp",
        right_on="timestamp",
        left_by="market",
        right_by="state",
        tolerance=300,
        direction="nearest",
    ).rename(columns={"market": "state", "probability": "market_probability"})

    national_markets = national_markets.sort_values("timestamp")

    national_results = []
    for timestamp in national_markets["timestamp"].unique():
        mask = votes_df["timestamp"] <= timestamp
        current_data = votes_df[mask].copy()

        if len(current_data) > 0:
            latest_state_totals = (
                current_data.sort_values("timestamp")
                .groupby("state")["total_votes"]
                .last()
            )
            total_votes = latest_state_totals.sum()

            trump_votes = (
                current_data[current_data["candidate_id"] == "trump-d"]
                .sort_values("timestamp")
                .groupby("state")["votes"]
                .last()
                .sum()
            )

            vote_pct = trump_votes / total_votes if total_votes > 0 else 0

            market_rows = national_markets[national_markets["timestamp"] == timestamp]

            for _, market_row in market_rows.iterrows():
                result_row = {
                    "timestamp": timestamp,
                    "market": market_row["market"],
                    "market_probability": market_row["probability"],
                    "votes": int(trump_votes),
                    "total_votes": int(total_votes),
                    "vote_pct": float(vote_pct),
                }
                national_results.append(result_row)

    national_results_df = pd.DataFrame(national_results)

    return state_results, national_results_df


def process_winner_data(predictions_file):
    predictions_df = pd.read_csv(predictions_file)
    winner_market = predictions_df[predictions_df["market"] == "winner"]
    return winner_market


def process_btc_data(btc_file):
    btc_df = pd.read_csv(btc_file)
    btc_df["timestamp"] = pd.to_datetime(btc_df["timestamp"])
    btc_df["timestamp"] = btc_df["timestamp"].astype("int64") // 10**9
    return btc_df


def get_time_boundaries(state_df, national_df):
    start_time = max(state_df["timestamp"].min(), national_df["timestamp"].min())
    end_time = min(state_df["timestamp"].max(), national_df["timestamp"].max())
    return start_time, end_time


def adjust_granularity(df, start_time, end_time, minutes=15):
    df = df.loc[:, ~df.columns.duplicated()]
    df = df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]
    df = df.copy()

    df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")
    start_dt = pd.to_datetime(start_time, unit="s")
    end_dt = pd.to_datetime(end_time, unit="s")

    time_range = pd.date_range(start=start_dt, end=end_dt, freq=f"{minutes}min")
    time_df = pd.DataFrame(
        {"datetime": time_range, "timestamp": time_range.astype("int64") // 10**9}
    )

    if "state" in df.columns:
        results = []
        for state in df["state"].unique():
            state_df = df[df["state"] == state].copy()

            template = time_df.copy()

            state_result = pd.merge_asof(
                template, state_df, on="timestamp", direction="backward"
            )

            results.append(state_result)

        result = pd.concat(results)
    else:
        result = pd.merge_asof(time_df, df, on="timestamp", direction="backward")

    for col in result.columns:
        if "datetime" in col:
            result.drop(col, axis=1, inplace=True)

    return result


if __name__ == "__main__":
    votes_file = current_dir / "nyt/parsed.csv"
    predictions_file = current_dir / "polymarket/parsed.csv"
    binance_file = current_dir / "binance/parsed.csv"

    state_results, national_results = process_election_data(
        votes_file, predictions_file
    )
    state_results = state_results.iloc[:, 1:]
    winner_results = process_winner_data(predictions_file)
    btc_data = process_btc_data(binance_file)

    start_time, end_time = get_time_boundaries(state_results, national_results)

    state_results_adjusted = adjust_granularity(
        state_results, start_time, end_time, minutes=15
    )
    national_results_adjusted = adjust_granularity(
        national_results, start_time, end_time, minutes=15
    )
    btc_data_adjusted = adjust_granularity(btc_data, start_time, end_time, minutes=15)
    winner_adjusted = adjust_granularity(
        winner_results, start_time, end_time, minutes=15
    )

    state_times = set(state_results_adjusted["timestamp"])
    national_times = set(national_results_adjusted["timestamp"])
    assert (
        state_times == national_times
    ), "Timestamp mismatch between state and national results"

    state_results_adjusted.to_csv(
        current_dir / "transformed/state_results.csv", index=False
    )
    national_results_adjusted.to_csv(
        current_dir / "transformed/national_results.csv", index=False
    )
    state_results_adjusted.to_json(
        current_dir / "transformed/state_results.json",
        orient="records",
        index=False,
        indent=2,
    )
    national_results_adjusted.to_json(
        current_dir / "transformed/national_results.json",
        orient="records",
        index=False,
        indent=2,
    )
    btc_data_adjusted.to_csv(current_dir / "transformed/btc_data.csv", index=False)
    btc_data_adjusted.to_json(
        current_dir / "transformed/btc_data.json",
        orient="records",
        index=False,
        indent=2,
    )
    winner_adjusted.to_csv(current_dir / "transformed/winner_results.csv", index=False)
    winner_adjusted.to_json(
        current_dir / "transformed/winner_results.json",
        orient="records",
        index=False,
        indent=2,
    )