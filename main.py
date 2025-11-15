import os
from src.data_filter import DataFilter
from src.analyzer import RentalAnalyzer
from src.config import CITY_LIST, SHORT_NAME_LIST, COUNTY_LIST

def run_analysis():
    """
    Runs the full apartment market analysis from saved CSV files.
    """
    print("Starting Romanian Apartment Market Analysis...")
    print("Note: Loading data from pre-saved CSV files in the /data folder.\n")

    # --- Step 1: Load the Cleaned Data ---
    filter_params = {
        'short_name_list': SHORT_NAME_LIST,
        'county_list': COUNTY_LIST, 
        'city_list': CITY_LIST,
        'data_path': 'data'
    }

    data_filter = DataFilter(filter_params)
    
    try:
        updated_df_list = data_filter.update_data()
        print("Successfully loaded cleaned data from /data folder.\n")
    except FileNotFoundError as e:
        print(f"ERROR: Could not find data file: {e.filename}")
        print("Please ensure your CSV files (cj_rent_df.csv, b_rent_df.csv, etc.)")
        print("are in the /data folder relative to this script.")
        return

    # --- Step 2: Run the Analysis ---
    analyzer_params = {
        'df_list': updated_df_list,
        'city_list': CITY_LIST,
    }

    analyzer = RentalAnalyzer(analyzer_params)
    
    # Step 2a: Run all calculations and generate plots
    print("Running analysis and generating plots (saved to /images)...")
    analyzer.analyzer() 
    
    # Step 2b: Print the results to the console
    print("\n--- CONSOLE ANALYSIS REPORT ---")
    analyzer.print_console_report()
    
    # Step 2c: Generate the Word document report
    analyzer.generate_word_report("Analysis_Report.docx")

    print(f"\nAnalysis complete. Check /images for plots and /reports for the .docx report.")

if __name__ == "__main__":
    run_analysis()