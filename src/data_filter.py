import pandas as pd
import os

class DataFilter():
    def __init__(self, params):
        # Initialize the DataFilter class with the provided parameters
        self.sell_df = params.get('sell_df')  # DataFrame containing selling data
        self.rent_df = params.get('rent_df')  # DataFrame containing rental data
        self.county_list = params.get('county_list')  # List of counties to filter
        self.city_list = params.get('city_list')  # List of cities to filter
        self.short_name_list = params.get('short_name_list')  # List of short names for counties
        self.listing = ['sell', 'rent']
        
        # --- MODIFICATION ---
        # Get data_path from params, default to 'data' if not provided
        self.data_path = params.get('data_path', 'data') 
        
    def _assign_name(self, short_name, listing):
        # Assigns a name based on the short name and listing type
        return f'{short_name}_{listing}_df'
        
    def _filter_county(self, df, county, city, listing, short_name):
        # Filter the DataFrame based on the county and save the filtered data to a CSV file
        if county == "Bucuresti":
            filter_condition = df['address'].str.contains(f'{county}')
        else:
            filter_condition = df['address'].str.contains(f'{city}, {county}')
        
        name = self._assign_name(short_name, listing)
        county_df = df[filter_condition].set_index(df.columns[0])
        county_df.index = range(1, len(county_df) + 1)
        county_df.name = name
        
        # Ensure data path exists
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
            
        # Save to the flexible data_path (could be 'data' or 'data_filtered_demo')
        county_df.to_csv(os.path.join(self.data_path, f'{name}.csv'))
        return county_df
    
    def process_data(self):
        # Process the data for each county and listing type
        df_list = []
        for county, city, short_name in zip(self.county_list, self.city_list, self.short_name_list):
            for listing in self.listing:
                df = self.sell_df if listing == 'sell' else self.rent_df
                filtered_df = self._filter_county(df, county, city, listing, short_name)
                df_list.append(filtered_df)
        print(f"Filtered files have been saved to the '{self.data_path}' folder.")
        return df_list
    
    def update_data(self):
        # Update the data by reading the CSV files from self.data_path
        new_df_list = []
        for short_name in self.short_name_list:
            for listing in self.listing:
                name = self._assign_name(short_name, listing)
                
                # Read from the flexible data_path
                filename = os.path.join(self.data_path, f'{name}.csv')
                
                try:
                    new_df = pd.read_csv(filename, index_col=0)
                    new_df.name = name
                    new_df_list.append(new_df)
                except FileNotFoundError:
                    print(f"Error: Could not find file {filename}")
                    print(f"Please ensure your CSV files are in the '{self.data_path}' directory.")
                    raise
        return new_df_list