"""
Fundamentals Router
Endpoints for fundamental financial data
"""

from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional
import yfinance as yf

from app.core.y_finance import get_balance_sheet, get_income_statement, get_cashflow
from app.core.json_utils import financial_statement_to_json

router = APIRouter()

@router.get("/{symbol}/balance-sheet")
async def get_balance_sheet_data(
    symbol: str = Path(..., description="Stock ticker symbol"),
    frequency: str = Query("quarterly", regex="^(annual|quarterly)$", description="Data frequency")
):
    """
    Get balance sheet data for a stock
    
    - **symbol**: Stock ticker symbol (e.g., AAPL, MSFT)
    - **frequency**: Data frequency - 'annual' or 'quarterly' (default: quarterly)
    
    Returns: Balance sheet data including assets, liabilities, and equity
    """
    try:
        # Get data directly from yfinance to convert to JSON
        ticker_obj = yf.Ticker(symbol.upper())
        
        if frequency.lower() == "quarterly":
            data = ticker_obj.quarterly_balance_sheet
        else:
            data = ticker_obj.balance_sheet
            
        if data.empty:
            raise HTTPException(status_code=404, detail=f"No balance sheet data found for symbol '{symbol}'")
        
        # Convert to structured JSON
        data_json = financial_statement_to_json(data)
        
        return {
            "symbol": symbol.upper(),
            "frequency": frequency,
            "periods": list(data_json.keys()),
            "data": data_json
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving balance sheet: {str(e)}"
        )

@router.get("/{symbol}/income-statement")
async def get_income_statement_data(
    symbol: str = Path(..., description="Stock ticker symbol"),
    frequency: str = Query("quarterly", regex="^(annual|quarterly)$", description="Data frequency")
):
    """
    Get income statement data for a stock
    
    - **symbol**: Stock ticker symbol (e.g., AAPL, MSFT)
    - **frequency**: Data frequency - 'annual' or 'quarterly' (default: quarterly)
    
    Returns: Income statement data including revenue, expenses, and net income
    """
    try:
        # Get data directly from yfinance to convert to JSON
        ticker_obj = yf.Ticker(symbol.upper())
        
        if frequency.lower() == "quarterly":
            data = ticker_obj.quarterly_income_stmt
        else:
            data = ticker_obj.income_stmt
            
        if data.empty:
            raise HTTPException(status_code=404, detail=f"No income statement data found for symbol '{symbol}'")
        
        # Convert to structured JSON
        data_json = financial_statement_to_json(data)
        
        return {
            "symbol": symbol.upper(),
            "frequency": frequency,
            "periods": list(data_json.keys()),
            "data": data_json
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving income statement: {str(e)}"
        )

@router.get("/{symbol}/cashflow")
async def get_cashflow_data(
    symbol: str = Path(..., description="Stock ticker symbol"),
    frequency: str = Query("quarterly", regex="^(annual|quarterly)$", description="Data frequency")
):
    """
    Get cash flow statement data for a stock
    
    - **symbol**: Stock ticker symbol (e.g., AAPL, MSFT)
    - **frequency**: Data frequency - 'annual' or 'quarterly' (default: quarterly)
    
    Returns: Cash flow statement data including operating, investing, and financing activities
    """
    try:
        # Get data directly from yfinance to convert to JSON
        ticker_obj = yf.Ticker(symbol.upper())
        
        if frequency.lower() == "quarterly":
            data = ticker_obj.quarterly_cashflow
        else:
            data = ticker_obj.cashflow
            
        if data.empty:
            raise HTTPException(status_code=404, detail=f"No cash flow data found for symbol '{symbol}'")
        
        # Convert to structured JSON
        data_json = financial_statement_to_json(data)
        
        return {
            "symbol": symbol.upper(),
            "frequency": frequency,
            "periods": list(data_json.keys()),
            "data": data_json
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving cash flow: {str(e)}"
        )

@router.get("/{symbol}/all")
async def get_all_fundamentals(
    symbol: str = Path(..., description="Stock ticker symbol"),
    frequency: str = Query("quarterly", regex="^(annual|quarterly)$", description="Data frequency")
):
    """
    Get all fundamental financial statements for a stock
    
    - **symbol**: Stock ticker symbol (e.g., AAPL, MSFT)
    - **frequency**: Data frequency - 'annual' or 'quarterly' (default: quarterly)
    
    Returns: All fundamental financial statements (balance sheet, income statement, cash flow)
    """
    try:
        # Get data directly from yfinance
        ticker_obj = yf.Ticker(symbol.upper())
        
        if frequency.lower() == "quarterly":
            bs_data = ticker_obj.quarterly_balance_sheet
            is_data = ticker_obj.quarterly_income_stmt
            cf_data = ticker_obj.quarterly_cashflow
        else:
            bs_data = ticker_obj.balance_sheet
            is_data = ticker_obj.income_stmt
            cf_data = ticker_obj.cashflow
        
        # Convert to structured JSON
        balance_sheet_json = financial_statement_to_json(bs_data) if not bs_data.empty else {}
        income_statement_json = financial_statement_to_json(is_data) if not is_data.empty else {}
        cashflow_json = financial_statement_to_json(cf_data) if not cf_data.empty else {}
        
        return {
            "symbol": symbol.upper(),
            "frequency": frequency,
            "balance_sheet": {
                "periods": list(balance_sheet_json.keys()),
                "data": balance_sheet_json
            },
            "income_statement": {
                "periods": list(income_statement_json.keys()),
                "data": income_statement_json
            },
            "cashflow": {
                "periods": list(cashflow_json.keys()),
                "data": cashflow_json
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving fundamentals: {str(e)}"
        )
