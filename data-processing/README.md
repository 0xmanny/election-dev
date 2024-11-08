# Election Data Collection and Analysis

This project collects and processes election data from New York Times and Polymarket to analyze prediction market probabilities and voting data for the 2024 US Presidential Election.

## Directory Structure

```
data/
├── binance/        # Crypto market data
│   ├── raw/        # Raw data files
│   ├── parse.py    # Klines data parser
│   ├── parsed.csv  # Processed BTC price data
├── tranformed/     # Final processed datasets
├── nyt/            # New York Times election data
│   ├── raw/        # Raw data files
│   ├── parse.py    # NYT data parser
│   ├── parsed.csv  # Processed NYT data
│   └── collect.py  # NYT data collector
├── polymarket/     # Prediction market data
│   ├── raw/        # Raw data files
│   ├── parse.py    # Polymarket data parser
│   ├── parsed.csv  # Processed market data
│   └── collect.py   # Market data collector
├── pyproject.toml
├── README.md
├── requirements.txt
└── transform.py    # Data transformations on parsed datasets
```

## Data Sources

### New York Times Election Data

- Includes vote counts, estimated participation percentages, and state-level statistics
- Parsed and stored in standardized CSV format

### Polymarket Prediction Data

- Tracks state-level win probabilities, popular vote, and electoral winner markets
- Historical prediction market probabilities **for Trump markets only**
  - It was slightly annoying (and manual) to find the marketIds
  - Due to lack of time other markets were not collected
  - This means the prediction market data represents prediction odds for only for Trump
  - It's reasonable to assume the compliment is Kamala though it isn't 100% accurate

### Binance BTC Data

- Downloaded spot BTC/USDT data from [binance.vision](https://data.binance.vision/)

## Data Processing Pipeline

1. **Data Collection** (`collect.py`)

   - Collects NYT election results
   - Collects Polymarket probabilities
   - Raw data stored in respective `raw/` directories

2. **Parsing** (`parse.py`)

   - Raw JSON data cleaned and standardized
   - Timestamps normalized to Unix epoch
   - Data validated and formatted consistently

3. **Transformation** (`transform.py`)
   - Merges election results with prediction market data
   - Adjusts data granularity to reduce size
   - Generates state-level and national-level analyses
   - Produces final datasets for visualization

## Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Collect raw data:

```bash
python nyt/collect.py
python polymarket/collect.py
```

3. Parse raw data:

```bash
python nyt/parse.py
python polymarket/parse.py
python binance/parse.py
```

4. Transform and merge data:

```bash
python transform.py
```

## Output Files

- `state_results.csv`: State-level election results with market probabilities
- `national_results.csv`: Odds of trump winning popular vote on Polymarket
- `winner_results.csv`: Odds of trump winner election on Polymarket
- `btc_data.csv`: BTC prices when polls closed
- JSON versions of the above files are also available

## Data Frequency

- NYT election data: Not 100% sure, think it's when AP releases
- Polymarket data: Every 1 minute
- Binance: 1 minute
- Final transformed data: 15-minute intervals to reduce size

## Notes

- Timestamps are in Unix epoch format (seconds since 1970)
- Vote percentages calculated from raw vote counts
- Forward-filling used for missing data points
- Market probabilities interpolated to match election result timestamps

## Requirements

See `requirements.txt` for complete list of Python dependencies.

## Contributing

Please submit discussions, issues, and pull requests for any feedback.

Before opening a PR, please run the following commands to ensure code quality:

```bash
black .
```
