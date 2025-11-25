"""
Stock Data Router
Endpoints for historical stock price data
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime

from app.core.y_finance import get_YFin_data_online
from app.core.yfin_utils import YFinanceUtils
from app.core.json_utils import csv_to_json, dataframe_to_json

router = APIRouter()

@router.get("/{symbol}/history")
async def get_stock_history(
    symbol: str,
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format")
):
    """
    Get historical stock price data for a symbol
    
    - **symbol**: Stock ticker symbol (e.g., AAPL, MSFT)
    - **start_date**: Start date in YYYY-MM-DD format
    - **end_date**: End date in YYYY-MM-DD format
    
    Returns: CSV formatted stock data with Open, High, Low, Close, Volume
    """
    try:
        # Validate date format
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
        
        result = get_YFin_data_online(symbol, start_date, end_date)
        
        if "No data found" in result:
            raise HTTPException(status_code=404, detail=result)
        
        # Convert CSV to JSON
        data_json = csv_to_json(result)
        
        return {
            "symbol": symbol.upper(),
            "start_date": start_date,
            "end_date": end_date,
            "total_records": len(data_json),
            "data": data_json
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving stock data: {str(e)}")

@router.get("/{symbol}/info")
async def get_stock_info(symbol: str):
    """
    Get detailed stock information including company details
    
    - **symbol**: Stock ticker symbol (e.g., AAPL, MSFT)
    
    Returns: Comprehensive stock information including company name, sector, industry, etc.
    """
    try:
        info = YFinanceUtils.get_stock_info(symbol)
        
        if not info:
            raise HTTPException(status_code=404, detail=f"No information found for symbol '{symbol}'")
        
        return {
            "symbol": symbol.upper(),
            "info": info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving stock info: {str(e)}")

@router.get("/{symbol}/dividends")
async def get_stock_dividends(symbol: str):
    """
    Get dividend history for a stock
    
    - **symbol**: Stock ticker symbol (e.g., AAPL, MSFT)
    
    Returns: Dividend payment history
    """
    try:
        dividends = YFinanceUtils.get_stock_dividends(symbol)
        
        if dividends.empty:
            raise HTTPException(status_code=404, detail=f"No dividend data found for symbol '{symbol}'")
        
        # Convert DataFrame to JSON
        dividends_json = dataframe_to_json(dividends)
        
        return {
            "symbol": symbol.upper(),
            "total_dividends": len(dividends_json),
            "dividends": dividends_json
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving dividends: {str(e)}")
