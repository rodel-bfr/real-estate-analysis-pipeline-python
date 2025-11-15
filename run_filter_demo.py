import os
import pandas as pd
from src.data_filter import DataFilter
from src.config import COUNTY_LIST, CITY_LIST, SHORT_NAME_LIST

def run_filtering_demo():
    """
    Demonstrates the DataFilter class by loading the raw
    scraped data from /data_raw and running the
    filtering process.
    
    The output is saved to /data_filtered_demo.
    """
    print("--- Running Data Filtering Demo ---")
    
    RAW_DATA_PATH = 'data_raw'
    DEMO_OUTPUT_PATH = 'data_filtered_demo'
    
    RAW_SELL_FILE = os.path.join(RAW_DATA_PATH, 'sell_df.csv')
    RAW_RENT_FILE = os.path.join(RAW_DATA_PATH, 'rent_df.csv')

    # --- Step 1: Load the RAW data ---
    try:
        print(f"Loading raw data from {RAW_DATA_PATH}...")
        sell_df = pd.read_csv(RAW_SELL_FILE, index_col=0)
        rent_df = pd.read_csv(RAW_RENT_FILE, index_col=0)
        print("Raw data loaded successfully.")
    except FileNotFoundError as e:
        print(f"ERROR: Raw data file not found: {e.filename}")
        print(f"Please make sure 'sell_df.csv' and 'rent_df.csv' are in the '{RAW_DATA_PATH}' folder.")
        return

    # --- Step 2: Set up the DataFilter ---
    
    # --- MODIFICATION ---
    # This also matches the new __init__
    # We are telling it to WRITE to the 'data_filtered_demo' folder
    filter_params = {
        'sell_df': sell_df,
        'rent_df': rent_df,
        'county_list': COUNTY_LIST,
        'city_list': CITY_LIST,
        'short_name_list': SHORT_NAME_LIST,
        'data_path': DEMO_OUTPUT_PATH  # <-- This is the important change
    }
    
    data_filter = DataFilter(filter_params)
    
    if not os.path.exists(DEMO_OUTPUT_PATH):
        os.makedirs(DEMO_OUTPUT_PATH)

    # --- Step 3: Run the filtering process ---
    print(f"Running DataFilter.process_data()...")
    
    df_list = data_filter.process_data()
    
    print("\nFiltering demo complete.")
    print(f"Check the '{DEMO_OUTPUT_PATH}' folder to see the 8 generated (un-cleaned) CSV files.")

if __name__ == "__main__":
    run_filtering_demo()