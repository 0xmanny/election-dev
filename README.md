# election-dev

Historical analysis of market developments during the 2024 presidential election. The data is collected from the NYT, Polymarket, and Binance.

## Overview

This project helps users understand the relationship between political events and market movements by:

- Tracking prediction market probabilities for election outcomes
- Correlating preliminary results with prediction market shifts and bitcoins price

## Data Sources

- **New York Times**: Political news and election coverage
- **Polymarket**: Prediction market data for election outcomes
- **Binance**: Cryptocurrency market data

For detailed information about the data collection methodology and transformations, see [data processing documentation](https://github.com/0xmanny/election-dev/tree/master/data-processing/README.md).

## Getting Started

### Prerequisites

```bash
python >= 3.8
node >= 14.0.0
```

### Installation

1. Clone the repository

```bash
git clone https://github.com/0xmanny/election-dev.git
cd election-dev
```

2. Install dependencies

```bash
cd data-processing
pip install -r requirements.txt

cd ../website
pnpm install
```

## Usage

To run the development server:

```bash
pnpm run dev
```

Visit [http://localhost:3000](http://localhost:3000) to view the application.

## Deployment

The platform is deployed at [election.dev](https://election.dev/).
