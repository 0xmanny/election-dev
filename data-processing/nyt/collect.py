import json
import time
from pathlib import Path

import requests

STATES = [
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New-Hampshire",
    "New-Jersey",
    "New-Mexico",
    "New-York",
    "North-Carolina",
    "North-Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode-Island",
    "South-Carolina",
    "South-Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West-Virginia",
    "Wisconsin",
    "Wyoming",
]

current_dir = Path(__file__).parent


def scrape_election_data():
    data_dir = current_dir / "raw"
    data_dir.mkdir(exist_ok=True)

    done_states = []

    for state in STATES:
        try:
            state = state.lower()
            url = f"https://static01.nyt.com/elections-assets/pages/data/2024-11-05/results-{state}-president.json"

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            filename = data_dir / f"{state}_results.json"
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)

            print(f"Data for {state} saved")
            done_states.append(state)

        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data for {state}. {e}")
            break

        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON for {state}. {e}")
            break

        except Exception as e:
            print(f"Unexpected error for {state}. {e}")
            break


if __name__ == "__main__":
    print("Starting election data scraping...")
    scrape_election_data()
    print("Scraping complete. Check the election_data directory for results.")
    print("Scraping complete. Check the election_data directory for results.")
