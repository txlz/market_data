# n8n HTTP Request Nodes - Usage Guide

This guide explains how to use the n8n HTTP request nodes for the Market Data API hosted at `https://market-data-c60q.onrender.com`.

## Quick Start

### 1. Import Nodes into n8n

You can import the node configurations from `n8n-http-request-nodes.json` directly into n8n, or create them manually using the configurations provided.

### 2. Understanding n8n Expressions

The nodes use n8n expressions to dynamically insert values from incoming data:
- `{{ $json.symbol }}` - Gets the symbol from incoming data
- `{{ $json.start_date }}` - Gets the start_date from incoming data
- `{{ $json.lookback_days || 10 }}` - Gets lookback_days or defaults to 10

## Available Endpoints

### Health & Info Endpoints

#### 1. API Root Info
```
GET https://market-data-c60q.onrender.com/
```
No parameters required.

#### 2. Health Check
```
GET https://market-data-c60q.onrender.com/health
```
No parameters required.

---

### Stock Data Endpoints

#### 3. Get Stock History
```
GET https://market-data-c60q.onrender.com/api/v1/stock/{symbol}/history
```
**Required Input Data:**
```json
{
  "symbol": "AAPL",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31"
}
```

#### 4. Get Stock Info
```
GET https://market-data-c60q.onrender.com/api/v1/stock/{symbol}/info
```
**Required Input Data:**
```json
{
  "symbol": "AAPL"
}
```

#### 5. Get Dividends
```
GET https://market-data-c60q.onrender.com/api/v1/stock/{symbol}/dividends
```
**Required Input Data:**
```json
{
  "symbol": "AAPL"
}
```

---

### Technical Indicators Endpoints

#### 6. List All Indicators
```
GET https://market-data-c60q.onrender.com/api/v1/indicators/list
```
No parameters required.

**Available Indicators:**
- close_50_sma (50-day Simple Moving Average)
- close_200_sma (200-day Simple Moving Average)
- close_10_ema (10-day Exponential Moving Average)
- macd (MACD Line)
- macds (MACD Signal Line)
- macdh (MACD Histogram)
- rsi (Relative Strength Index)
- boll (Bollinger Bands Middle)
- boll_ub (Bollinger Bands Upper)
- boll_lb (Bollinger Bands Lower)
- atr (Average True Range)
- vwma (Volume Weighted Moving Average)
- mfi (Money Flow Index)

#### 7. Get Single Indicator
```
GET https://market-data-c60q.onrender.com/api/v1/indicators/{symbol}/{indicator}
```
**Required Input Data:**
```json
{
  "symbol": "AAPL",
  "indicator": "rsi",
  "date": "2024-01-31",
  "lookback_days": 10
}
```
Note: `lookback_days` is optional and defaults to 10.

#### 8. Get All Indicators
```
GET https://market-data-c60q.onrender.com/api/v1/indicators/{symbol}/all
```
**Required Input Data:**
```json
{
  "symbol": "AAPL",
  "date": "2024-01-31",
  "lookback_days": 10
}
```

---

### Fundamentals Endpoints

#### 9. Get Balance Sheet
```
GET https://market-data-c60q.onrender.com/api/v1/fundamentals/{symbol}/balance-sheet
```
**Required Input Data:**
```json
{
  "symbol": "AAPL",
  "frequency": "quarterly"
}
```
Note: `frequency` can be "quarterly" or "annual" (default: quarterly).

#### 10. Get Income Statement
```
GET https://market-data-c60q.onrender.com/api/v1/fundamentals/{symbol}/income-statement
```
**Required Input Data:**
```json
{
  "symbol": "AAPL",
  "frequency": "quarterly"
}
```

#### 11. Get Cash Flow
```
GET https://market-data-c60q.onrender.com/api/v1/fundamentals/{symbol}/cashflow
```
**Required Input Data:**
```json
{
  "symbol": "AAPL",
  "frequency": "quarterly"
}
```

#### 12. Get All Fundamentals
```
GET https://market-data-c60q.onrender.com/api/v1/fundamentals/{symbol}/all
```
**Required Input Data:**
```json
{
  "symbol": "AAPL",
  "frequency": "quarterly"
}
```

---

### Company Information Endpoints

#### 13. Get Company Info
```
GET https://market-data-c60q.onrender.com/api/v1/company/{symbol}/info
```
**Required Input Data:**
```json
{
  "symbol": "AAPL"
}
```

#### 14. Get Insider Transactions
```
GET https://market-data-c60q.onrender.com/api/v1/company/{symbol}/insider-transactions
```
**Required Input Data:**
```json
{
  "symbol": "AAPL"
}
```

#### 15. Get Analyst Recommendations
```
GET https://market-data-c60q.onrender.com/api/v1/company/{symbol}/analyst-recommendations
```
**Required Input Data:**
```json
{
  "symbol": "AAPL"
}
```

---

## Example n8n Workflows

### Example 1: Simple Stock Data Retrieval

```
[Manual Trigger] → [Set Node] → [Get Stock History]
```

**Set Node Configuration:**
```json
{
  "symbol": "AAPL",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31"
}
```

### Example 2: Get All Indicators for Multiple Stocks

```
[Schedule Trigger] → [Set Node] → [Split In Batches] → [Get All Indicators]
```

**Set Node Configuration (Array):**
```json
[
  {
    "symbol": "AAPL",
    "date": "2024-01-31",
    "lookback_days": 14
  },
  {
    "symbol": "MSFT",
    "date": "2024-01-31",
    "lookback_days": 14
  },
  {
    "symbol": "GOOGL",
    "date": "2024-01-31",
    "lookback_days": 14
  }
]
```

### Example 3: Complete Company Analysis

```
[Webhook] → [Get Stock Info] → [Get All Indicators] → [Get All Fundamentals] → [Response]
```

**Webhook Input:**
```json
{
  "symbol": "AAPL",
  "date": "2024-01-31",
  "frequency": "quarterly"
}
```

### Example 4: Daily Technical Analysis Alert

```
[Schedule Trigger (Daily)] → [Set Symbols] → [Loop] → [Get All Indicators] → [IF Node] → [Send Alert]
```

- Check RSI for overbought/oversold conditions
- Check MACD for trend changes
- Send alerts via email/Slack/etc.

---

## Manual Node Configuration

If you prefer to create nodes manually in n8n:

### Basic HTTP Request Node Setup

1. Add an "HTTP Request" node
2. Set the Authentication to "None"
3. Configure the URL with parameters as shown above
4. For query parameters, enable "Send Query Parameters"
5. Add query parameter pairs as needed

### Example: Manual Configuration for "Get Stock History"

**HTTP Request Node Settings:**
- **Method**: GET
- **URL**: `https://market-data-c60q.onrender.com/api/v1/stock/{{ $json.symbol }}/history`
- **Send Query Parameters**: ✓ Enabled
- **Query Parameters**:
  - Name: `start_date`, Value: `{{ $json.start_date }}`
  - Name: `end_date`, Value: `{{ $json.end_date }}`

---

## Tips and Best Practices

1. **Error Handling**: Add "IF" nodes after HTTP requests to handle errors gracefully
2. **Rate Limiting**: Consider adding "Wait" nodes between requests to avoid overwhelming the API
3. **Data Validation**: Use "Set" nodes to validate and format dates before API calls
4. **Caching**: The API has built-in caching, but consider storing results in a database for historical analysis
5. **Date Format**: Always use YYYY-MM-DD format for dates
6. **Stock Symbols**: Use valid ticker symbols (e.g., AAPL, MSFT, GOOGL)

---

## Common Use Cases

### 1. Daily Portfolio Monitoring
```
Schedule Trigger (Daily at market close) 
→ Get list of portfolio stocks
→ Loop through each stock
→ Get Stock History (last 30 days)
→ Get All Indicators
→ Calculate performance metrics
→ Send summary email
```

### 2. Technical Analysis Alerts
```
Schedule Trigger (Every 1 hour during market hours)
→ Get watchlist symbols
→ Get All Indicators
→ Check conditions (RSI < 30 or > 70)
→ Send alert if conditions met
```

### 3. Fundamental Analysis Report
```
Manual Trigger
→ Input stock symbol
→ Get Company Info
→ Get All Fundamentals (Annual)
→ Get Analyst Recommendations
→ Format report
→ Save to database/Send email
```

### 4. Dividend Tracker
```
Schedule Trigger (Weekly)
→ Get dividend stocks list
→ Get Dividends for each
→ Calculate yield
→ Update tracking spreadsheet
```

---

## Troubleshooting

### Common Errors

**Error: No data found for symbol**
- Verify the stock symbol is correct and traded on supported exchanges
- Check date range is valid

**Error: Invalid date format**
- Ensure dates are in YYYY-MM-DD format
- Verify start_date is before end_date

**Error: Unsupported indicator**
- Check the indicator name against the supported list
- Use `/api/v1/indicators/list` to see all available indicators

**Error: Connection timeout**
- The Render.com server may be sleeping (free tier spins down after inactivity)
- First request may take 30-60 seconds to wake up the server
- Add retry logic with exponential backoff

---

## Response Examples

### Stock History Response
```json
{
  "symbol": "AAPL",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "data": "Date,Open,High,Low,Close,Volume\n2024-01-02,185.0,186.5,184.0,185.5,50000000\n..."
}
```

### Single Indicator Response
```json
{
  "symbol": "AAPL",
  "indicator": "rsi",
  "date": "2024-01-31",
  "lookback_days": 10,
  "data": "## rsi values from 2024-01-21 to 2024-01-31:\n\n2024-01-31: 65.4\n2024-01-30: 62.1\n..."
}
```

### Company Info Response
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

---

## Additional Resources

- **API Documentation**: See `API_REFERENCE.md` for complete API details
- **n8n Documentation**: https://docs.n8n.io
- **n8n Community**: https://community.n8n.io

## Support

For API issues or questions, please refer to the API documentation or contact the API maintainer.
