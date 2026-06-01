import pandas as pd
import numpy as np

def clean_dataset(df, handle_missing="fill_mode", remove_duplicates=True):
    """
    Cleans the dataset and provides a summary report of operations performed.
    Args:
        df: Input pandas DataFrame
        handle_missing: 'fill_mode' (fill categorical with 'Unknown'/Mode), 'drop' (drop rows with missing values)
        remove_duplicates: Boolean to remove exact duplicates
    Returns:
        cleaned_df: Cleaned pandas DataFrame
        report: Dictionary summary of cleaning operations
    """
    cleaned_df = df.copy()
    report = {
        "initial_rows": len(df),
        "duplicates_removed": 0,
        "missing_filled": {},
        "missing_dropped": 0,
        "type_corrections": []
    }
    
    # 1. Handle Duplicates
    if remove_duplicates:
        initial_count = len(cleaned_df)
        cleaned_df = cleaned_df.drop_duplicates()
        report["duplicates_removed"] = initial_count - len(cleaned_df)
        
    # 2. Date parsing and validation
    if "Order_Date" in cleaned_df.columns:
        try:
            cleaned_df["Order_Date"] = pd.to_datetime(cleaned_df["Order_Date"], errors="coerce")
            # Drop invalid dates (NaT)
            invalid_dates = cleaned_df["Order_Date"].isnull().sum()
            if invalid_dates > 0:
                cleaned_df = cleaned_df.dropna(subset=["Order_Date"])
                report["type_corrections"].append(f"Parsed Order_Date to Datetime (removed {invalid_dates} invalid rows)")
            else:
                report["type_corrections"].append("Parsed Order_Date to Datetime successfully")
        except Exception as e:
            report["type_corrections"].append(f"Error parsing Order_Date: {str(e)}")
            
    # 3. Data type corrections
    numeric_cols = {"Units_Sold": "int64", "Unit_Price": "float64", "Revenue": "float64"}
    for col, target_type in numeric_cols.items():
        if col in cleaned_df.columns:
            try:
                # Force conversion, coercing errors to NaN
                cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors="coerce")
                cleaned_df[col] = cleaned_df[col].astype(target_type)
                report["type_corrections"].append(f"Cast {col} to {target_type}")
            except Exception as e:
                report["type_corrections"].append(f"Failed casting {col} to {target_type}: {str(e)}")
                
    # 4. Handle Missing Values
    cols_with_missing = cleaned_df.columns[cleaned_df.isnull().any()].tolist()
    
    if handle_missing == "drop":
        initial_count = len(cleaned_df)
        cleaned_df = cleaned_df.dropna()
        report["missing_dropped"] = initial_count - len(cleaned_df)
    else: # fill mode
        for col in cols_with_missing:
            null_count = int(cleaned_df[col].isnull().sum())
            if null_count > 0:
                if cleaned_df[col].dtype == "object":
                    # For string/categorical columns
                    fill_val = "Unknown"
                    cleaned_df[col] = cleaned_df[col].fillna(fill_val)
                    report["missing_filled"][col] = {"count": null_count, "val": fill_val}
                else:
                    # For numeric columns
                    fill_val = float(cleaned_df[col].median()) if not cleaned_df[col].isnull().all() else 0.0
                    cleaned_df[col] = cleaned_df[col].fillna(fill_val)
                    report["missing_filled"][col] = {"count": null_count, "val": fill_val}
                    
    # Re-calculate revenue just in case Unit_Price or Units_Sold were modified or filled
    if "Revenue" in cleaned_df.columns and "Units_Sold" in cleaned_df.columns and "Unit_Price" in cleaned_df.columns:
        cleaned_df["Revenue"] = (cleaned_df["Units_Sold"] * cleaned_df["Unit_Price"]).round(2)
        
    report["final_rows"] = len(cleaned_df)
    return cleaned_df, report
