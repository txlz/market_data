"""
Technical Indicators Router
Endpoints for technical analysis indicators
"""

from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional
from datetime import datetime
from enum import Enum

from app.core.y_finance import get_stock_stats_indicators_window
from app.core.json_utils import parse_indicator_string

router = APIRouter()

# Enum for technical indicators (creates dropdown in docs)
class TechnicalIndicator(str, Enum):
    """Available technical indicators"""
    close_50_sma = "close_50_sma"
    close_200_sma = "close_200_sma"
    close_10_ema = "close_10_ema"
    macd = "macd"
    macds = "macds"
    macdh = "macdh"
    rsi = "rsi"
    boll = "boll"
    boll_ub = "boll_ub"
    boll_lb = "boll_lb"
    atr = "atr"
    vwma = "vwma"
    mfi = "mfi"

# List of supported indicators
SUPPORTED_INDICATORS = [ind.value for ind in TechnicalIndicator]

@router.get("/{symbol}/all")
async def get_all_indicators(
    symbol: str = Path(..., description="Stock ticker symbol"),
    date: str = Query(..., description="Analysis date in YYYY-MM-DD format"),
    lookback_days: int = Query(10, ge=1, le=365, description="Number of days to look back")
):
    """
    Get all technical indicators for a stock
    
    - **symbol**: Stock ticker symbol (e.g., AAPL, MSFT)
    - **date**: Analysis date in YYYY-MM-DD format
    - **lookback_days**: Number of days to look back (1-365, default: 10)
    
    Returns: All available technical indicators for the symbol
    """
    try:
        # Validate date format
        datetime.strptime(date, "%Y-%m-%d")
        
        results = {}
        errors = {}
        
        for indicator in SUPPORTED_INDICATORS:
            try:
                result = get_stock_stats_indicators_window(
                    symbol, indicator, date, lookback_days
                )
                # Parse the string result into structured JSON
                parsed_result = parse_indicator_string(result)
                results[indicator] = parsed_result
            except Exception as e:
                errors[indicator] = str(e)
        
        return {
            "symbol": symbol.upper(),
            "date": date,
            "lookback_days": lookback_days,
            "total_indicators": len(results),
            "indicators": results,
            "errors": errors if errors else None
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error retrieving indicators: {str(e)}"
        )

@router.get("/{symbol}/{indicator}")
async def get_technical_indicator(
    symbol: str = Path(..., description="Stock ticker symbol"),
    indicator: TechnicalIndicator = Path(..., description="Technical indicator name"),
    date: str = Query(..., description="Analysis date in YYYY-MM-DD format"),
    lookback_days: int = Query(10, ge=1, le=365, description="Number of days to look back")
):
    """
    Get technical indicator values for a stock
    
    - **symbol**: Stock ticker symbol (e.g., AAPL, MSFT)
    - **indicator**: Technical indicator name (e.g., close_50_sma, rsi, macd)
    - **date**: Analysis date in YYYY-MM-DD format
    - **lookback_days**: Number of days to look back (1-365, default: 10)
    
    **Supported Indicators:**
    - close_50_sma: 50-day Simple Moving Average
    - close_200_sma: 200-day Simple Moving Average
    - close_10_ema: 10-day Exponential Moving Average
    - macd: Moving Average Convergence Divergence
    - macds: MACD Signal Line
    - macdh: MACD Histogram
    - rsi: Relative Strength Index
    - boll: Bollinger Bands Middle
    - boll_ub: Bollinger Bands Upper
    - boll_lb: Bollinger Bands Lower
    - atr: Average True Range
    - vwma: Volume Weighted Moving Average
    - mfi: Money Flow Index
    
    Returns: Indicator values for the specified time period with description
    """
    try:
        # Validate date format
        datetime.strptime(date, "%Y-%m-%d")
        
        result = get_stock_stats_indicators_window(
            symbol, indicator.value, date, lookback_days
        )
        
        if not result:
            raise HTTPException(
                status_code=404, 
                detail=f"No data found for {indicator} on {symbol}"
            )
        
        # Parse the string result into structured JSON
        parsed_result = parse_indicator_string(result)
        
        return {
            "symbol": symbol.upper(),
            "indicator": indicator.value,
            "date": date,
            "lookback_days": lookback_days,
            "total_values": len(parsed_result.get("values", [])),
            "header": parsed_result.get("header", ""),
            "description": parsed_result.get("description", ""),
            "values": parsed_result.get("values", [])
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error retrieving indicator {indicator}: {str(e)}"
        )
