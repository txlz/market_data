"""
Fundamentals Router
Endpoints for fundamental financial data
"""

from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional

from app.core.y_finance import get_balance_sheet, get_income_statement, get_cashflow

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
        result = get_balance_sheet(symbol, frequency)
        
        if "No balance sheet data" in result:
            raise HTTPException(status_code=404, detail=result)
        
        return {
            "symbol": symbol.upper(),
            "frequency": frequency,
            "data": result
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
        result = get_income_statement(symbol, frequency)
        
        if "No income statement data" in result:
            raise HTTPException(status_code=404, detail=result)
        
        return {
            "symbol": symbol.upper(),
            "frequency": frequency,
            "data": result
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
        result = get_cashflow(symbol, frequency)
        
        if "No cash flow data" in result:
            raise HTTPException(status_code=404, detail=result)
        
        return {
            "symbol": symbol.upper(),
            "frequency": frequency,
            "data": result
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
        balance_sheet = get_balance_sheet(symbol, frequency)
        income_statement = get_income_statement(symbol, frequency)
        cashflow = get_cashflow(symbol, frequency)
        
        return {
            "symbol": symbol.upper(),
            "frequency": frequency,
            "balance_sheet": balance_sheet,
            "income_statement": income_statement,
            "cashflow": cashflow
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving fundamentals: {str(e)}"
        )
