import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import t

class RentalAnalyzer():
    def __init__(self, params):
        # Initialize the RentalAnalyzer class with the provided parameters
        self.df_list = params.get('df_list')
        self.stats_dict = {
            'rent': {'sample_size': [], 'mean': [], 'median': [], 'mode': [], 'skewness': [], 'variance': [],
                     'standard_deviation': [], 'coefficient_of_variation': [], 'conf_level': [], 'lower_bound': [], 
                     'upper_bound': []},
            'sell': {'sample_size': [], 'mean': [], 'median': [], 'mode': [], 'skewness': [], 'variance': [],
                     'standard_deviation': [], 'coefficient_of_variation': [], 'conf_level': [], 'lower_bound': [], 
                     'upper_bound': []}
        }
        self.city_list = params.get('city_list')
        
        # Define the path for saving plots
        self.images_path = 'images'
        # Ensure images directory exists
        if not os.path.exists(self.images_path):
            os.makedirs(self.images_path)
    
    def _calculate_stats(self, df, column='price_per_sqm', conf_level=0.95):
        # Calculate various statistical measures for the given DataFrame and column
        sample_size = len(df)
        mean = df[column].mean()
        median = df[column].median()
        mode = df[column].mode()
        skewness = df[column].skew()
        variance = df[column].var()
        std_dev = df[column].std()
        coefficient_of_variation = std_dev / mean
        dfg = len(df) - 1
        crit_value = t.ppf((1 + conf_level) / 2, dfg)
        lower_bound = mean - crit_value * (std_dev / np.sqrt(len(df)))
        upper_bound = mean + crit_value * (std_dev / np.sqrt(len(df)))
        stats = {
            'sample_size': sample_size,
            'mean': mean,
            'median': median,
            'mode': mode,
            'skewness': skewness,
            'variance': variance,
            'standard_deviation': std_dev,
            'coefficient_of_variation': coefficient_of_variation,
            'conf_level': conf_level,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound
        }
        return stats

    def _append_stats(self, key, stats):
        # Append the calculated statistics to the stats_dict based on the given key
        for column, value in stats.items():
            self.stats_dict[key][column].append(value)
        
    def _get_stats_dict(self):
        # Calculate and collect the statistics for each DataFrame in df_list
        for df in self.df_list:
            key = 'rent' if 'rent' in df.name else 'sell'
            stats = self._calculate_stats(df)
            self._append_stats(key, stats)
    
    def _plot_price_per_sqm(self, city, sell_df, rent_df):
        # Plot the bar charts for selling and renting price per square meter for a given city
        n_cols = 2
        n_rows = 1
        fig, axs = plt.subplots(n_rows, n_cols, figsize=(15, 4))

        sell_ax = axs[0]
        rent_ax = axs[1]
        sell_ax.set_title(f'{city} (Sell)')
        rent_ax.set_title(f'{city} (Rent)')

        # Bar chart for selling price per square meter
        sell_counts, sell_bins, _ = sell_ax.hist(sell_df['price_per_sqm'], bins=15, edgecolor='black', linewidth=1)
        sell_ticks = np.linspace(sell_bins[0], sell_bins[-1], num=15, endpoint=True)
        sell_ax.set_xticks(sell_ticks)

        # Bar chart for renting price per square meter
        rent_counts, rent_bins, _ = rent_ax.hist(rent_df['price_per_sqm'], bins=15, edgecolor='black', linewidth=1)
        rent_ticks = np.linspace(rent_bins[0], rent_bins[-1], num=15, endpoint=True)
        rent_ax.set_xticks(rent_ticks)

        plt.tight_layout()
        
        # MODIFICATION: Save the figure instead of showing it
        plot_filename = os.path.join(self.images_path, f'{city}_price_per_sqm.png')
        plt.savefig(plot_filename)
        print(f"Saved plot to {plot_filename}")
        plt.close(fig) # Close the figure to free up memory
    
    def _estimate_monthly_return(self, selling_price_per_sqm, renting_price_per_sqm, property_value=100000):
        # Estimate the monthly return on investment based on selling and renting price per square meter
        property_size = property_value / selling_price_per_sqm
        monthly_rental_income = renting_price_per_sqm * property_size
        monthly_return = (monthly_rental_income / property_value) * 100
        return monthly_return

    def analyzer(self):
        # Calls all private methods in order to print a summary of the statistical analysis and ranks the cities
        self._get_stats_dict()
        sell_dfs = [df for df in self.df_list if 'sell' in df.name]
        rent_dfs = [df for df in self.df_list if 'rent' in df.name]
        sell = self.stats_dict['sell']
        rent = self.stats_dict['rent']
        
        city_ranking = []
        
        for city, sell_df, rent_df, i in zip(self.city_list, sell_dfs, rent_dfs, list(range(len(self.city_list)+1))): 
            lower_estimate = self._estimate_monthly_return(sell['lower_bound'][i], rent['lower_bound'][i])
            upper_estimate = self._estimate_monthly_return(sell['upper_bound'][i], rent['upper_bound'][i])
            
            # This will now save the plot
            self._plot_price_per_sqm(city, sell_df, rent_df)
            
            text = f"""
Based on the data from storia.ro, the following observations can be made for {city}:

1. Analysis of property listed for sale:

Sample Size: {sell['sample_size'][i]} estates listed for sale.
Average Selling Price per Square Meter: {sell['mean'][i]:.2f}
Median Selling Price per Square Meter: {sell['median'][i]:.2f}
Most Common Selling Price per Square Meter: {sell['mode'][i][0]}
Skewness: {sell['skewness'][i]:.2f}
Standard deviation: {sell['standard_deviation'][i]:.2f}
Coefficient of Variation: {sell['coefficient_of_variation'][i]:.2f}
Confidence intervals: {sell['conf_level'][i]*100}% confidence that the true average price of a 
square meter is between {sell['lower_bound'][i]:.2f} - {sell['upper_bound'][i]:.2f}


2. Analysis of property listed for rent:

Sample Size: {rent['sample_size'][i]} estates listed for rent.
Average Renting Price per Square Meter: {rent['mean'][i]:.2f}
Median Renting Price per Square Meter: {rent['median'][i]:.2f}
Most Common Renting Price per Square Meter: {rent['mode'][i][0]}
Skewness: {rent['skewness'][i]:.2f}
Standard deviation: {rent['standard_deviation'][i]:.2f}
Coefficient of Variation: {rent['coefficient_of_variation'][i]:.2f}
Confidence intervals: {rent['conf_level'][i]*100}% confidence that the true average price of a 
square meter is between {rent['lower_bound'][i]:.2f} - {rent['upper_bound'][i]:.2f}

For every euro spent buying a square meter in {city}, we can expect a monthly income from rent between
{lower_estimate:.2f} and {upper_estimate:.2f} euro.
"""         
            print(text)
            city_ranking.append((city, lower_estimate, upper_estimate))
        
        ranked_cities = sorted(city_ranking, key=lambda x: x[1], reverse=True)
        print("\nRanking based on monthly rental income estimates:\n")
        for rank, (city, lower, upper) in enumerate(ranked_cities, start=1):
            print(f"""{rank}. {city}: 
The expected monthly income from rent for every euro spent is estimated to be between {lower:.2f} and {upper:.2f}.\n""")