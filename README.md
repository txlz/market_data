# Market Data API

A comprehensive standalone API for financial market data including stock prices, technical indicators, and fundamental data. Built using the TradingAgents yfinance implementation.

## Features

- 📈 **Historical Stock Data**: Get historical price data for any stock symbol
- 📊 **Technical Indicators**: 13+ technical indicators including SMA, EMA, RSI, MACD, Bollinger Bands, and more
- 💰 **Fundamental Data**: Access balance sheets, income statements, and cash flow data
- 🏢 **Company Information**: Detailed company info, insider transactions, and analyst recommendations
- 🚀 **Fast & Reliable**: Built with FastAPI for high performance
- 🐳 **Docker Support**: Easy deployment with Docker and docker-compose

## Quick Start

### Using Docker (Recommended)

```bash
# Build and start the API
docker-compose up -d

# Check if it's running
curl http://localhost:8000/health
```

### Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn app.main:app --reload

# Or run directly
python -m app.main
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the API is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Stock Data

- `GET /api/v1/stock/{symbol}/history` - Get historical stock price data
- `GET /api/v1/stock/{symbol}/info` - Get detailed stock information
- `GET /api/v1/stock/{symbol}/dividends` - Get dividend history

### Technical Indicators

- `GET /api/v1/indicators/{symbol}/{indicator}` - Get specific technical indicator
- `GET /api/v1/indicators/{symbol}/all` - Get all technical indicators
- `GET /api/v1/indicators/list` - List all available indicators

### Fundamentals

- `GET /api/v1/fundamentals/{symbol}/balance-sheet` - Get balance sheet data
- `GET /api/v1/fundamentals/{symbol}/income-statement` - Get income statement
- `GET /api/v1/fundamentals/{symbol}/cashflow` - Get cash flow statement
- `GET /api/v1/fundamentals/{symbol}/all` - Get all fundamental data

### Company Information

- `GET /api/v1/company/{symbol}/info` - Get company information
- `GET /api/v1/company/{symbol}/insider-transactions` - Get insider trades
- `GET /api/v1/company/{symbol}/analyst-recommendations` - Get analyst recommendations

## Usage Examples

### Get Historical Stock Data

```bash
curl "http://localhost:8000/api/v1/stock/AAPL/history?start_date=2024-01-01&end_date=2024-01-31"
```

```python
import requests

response = requests.get(
    "http://localhost:8000/api/v1/stock/AAPL/history",
    params={"start_date": "2024-01-01", "end_date": "2024-01-31"}
)
data = response.json()
print(data)
```

### Get Technical Indicator

```bash
curl "http://localhost:8000/api/v1/indicators/AAPL/close_50_sma?date=2024-01-31&lookback_days=10"
```

```python
import requests

response = requests.get(
    "http://localhost:8000/api/v1/indicators/AAPL/close_50_sma",
    params={"date": "2024-01-31", "lookback_days": 10}
)
data = response.json()
print(data)
```

### Get All Technical Indicators

```bash
curl "http://localhost:8000/api/v1/indicators/AAPL/all?date=2024-01-31&lookback_days=10"
```

### Get Fundamental Data

```bash
curl "http://localhost:8000/api/v1/fundamentals/AAPL/balance-sheet?frequency=quarterly"
```

```python
import requests

response = requests.get(
    "http://localhost:8000/api/v1/fundamentals/AAPL/balance-sheet",
    params={"frequency": "quarterly"}
)
data = response.json()
print(data)
```

### Get Company Information

```bash
curl "http://localhost:8000/api/v1/company/AAPL/info"
```

### List Available Indicators

```bash
curl "http://localhost:8000/api/v1/indicators/list"
```

## Supported Technical Indicators

1. **close_50_sma** - 50-day Simple Moving Average
2. **close_200_sma** - 200-day Simple Moving Average
3. **close_10_ema** - 10-day Exponential Moving Average
4. **macd** - Moving Average Convergence Divergence
5. **macds** - MACD Signal Line
6. **macdh** - MACD Histogram
7. **rsi** - Relative Strength Index
8. **boll** - Bollinger Bands Middle
9. **boll_ub** - Bollinger Bands Upper
10. **boll_lb** - Bollinger Bands Lower
11. **atr** - Average True Range
12. **vwma** - Volume Weighted Moving Average
13. **mfi** - Money Flow Index

Each indicator includes contextual descriptions and usage tips in the API response.

## Docker Commands

```bash
# Start the API
docker-compose up -d

# Stop the API
docker-compose down

# View logs
docker-compose logs -f

# Rebuild after code changes
docker-compose up -d --build

# Check container status
docker-compose ps
```

## Data Caching

The API automatically caches data in the `data_cache/` directory to improve performance and reduce redundant API calls to data providers.

## Configuration

The API uses the TradingAgents configuration system. Key settings are in `app/core/default_config.py`:

- Data cache directory
- Data vendors (yfinance by default)
- Other configuration options

## Error Handling

The API returns standard HTTP status codes:

- `200 OK` - Success
- `400 Bad Request` - Invalid parameters
- `404 Not Found` - Data not found
- `500 Internal Server Error` - Server error

Error responses include detailed messages:

```json
{
  "detail": "No data found for symbol 'INVALID' between 2024-01-01 and 2024-01-31"
}
```

## Development

### Running in Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Running Tests

```bash
# Test with curl
curl http://localhost:8000/health

# Test stock data
curl "http://localhost:8000/api/v1/stock/AAPL/history?start_date=2024-01-01&end_date=2024-01-05"

# Test technical indicators
curl "http://localhost:8000/api/v1/indicators/AAPL/rsi?date=2024-01-31&lookback_days=10"
```

## Requirements

- Python 3.11+
- FastAPI
- yfinance
- pandas
- stockstats

See `requirements.txt` for full list.

## License

This project uses the TradingAgents yfinance implementation.

## Support

For issues or questions, please refer to the API documentation at `/docs` when the server is running.

## Version

Current version: 1.0.0
