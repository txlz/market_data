"""
Comprehensive API Testing Script
Tests all Market Data API endpoints and saves results to JSON files
"""

import requests
import json
from datetime import datetime, timedelta
import os
import time

# Configuration
BASE_URL = "http://localhost:8000"
SYMBOL = "AAPL"  # Test symbol
OUTPUT_DIR = "test_results"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_json(data, filename):
    """Save data to JSON file"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved: {filename}")

def test_endpoint(name, url, params=None):
    """Test an API endpoint and return the response"""
    try:
        print(f"\nTesting: {name}")
        print(f"URL: {url}")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"✓ Success: {name}")
        return {"success": True, "data": data, "status_code": response.status_code}
    except requests.exceptions.RequestException as e:
        print(f"✗ Error: {name} - {str(e)}")
        return {"success": False, "error": str(e), "status_code": getattr(e.response, 'status_code', None)}

def main():
    print("=" * 70)
    print("Market Data API - Comprehensive Test Suite")
    print("=" * 70)
    print(f"Base URL: {BASE_URL}")
    print(f"Test Symbol: {SYMBOL}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print("=" * 70)
    
    # Check if API is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        response.raise_for_status()
        print("\n✓ API is running and healthy")
    except:
        print("\n✗ ERROR: API is not running!")
        print(f"Please start the API server first:")
        print(f"  cd {os.path.dirname(os.path.abspath(__file__))}")
        print(f"  uvicorn app.main:app --reload")
        return
    
    # Calculate dates for testing
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    analysis_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    all_results = {
        "test_metadata": {
            "timestamp": datetime.now().isoformat(),
            "symbol": SYMBOL,
            "base_url": BASE_URL,
            "test_dates": {
                "start_date": start_date,
                "end_date": end_date,
                "analysis_date": analysis_date
            }
        },
        "endpoints": {}
    }
    
    # =================================================================
    # 1. TECHNICAL INDICATORS
    # =================================================================
    print("\n" + "=" * 70)
    print("1. TESTING TECHNICAL INDICATORS")
    print("=" * 70)
    
    # Test individual indicators
    indicators = [
        "close_50_sma", "close_200_sma", "close_10_ema",
        "macd", "macds", "macdh",
        "rsi", "boll", "boll_ub", "boll_lb",
        "atr", "vwma", "mfi"
    ]
    
    indicators_results = {}
    
    for indicator in indicators:
        result = test_endpoint(
            f"Technical Indicator: {indicator}",
            f"{BASE_URL}/api/v1/indicators/{SYMBOL}/{indicator}",
            params={"date": analysis_date, "lookback_days": 10}
        )
        indicators_results[indicator] = result
        time.sleep(0.5)  # Small delay to avoid overwhelming the API
    
    save_json(indicators_results, "technical_indicators_individual.json")
    all_results["endpoints"]["technical_indicators_individual"] = indicators_results
    
    # Test all indicators at once
    result = test_endpoint(
        "All Technical Indicators",
        f"{BASE_URL}/api/v1/indicators/{SYMBOL}/all",
        params={"date": analysis_date, "lookback_days": 10}
    )
    save_json(result, "technical_indicators_all.json")
    all_results["endpoints"]["technical_indicators_all"] = result
    
    # Test indicators list
    result = test_endpoint(
        "Indicators List",
        f"{BASE_URL}/api/v1/indicators/list"
    )
    save_json(result, "indicators_list.json")
    all_results["endpoints"]["indicators_list"] = result
    
    # =================================================================
    # 2. STOCK DATA
    # =================================================================
    print("\n" + "=" * 70)
    print("2. TESTING STOCK DATA")
    print("=" * 70)
    
    # Historical data
    result = test_endpoint(
        "Stock History",
        f"{BASE_URL}/api/v1/stock/{SYMBOL}/history",
        params={"start_date": start_date, "end_date": end_date}
    )
    save_json(result, "stock_history.json")
    all_results["endpoints"]["stock_history"] = result
    
    # Stock info
    result = test_endpoint(
        "Stock Info",
        f"{BASE_URL}/api/v1/stock/{SYMBOL}/info"
    )
    save_json(result, "stock_info.json")
    all_results["endpoints"]["stock_info"] = result
    
    # Dividends
    result = test_endpoint(
        "Stock Dividends",
        f"{BASE_URL}/api/v1/stock/{SYMBOL}/dividends"
    )
    save_json(result, "stock_dividends.json")
    all_results["endpoints"]["stock_dividends"] = result
    
    # =================================================================
    # 3. FUNDAMENTALS
    # =================================================================
    print("\n" + "=" * 70)
    print("3. TESTING FUNDAMENTALS")
    print("=" * 70)
    
    # Balance Sheet - Quarterly
    result = test_endpoint(
        "Balance Sheet (Quarterly)",
        f"{BASE_URL}/api/v1/fundamentals/{SYMBOL}/balance-sheet",
        params={"frequency": "quarterly"}
    )
    save_json(result, "balance_sheet_quarterly.json")
    all_results["endpoints"]["balance_sheet_quarterly"] = result
    
    # Balance Sheet - Annual
    result = test_endpoint(
        "Balance Sheet (Annual)",
        f"{BASE_URL}/api/v1/fundamentals/{SYMBOL}/balance-sheet",
        params={"frequency": "annual"}
    )
    save_json(result, "balance_sheet_annual.json")
    all_results["endpoints"]["balance_sheet_annual"] = result
    
    # Income Statement - Quarterly
    result = test_endpoint(
        "Income Statement (Quarterly)",
        f"{BASE_URL}/api/v1/fundamentals/{SYMBOL}/income-statement",
        params={"frequency": "quarterly"}
    )
    save_json(result, "income_statement_quarterly.json")
    all_results["endpoints"]["income_statement_quarterly"] = result
    
    # Income Statement - Annual
    result = test_endpoint(
        "Income Statement (Annual)",
        f"{BASE_URL}/api/v1/fundamentals/{SYMBOL}/income-statement",
        params={"frequency": "annual"}
    )
    save_json(result, "income_statement_annual.json")
    all_results["endpoints"]["income_statement_annual"] = result
    
    # Cash Flow - Quarterly
    result = test_endpoint(
        "Cash Flow (Quarterly)",
        f"{BASE_URL}/api/v1/fundamentals/{SYMBOL}/cashflow",
        params={"frequency": "quarterly"}
    )
    save_json(result, "cashflow_quarterly.json")
    all_results["endpoints"]["cashflow_quarterly"] = result
    
    # Cash Flow - Annual
    result = test_endpoint(
        "Cash Flow (Annual)",
        f"{BASE_URL}/api/v1/fundamentals/{SYMBOL}/cashflow",
        params={"frequency": "annual"}
    )
    save_json(result, "cashflow_annual.json")
    all_results["endpoints"]["cashflow_annual"] = result
    
    # All Fundamentals - Quarterly
    result = test_endpoint(
        "All Fundamentals (Quarterly)",
        f"{BASE_URL}/api/v1/fundamentals/{SYMBOL}/all",
        params={"frequency": "quarterly"}
    )
    save_json(result, "fundamentals_all_quarterly.json")
    all_results["endpoints"]["fundamentals_all_quarterly"] = result
    
    # All Fundamentals - Annual
    result = test_endpoint(
        "All Fundamentals (Annual)",
        f"{BASE_URL}/api/v1/fundamentals/{SYMBOL}/all",
        params={"frequency": "annual"}
    )
    save_json(result, "fundamentals_all_annual.json")
    all_results["endpoints"]["fundamentals_all_annual"] = result
    
    # =================================================================
    # 4. COMPANY INFO
    # =================================================================
    print("\n" + "=" * 70)
    print("4. TESTING COMPANY INFO")
    print("=" * 70)
    
    # Company Info
    result = test_endpoint(
        "Company Info",
        f"{BASE_URL}/api/v1/company/{SYMBOL}/info"
    )
    save_json(result, "company_info.json")
    all_results["endpoints"]["company_info"] = result
    
    # Insider Transactions
    result = test_endpoint(
        "Insider Transactions",
        f"{BASE_URL}/api/v1/company/{SYMBOL}/insider-transactions"
    )
    save_json(result, "insider_transactions.json")
    all_results["endpoints"]["insider_transactions"] = result
    
    # Analyst Recommendations
    result = test_endpoint(
        "Analyst Recommendations",
        f"{BASE_URL}/api/v1/company/{SYMBOL}/analyst-recommendations"
    )
    save_json(result, "analyst_recommendations.json")
    all_results["endpoints"]["analyst_recommendations"] = result
    
    # =================================================================
    # SAVE COMPLETE RESULTS
    # =================================================================
    save_json(all_results, "complete_test_results.json")
    
    # =================================================================
    # SUMMARY
    # =================================================================
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    total_tests = len([v for v in all_results["endpoints"].values() if isinstance(v, dict)])
    successful_tests = len([v for v in all_results["endpoints"].values() if isinstance(v, dict) and v.get("success")])
    
    # Count individual indicator tests
    if "technical_indicators_individual" in all_results["endpoints"]:
        ind_results = all_results["endpoints"]["technical_indicators_individual"]
        total_tests += len(ind_results) - 1  # Subtract 1 because we already counted it
        successful_tests += len([v for v in ind_results.values() if v.get("success")]) - 1
    
    print(f"Total Tests: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {total_tests - successful_tests}")
    print(f"Success Rate: {(successful_tests/total_tests*100):.1f}%")
    print(f"\nAll results saved to: {OUTPUT_DIR}/")
    print("=" * 70)

if __name__ == "__main__":
    main()
