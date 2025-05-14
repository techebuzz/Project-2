import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime

# Set plot style
plt.style.use('seaborn')
sns.set_palette('husl')

# Display settings
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

def load_data(file_path):
    """Load and preprocess the COVID-19 dataset"""
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    return df

def analyze_global_trends(df):
    """Analyze global COVID-19 trends"""
    # Global cases over time
    global_cases = df.groupby('date')['total_cases'].sum().reset_index()
    
    plt.figure(figsize=(15, 8))
    plt.plot(global_cases['date'], global_cases['total_cases'])
    plt.title('Global COVID-19 Cases Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Cases')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('global_cases.png')
    plt.close()

def analyze_country_comparison(df, countries):
    """Compare COVID-19 metrics between countries"""
    country_data = df[df['location'].isin(countries)]
    
    # Plot cases per million for selected countries
    plt.figure(figsize=(15, 8))
    for country in countries:
        country_df = country_data[country_data['location'] == country]
        plt.plot(country_df['date'], country_df['total_cases_per_million'], label=country)
    
    plt.title('COVID-19 Cases per Million by Country')
    plt.xlabel('Date')
    plt.ylabel('Cases per Million')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('country_comparison.png')
    plt.close()

def analyze_vaccination_progress(df):
    """Analyze vaccination progress"""
    # Plot vaccination rates
    plt.figure(figsize=(15, 8))
    for country in ['United States', 'United Kingdom', 'Germany', 'France', 'Italy']:
        country_df = df[df['location'] == country]
        plt.plot(country_df['date'], country_df['people_vaccinated_per_hundred'], 
                label=country, marker='o', markersize=2)
    
    plt.title('Vaccination Progress (% of Population)')
    plt.xlabel('Date')
    plt.ylabel('Percentage Vaccinated')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('vaccination_progress.png')
    plt.close()

def create_world_map(df):
    """Create an interactive world map of COVID-19 cases"""
    latest_date = df['date'].max()
    latest_data = df[df['date'] == latest_date]
    
    fig = px.choropleth(latest_data,
                        locations='iso_code',
                        color='total_cases_per_million',
                        hover_name='location',
                        color_continuous_scale='Viridis',
                        title=f'COVID-19 Cases per Million (as of {latest_date.strftime("%Y-%m-%d")})')
    
    fig.write_html('world_map.html')

def main():
    # Load data
    df = load_data('data/owid-covid-data.csv')
    
    # Perform analyses
    analyze_global_trends(df)
    
    # Compare major countries
    countries = ['United States', 'India', 'Brazil', 'United Kingdom', 'Germany', 'France']
    analyze_country_comparison(df, countries)
    
    # Analyze vaccination progress
    analyze_vaccination_progress(df)
    
    # Create world map
    create_world_map(df)
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Total number of countries: {df['location'].nunique()}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print("\nTop 5 countries by total cases:")
    latest_data = df[df['date'] == df['date'].max()]
    print(latest_data.nlargest(5, 'total_cases')[['location', 'total_cases']])

if __name__ == "__main__":
    main() 