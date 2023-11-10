# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 14:33:46 2023

@author: HP
"""


# Import library packages for this project
import pandas as pd
import matplotlib.pyplot as plt


# Define the function for plotting the GDP time-series
def ln_crt(x, y, label):
    
    """
    Plot a time-series line plot of the GDP growth for the countries in the 
    dataframe.
    
    Parameters:
    - x: Years(time-series)
    - y: GDP (current US$)
    
    Returns
    ------------------------
    fig_ln: line 2D figures
    a collection of line
    """
    
    # Make a line plot
    fig_ln = plt.figure(figsize=(14, 8))

    # Loop through each country and plot the time-series
    for country in gdp_data_long['Country Name'].unique():
        country_data = gdp_data_long[gdp_data_long['Country Name'] == country]
        plt.plot(country_data['Year'], country_data['GDP'], label=country)

    # Add title and labels
    plt.title('GDP Growth Over the Years', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('GDP (current US$)', fontsize=14)
    plt.legend()

    # Save the plot
    plt.savefig('gdp_timeseries.png')

    # Show the plot
    plt.show()
    return fig_ln
    

# Define the function for the bar plot
def bar_crt(df):
    
    """
    Make a bar plot for the GDP per China region.

    Parameters:
    - df: A pandas DataFrame containing the long-format GDP data with regions.

    Returns
    ------------------------
    fig_bar: A bar chart
    a collection of bars depicting the data plotted.
    """
    
    # Create the bar plot
    fig_bar = plt.figure(figsize=(14, 8))

    # Aggregate the GDP data by region, sort the values and plot the bar
    df.groupby('Region')['GDP'].sum().sort_values(ascending=False).\
    plot(kind='bar')

    # Set the title and labels
    plt.title('Total GDP per China Region', fontsize=16)
    plt.xlabel('Region', fontsize=14)
    plt.ylabel('Total GDP (current US$)', fontsize=14)
    plt.xticks(rotation=45)

    # Save the plot
    plt.savefig('china_gdp_by_region.png')

    # Show the plot
    plt.tight_layout()
    plt.show()
    return fig_bar


# Define the function for the box plot
def box_plt(df):
    
    """
    Create a box plot to show the yearly distribution of GDP per China 
    province for a specified period, using matplotlib.

    Parameters:
    - df: A pandas DataFrame containing the long-format GDP data.

    Returns
    ------------------------
    fig_box: A box plot
    A plot of box and whiskers
    
    The box extends from the first quartile (Q1) to the third quartile (Q3) 
    of the data, with a line at the median. The whiskers extend from the box 
    by 1.5x the inter-quartile range (IQR). Flier points are those past the 
    end of the whiskers
    """
    
    # Make the box plot
    fig_box, ax = plt.subplots(figsize=(16, 10))
    ax.boxplot(data_to_plot, vert=True, patch_artist=True)

    # Set the title and labels
    ax.set_title('Yearly Distribution of GDP per China Province from {} to {}'
                 .format(1990, 2020), fontsize=16)
    ax.set_xlabel('Province', fontsize=14)
    ax.set_ylabel('GDP (current US$)', fontsize=14)

    # Set x-axis labels and rotate them
    ax.set_xticklabels(provinces, rotation=90)

    # Save the plot
    plt.savefig('Provincial_gdp_boxplot.png')

    # Show the plot
    plt.tight_layout()
    plt.show()
    return fig_box


# Data Preparation
# Read CSV files into pandas
gdp_data = pd.read_csv('GDP for top 5 leading Economies.csv')
china_gdp = pd.read_csv('Chinas GDP in Province.csv')

# Rename the 'Unnamed: 0' column to 'Year' in china_gdp DataFrame
china_gdp = china_gdp.rename(columns={'Unnamed: 0': 'Year'})

# Drop columns irrelevant to the data preprocessing
gdp_data_cleaned = gdp_data.drop(['Series Name', 'Series Code'], axis=1)

# Melt the dataframes to convert it from wide to long format
gdp_data_long = gdp_data_cleaned.melt(id_vars=['Country Name', 'Country Code'],
                                      var_name='Year', value_name='GDP')
china_gdp_long = china_gdp.melt(id_vars=['Year'], var_name='Province',
                                value_name='GDP')

# Extract the year from the Year column in gdp_data and convert it to datetime
gdp_data_long['Year'] = gdp_data_long['Year'].str.extract('(\d+)').astype(int)
gdp_data_long['Year'] = pd.to_datetime(gdp_data_long['Year'], format='%Y')

# Ensure the GDP values in gdp_data are numeric (float)
gdp_data_long['GDP'] = pd.to_numeric(gdp_data_long['GDP'], errors='coerce')

# Sort the gdp_data by Country and Year
gdp_data_long = gdp_data_long.sort_values(by=['Country Name', 'Year'])

# Define a mapping of provinces to regions
province_to_region = {
    'Anhui': 'East China', 'Shanghai': 'East China', 'Shandong': 'East China',
    'Jiangxi': 'East China', 'Jiangsu': 'East China', 'Zhejiang': 'East China',
    'Fujian': 'East China', 'Tianjin': 'North China', 'Shanxi': 'North China',
    'Beijing': 'North China', 'Hebei': 'North China',
    'Inner Mongolia': 'North China', 'Liaoning': 'Northeast China',
    'Jilin': 'Northeast China', 'Heilongjiang': 'Northeast China',
    'Xinjiang': 'Northwest China', 'Gansu': 'Northwest China',
    'Ningxia': 'Northwest China', 'Qinghai': 'Northwest China',
    'Shaanxi': 'Northwest China', 'Hubei': 'South Central China',
    'Guangxi': 'South Central China', 'Hainan': 'South Central China',
    'Guangdong': 'South Central China', 'Henan': 'South Central China',
    'Hunan': 'South Central China', 'Guizhou': 'Southwest China',
    'Sichuan': 'Southwest China', 'Tibet': 'Southwest China',
    'Yunnan': 'Southwest China', 'Chongqing': 'Southwest China'
}

# Map the provinces in china_gdp to the regions
china_gdp_long['Region'] = china_gdp_long['Province'].map(province_to_region)

# Display the cleaned and transformed data
print(gdp_data_long.head())
print(china_gdp_long.head())

# use the function to plot the time-series from the gdp_data_long dataframe
ln_crt(gdp_data_long['Year'], gdp_data_long['GDP'], label='country')

# Call the function to plot the GDP by region
bar_crt(china_gdp_long)

# Prepare the data for the box plot
# Filter the dataframe for the specified years
china_gdp_long_filtered = china_gdp_long[(china_gdp_long['Year'] >= 
                           1990) & (china_gdp_long['Year'] <= 2020)]

provinces = china_gdp_long_filtered['Province'].unique()
data_to_plot = [china_gdp_long_filtered.loc[china_gdp_long_filtered
                    ['Province'] == province, 'GDP'].values for province
                    in provinces]

# Call the function to plot the GDP distribution per province
box_plt(china_gdp_long)