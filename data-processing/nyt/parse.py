import json
from datetime import datetime, timezone
import os
from pathlib import Path

CANDIDATES = set(["harris-k", "trump-d"])

current_dir = Path(__file__).parent


def parse_candidate_data(candidate):
    votes = candidate.get("votes", {}).get("total", 0)
    if votes is None:
        votes = 0

    nyt_id = candidate.get("nyt_id", "")

    estimates = candidate.get("nyt_model_estimates", {})
    if estimates:
        votes_estimated = estimates.get("votes_estimated", 0)
        win_probability = estimates.get("win_probability", 0)
        ranking = estimates.get("ranking", None)
        party = estimates.get("party_caucus", "")
    else:
        votes_estimated = 0
        win_probability = 0
        ranking = None
        party = ""

    return {
        "candidate_id": nyt_id,
        "votes": votes,
        "votes_estimated": votes_estimated,
        "win_probability": win_probability,
        "ranking": ranking,
        "party": party,
    }


def parse_snapshot(json_data, state):
    dt = datetime.strptime(
        json_data["greatest_updated_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
    ).replace(tzinfo=timezone.utc)
    timestamp = int(dt.timestamp())

    total_votes = json_data["total_votes"]
    eevp = json_data["eevp"]

    model_estimates = json_data.get("nyt_model_estimates", {})
    total_votes_estimated = model_estimates.get("votes_estimated", 0)
    total_votes_remaining = model_estimates.get("votes_remaining", 0)

    rows = []
    for candidate in json_data["candidates"]:

        if candidate["nyt_id"] not in CANDIDATES:
            continue

        candidate_data = parse_candidate_data(candidate)

        row = {
            "timestamp": timestamp,
            "state": state,
            "total_votes": total_votes,
            "total_votes_estimated": total_votes_estimated,
            "total_votes_remaining": total_votes_remaining,
            "eevp": eevp,
            **candidate_data,
        }
        rows.append(row)

    return rows


def parse_state_data(data, state):
    rows = []

    ts = data["timeseries"]
    key = list(ts.keys())[0]
    for snapshot in ts[key]:
        snapshot_rows = parse_snapshot(snapshot, state)
        rows.extend(snapshot_rows)

    return rows


def convert_to_csv_format(rows):
    csv_rows = []
    headers = [
        "timestamp",
        "state",
        "candidate_id",
        "party",
        "votes",
        "votes_estimated",
        "win_probability",
        "ranking",
        "total_votes",
        "total_votes_estimated",
        "total_votes_remaining",
        "eevp",
    ]

    csv_rows.append(headers)
    for row in rows:
        csv_row = [str(row.get(header, "")) for header in headers]
        csv_rows.append(csv_row)

    return csv_rows


if __name__ == "__main__":
    all_states = []

    for filename in os.listdir(current_dir / "raw"):
        state = filename.split("_")[0]
        with open(current_dir / f"raw/{filename}", "r") as f:
            state_data = json.load(f)
            parsed_state_data = parse_state_data(state_data, state)
            all_states.extend(parsed_state_data)

    csv_data = convert_to_csv_format(all_states)

    with open(current_dir / "parsed.csv", "w") as f:
        for row in csv_data:
            f.write(",".join(row) + "\n")
