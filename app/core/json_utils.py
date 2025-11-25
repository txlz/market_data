"""
JSON utilities for converting data to structured JSON format
"""
import pandas as pd
import io
from typing import Dict, List, Any


def csv_to_json(csv_string: str, remove_header_lines: bool = True) -> List[Dict[str, Any]]:
    """
    Convert CSV string to list of dictionaries (JSON format)
    
    Args:
        csv_string: CSV formatted string
        remove_header_lines: Remove comment lines starting with #
        
    Returns:
        List of dictionaries representing the data
    """
    if remove_header_lines:
        # Remove header comment lines
        lines = csv_string.split('\n')
        csv_lines = [line for line in lines if not line.startswith('#')]
        csv_string = '\n'.join(csv_lines)
    
    # Read CSV into DataFrame
    df = pd.read_csv(io.StringIO(csv_string))
    
    # Convert to list of dictionaries
    return df.to_dict('records')


def dataframe_to_json(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Convert pandas DataFrame to list of dictionaries
    
    Args:
        df: pandas DataFrame
        
    Returns:
        List of dictionaries representing the data
    """
    # Reset index to include it in the output
    df_reset = df.reset_index()
    
    # Handle datetime columns
    for col in df_reset.columns:
        if pd.api.types.is_datetime64_any_dtype(df_reset[col]):
            df_reset[col] = df_reset[col].astype(str)
    
    # Convert to list of dictionaries
    return df_reset.to_dict('records')


def financial_statement_to_json(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Convert financial statement DataFrame to structured JSON
    Financial statements have dates as columns and line items as rows
    
    Args:
        df: pandas DataFrame with financial statement data
        
    Returns:
        Dictionary with periods as keys and line items as nested dicts
    """
    if df.empty:
        return {}
    
    # Transpose so dates become rows
    df_transposed = df.T
    
    # Convert to dictionary where each date is a key
    result = {}
    for date_col in df_transposed.index:
        # Convert timestamp to string if needed
        date_str = str(date_col) if not isinstance(date_col, str) else date_col
        
        # Create a dictionary of line items for this period
        period_data = {}
        for line_item in df_transposed.columns:
            value = df_transposed.loc[date_col, line_item]
            # Handle NaN values
            if pd.notna(value):
                period_data[line_item] = float(value) if isinstance(value, (int, float)) else value
            else:
                period_data[line_item] = None
        
        result[date_str] = period_data
    
    return result


def parse_indicator_string(indicator_string: str) -> Dict[str, Any]:
    """
    Parse technical indicator string format into structured JSON
    
    Args:
        indicator_string: String with format "## indicator values...\n\ndate: value\n..."
        
    Returns:
        Dictionary with dates, values, and description
    """
    import re
    
    lines = indicator_string.strip().split('\n')
    
    # Regex pattern to match date format YYYY-MM-DD at the start of a line before colon
    date_line_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2}):\s*(.+)$')
    
    # Extract header and description
    header = ""
    description = ""
    values = []
    
    in_description = False
    for line in lines:
        line = line.strip()
        
        if not line:
            continue
            
        if line.startswith('##'):
            header = line.replace('##', '').strip()
        else:
            # Try to match date:value pattern
            date_match = date_line_pattern.match(line)
            
            if date_match and not in_description:
                # This is a proper date:value line
                date_str = date_match.group(1)
                value_str = date_match.group(2).strip()
                
                # Try to convert value to float if possible
                try:
                    if value_str not in ["N/A", "N/A: Not a trading day (weekend or holiday)"]:
                        value = float(value_str)
                    else:
                        value = value_str
                except ValueError:
                    value = value_str
                
                values.append({
                    "date": date_str,
                    "value": value
                })
            else:
                # This is description text
                in_description = True
                description += line + " "
    
    return {
        "header": header,
        "values": values,
        "description": description.strip()
    }
