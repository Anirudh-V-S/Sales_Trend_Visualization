import os
import pandas as pd
from src.helpers import generate_sales_dataset

REQUIRED_COLUMNS = [
    "Order_ID", "Order_Date", "Product_Name", "Category", 
    "Region", "Sales_Channel", "Units_Sold", "Unit_Price", 
    "Revenue", "Customer_ID"
]

def load_data(file_path="data/sales_data.csv"):
    """
    Loads dataset from CSV file.
    If file doesn't exist, it generates the sample dataset automatically.
    Returns:
        df: Pandas DataFrame
        error: String or None
    """
    if not os.path.exists(file_path):
        # Automatically generate default dataset
        generate_sales_dataset(file_path)
        
    try:
        df = pd.read_csv(file_path)
        return df, None
    except Exception as e:
        return None, str(e)

def validate_dataset(df):
    """
    Validates if the dataset contains all required columns.
    Returns:
        is_valid: Boolean
        missing_columns: List of missing columns
    """
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    is_valid = len(missing_columns) == 0
    return is_valid, missing_columns

def get_data_quality_metrics(df):
    """
    Analyzes missing values, duplicate values, and data type details.
    Returns a dictionary of data quality metrics.
    """
    total_rows = len(df)
    
    # Missing values
    missing_counts = df.isnull().sum().to_dict()
    missing_pcts = (df.isnull().sum() / total_rows * 100).round(2).to_dict()
    
    # Duplicates
    duplicate_count = df.duplicated().sum()
    duplicate_pct = round((duplicate_count / total_rows * 100), 2)
    
    # Data type summary
    dtypes_summary = {col: str(dtype) for col, dtype in df.dtypes.items()}
    
    return {
        "total_rows": total_rows,
        "total_columns": len(df.columns),
        "missing_counts": missing_counts,
        "missing_percentages": missing_pcts,
        "duplicate_count": int(duplicate_count),
        "duplicate_percentage": duplicate_pct,
        "data_types": dtypes_summary
    }
