# Market Data API Reference

Complete API reference for all endpoints.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required.

## Response Format

All responses are in JSON format with the following structure:

### Success Response
```json
{
  "symbol": "AAPL",
  "data": "..."
}
```

### Error Response
```json
{
  "detail": "Error message here"
}
```

## Status Codes

- `200 OK` - Request successful
- `400 Bad Request` - Invalid parameters
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Endpoints

### Root & Health

#### GET /

Get API information

**Response:**
```json
{
  "name": "Market Data API",
  "version": "1.0.0",
  "description": "Financial market data API",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

#### GET /health

Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-31T12:00:00",
  "version": "1.0.0"
}
```

---

### Stock Data Endpoints

#### GET /api/v1/stock/{symbol}/history

Get historical stock price data

**Parameters:**
- `symbol` (path, required): Stock ticker symbol
- `start_date` (query, required): Start date (YYYY-MM-DD)
- `end_date` (query, required): End date (YYYY-MM-DD)

**Example:**
```bash
GET /api/v1/stock/AAPL/history?start_date=2024-01-01&end_date=2024-01-31
```

**Response:**
```json
{
  "symbol": "AAPL",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "data": "CSV formatted data..."
}
```

#### GET /api/v1/stock/{symbol}/info

Get detailed stock information

**Parameters:**
- `symbol` (path, required): Stock ticker symbol

**Example:**
```bash
GET /api/v1/stock/AAPL/info
```

**Response:**
```json
{
  "symbol": "AAPL",
  "info": {
    "shortName": "Apple Inc.",
    "sector": "Technology",
    "industry": "Consumer Electronics",
    ...
  }
}
```

#### GET /api/v1/stock/{symbol}/dividends

Get dividend history

**Parameters:**
- `symbol` (path, required): Stock ticker symbol

**Example:**
```bash
GET /api/v1/stock/AAPL/dividends
```

---

### Technical Indicators Endpoints

#### GET /api/v1/indicators/list

List all available technical indicators with descriptions

**Example:**
```bash
GET /api/v1/indicators/list
```

**Response:**
```json
{
  "total": 13,
  "indicators": {
    "close_50_sma": "50 SMA: A medium-term trend indicator...",
    "rsi": "RSI: Measures momentum to flag overbought/oversold conditions...",
    ...
  }
}
```

#### GET /api/v1/indicators/{symbol}/{indicator}

Get specific technical indicator values

**Parameters:**
- `symbol` (path, required): Stock ticker symbol
- `indicator` (path, required): Indicator name
- `date` (query, required): Analysis date (YYYY-MM-DD)
- `lookback_days` (query, optional): Days to look back (1-365, default: 10)

**Supported Indicators:**
- close_50_sma
- close_200_sma
- close_10_ema
- macd
- macds
- macdh
- rsi
- boll
- boll_ub
- boll_lb
- atr
- vwma
- mfi

**Example:**
```bash
GET /api/v1/indicators/AAPL/rsi?date=2024-01-31&lookback_days=10
```

**Response:**
```json
{
  "symbol": "AAPL",
  "indicator": "rsi",
  "date": "2024-01-31",
  "lookback_days": 10,
  "data": "## rsi values from 2024-01-21 to 2024-01-31:\n\n2024-01-31: 65.4\n..."
}
```

#### GET /api/v1/indicators/{symbol}/all

Get all technical indicators for a symbol

**Parameters:**
- `symbol` (path, required): Stock ticker symbol
- `date` (query, required): Analysis date (YYYY-MM-DD)
- `lookback_days` (query, optional): Days to look back (1-365, default: 10)

**Example:**
```bash
GET /api/v1/indicators/AAPL/all?date=2024-01-31&lookback_days=10
```

**Response:**
```json
{
  "symbol": "AAPL",
  "date": "2024-01-31",
  "lookback_days": 10,
  "indicators": {
    "close_50_sma": "data...",
    "rsi": "data...",
    ...
  },
  "errors": null
}
```

---

### Fundamentals Endpoints

#### GET /api/v1/fundamentals/{symbol}/balance-sheet

Get balance sheet data

**Parameters:**
- `symbol` (path, required): Stock ticker symbol
- `frequency` (query, optional): 'annual' or 'quarterly' (default: quarterly)

**Example:**
```bash
GET /api/v1/fundamentals/AAPL/balance-sheet?frequency=quarterly
```

**Response:**
```json
{
  "symbol": "AAPL",
  "frequency": "quarterly",
  "data": "CSV formatted balance sheet data..."
}
```

#### GET /api/v1/fundamentals/{symbol}/income-statement

Get income statement data

**Parameters:**
- `symbol` (path, required): Stock ticker symbol
- `frequency` (query, optional): 'annual' or 'quarterly' (default: quarterly)

**Example:**
```bash
GET /api/v1/fundamentals/AAPL/income-statement?frequency=quarterly
```

#### GET /api/v1/fundamentals/{symbol}/cashflow

Get cash flow statement data

**Parameters:**
- `symbol` (path, required): Stock ticker symbol
- `frequency` (query, optional): 'annual' or 'quarterly' (default: quarterly)

**Example:**
```bash
GET /api/v1/fundamentals/AAPL/cashflow?frequency=quarterly
```

#### GET /api/v1/fundamentals/{symbol}/all

Get all fundamental financial statements

**Parameters:**
- `symbol` (path, required): Stock ticker symbol
- `frequency` (query, optional): 'annual' or 'quarterly' (default: quarterly)

**Example:**
```bash
GET /api/v1/fundamentals/AAPL/all?frequency=quarterly
```

**Response:**
```json
{
  "symbol": "AAPL",
  "frequency": "quarterly",
  "balance_sheet": "data...",
  "income_statement": "data...",
  "cashflow": "data..."
}
```

---

### Company Information Endpoints

#### GET /api/v1/company/{symbol}/info

Get detailed company information

**Parameters:**
- `symbol` (path, required): Stock ticker symbol

**Example:**
```bash
GET /api/v1/company/AAPL/info
```

**Response:**
```json
{
  "symbol": "AAPL",
  "company_info": {
    "Company Name": "Apple Inc.",
    "Industry": "Consumer Electronics",
    "Sector": "Technology",
    "Country": "United States",
    "Website": "https://www.apple.com"
  }
}
```

#### GET /api/v1/company/{symbol}/insider-transactions

Get insider transaction data

**Parameters:**
- `symbol` (path, required): Stock ticker symbol

**Example:**
```bash
GET /api/v1/company/AAPL/insider-transactions
```

**Response:**
```json
{
  "symbol": "AAPL",
  "data": "CSV formatted insider transaction data..."
}
```

#### GET /api/v1/company/{symbol}/analyst-recommendations

Get analyst recommendations

**Parameters:**
- `symbol` (path, required): Stock ticker symbol

**Example:**
```bash
GET /api/v1/company/AAPL/analyst-recommendations
```

**Response:**
```json
{
  "symbol": "AAPL",
  "majority_recommendation": "Buy",
  "vote_count": 25
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. However, the underlying data provider (Yahoo Finance) may have their own rate limits.

## Data Caching

The API automatically caches responses to improve performance. Cached data is stored in the `data_cache/` directory.

## Error Examples

### Invalid Symbol
```json
{
  "detail": "No data found for symbol 'INVALID' between 2024-01-01 and 2024-01-31"
}
```

### Invalid Date Format
```json
{
  "detail": "Invalid date format: time data '2024-13-01' does not match format '%Y-%m-%d'"
}
```

### Unsupported Indicator
```json
{
  "detail": "Unsupported indicator 'invalid_indicator'. Supported indicators: close_50_sma, close_200_sma, ..."
}
```

## Python Client Example

```python
import requests

class MarketDataClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def get_stock_history(self, symbol, start_date, end_date):
        response = requests.get(
            f"{self.base_url}/api/v1/stock/{symbol}/history",
            params={"start_date": start_date, "end_date": end_date}
        )
        return response.json()
    
    def get_indicator(self, symbol, indicator, date, lookback_days=10):
        response = requests.get(
            f"{self.base_url}/api/v1/indicators/{symbol}/{indicator}",
            params={"date": date, "lookback_days": lookback_days}
        )
        return response.json()
    
    def get_fundamentals(self, symbol, statement_type, frequency="quarterly"):
        response = requests.get(
            f"{self.base_url}/api/v1/fundamentals/{symbol}/{statement_type}",
            params={"frequency": frequency}
        )
        return response.json()

# Usage
client = MarketDataClient()
data = client.get_stock_history("AAPL", "2024-01-01", "2024-01-31")
print(data)
```

## Notes

- All dates should be in `YYYY-MM-DD` format
- Stock symbols should be valid ticker symbols (e.g., AAPL, MSFT, GOOGL)
- The API uses the TradingAgents yfinance implementation for data retrieval
- Technical indicator descriptions are included in indicator responses
- Error messages are descriptive to help with troubleshooting
