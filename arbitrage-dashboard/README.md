# Dhan NSE BSE Arbitrage Dashboard

A real-time arbitrage opportunity scanner for NSE and BSE markets using Dhan API.

## Features

- Real-time price comparison between NSE and BSE
- Arbitrage opportunity detection with profit calculations
- Live market data integration via Dhan API
- Interactive dashboard with filtering and sorting
- Risk analysis and position sizing recommendations

## Prerequisites

- Dhan trading account and API access
- Python 3.8+
- Required dependencies (see requirements.txt)

## Installation

```bash
git clone <repository-url>
cd dhan-arbitrage-dashboard
pip install -r requirements.txt
```

## Configuration

1. Create `.env` file:
```
DHAN_CLIENT_ID=your_client_id
DHAN_ACCESS_TOKEN=your_access_token
```

2. Configure stock watchlist in `config.json`

## Usage

```bash
python app.py
```

Access dashboard at `http://localhost:5000`

## Key Metrics

- **Price Spread**: Difference between NSE and BSE prices
- **Arbitrage %**: Percentage profit opportunity
- **Volume**: Trading volumes on both exchanges
- **Liquidity Score**: Ease of execution rating

## Risk Warnings

- Consider transaction costs and taxes
- Monitor liquidity before executing trades
- Market timing is crucial for arbitrage success
- Use proper position sizing

## Support

For issues or feature requests, create an issue in the repository.

## Disclaimer

This tool is for educational purposes. Trading involves risk. Users are responsible for their trading decisions.
