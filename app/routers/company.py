"""
Company Router
Endpoints for company information and insider data
"""

from fastapi import APIRouter, HTTPException, Path

from app.core.y_finance import get_insider_transactions
from app.core.yfin_utils import YFinanceUtils

router = APIRouter()

@router.get("/{symbol}/info")
async def get_company_info(symbol: str = Path(..., description="Stock ticker symbol")):
    """
    Get detailed company information
    
    - **symbol**: Stock ticker symbol (e.g., AAPL, MSFT)
    
    Returns: Company details including name, sector, industry, country, website, etc.
    """
    try:
        info = YFinanceUtils.get_company_info(symbol)
        
        if info.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No company information found for symbol '{symbol}'"
            )
        
        return {
            "symbol": symbol.upper(),
            "company_info": info.to_dict('records')[0]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving company info: {str(e)}"
        )

@router.get("/{symbol}/insider-transactions")
async def get_insider_trades(symbol: str = Path(..., description="Stock ticker symbol")):
    """
    Get insider transaction data for a stock
    
    - **symbol**: Stock ticker symbol (e.g., AAPL, MSFT)
    
    Returns: Recent insider trading activity including purchases and sales
    """
    try:
        result = get_insider_transactions(symbol)
        
        if "No insider transactions data" in result:
            raise HTTPException(status_code=404, detail=result)
        
        return {
            "symbol": symbol.upper(),
            "data": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving insider transactions: {str(e)}"
        )

@router.get("/{symbol}/analyst-recommendations")
async def get_analyst_recommendations(symbol: str = Path(..., description="Stock ticker symbol")):
    """
    Get analyst recommendations for a stock
    
    - **symbol**: Stock ticker symbol (e.g., AAPL, MSFT)
    
    Returns: Latest analyst recommendations and ratings
    """
    try:
        recommendation, count = YFinanceUtils.get_analyst_recommendations(symbol)
        
        if recommendation is None:
            raise HTTPException(
                status_code=404,
                detail=f"No analyst recommendations found for symbol '{symbol}'"
            )
        
        return {
            "symbol": symbol.upper(),
            "majority_recommendation": recommendation,
            "vote_count": int(count)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving analyst recommendations: {str(e)}"
        )
