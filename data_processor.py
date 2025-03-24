import pandas as pd
import requests
import io
import os
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import time

def fetch_with_retry(url, max_retries=3):
    """Helper function to fetch data with retries"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                print(f"Failed to fetch data from {url} after {max_retries} attempts: {e}")
                return None
            print(f"Attempt {attempt + 1} failed, retrying...")
            time.sleep(2 ** attempt)  # Exponential backoff

def generate_sample_temperature_data():
    """Generate sample temperature data if API fails"""
    print("Generating sample temperature data...")
    years = list(range(1900, 2024))
    temperatures = [15 + year * 0.01 + np.random.normal(0, 0.5) for year in years]
    
    df = pd.DataFrame({
        'Year': years,
        'Temperature': temperatures,
        'Type': 'Historical'
    })
    
    # Generate predictions
    X = df['Year'].values.reshape(-1, 1)
    y = df['Temperature'].values
    model = LinearRegression()
    model.fit(X, y)
    
    future_years = np.array(range(2024, 2054))
    predictions = model.predict(future_years.reshape(-1, 1))
    
    prediction_df = pd.DataFrame({
        'Year': future_years,
        'Temperature': predictions,
        'Type': 'Prediction'
    })
    
    return pd.concat([df, prediction_df])

def fetch_temperature_data():
    """
    Fetch global temperature data from NASA GISS
    Returns processed DataFrame
    """
    try:
        url = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
        response = fetch_with_retry(url)
        
        if response is None:
            return generate_sample_temperature_data()
            
        df = pd.read_csv(io.StringIO(response.text), skiprows=1)
        
        # Process the data
        df = df.melt(id_vars=['Year'], var_name='Month', value_name='Temperature')
        df = df[df['Month'] != 'J-D']  # Remove annual average
        df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce')
        
        # Add temperature predictions
        yearly_avg = df.groupby('Year')['Temperature'].mean().reset_index()
        X = yearly_avg['Year'].values.reshape(-1, 1)
        y = yearly_avg['Temperature'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict next 30 years
        future_years = np.array(range(X[-1][0] + 1, X[-1][0] + 31)).reshape(-1, 1)
        predictions = model.predict(future_years)
        
        prediction_df = pd.DataFrame({
            'Year': future_years.flatten(),
            'Temperature': predictions,
            'Type': 'Prediction'
        })
        yearly_avg['Type'] = 'Historical'
        
        final_df = pd.concat([yearly_avg, prediction_df])
        return final_df
    except Exception as e:
        print(f"Error processing temperature data: {e}")
        return generate_sample_temperature_data()

def generate_sample_emissions_data():
    """Generate sample emissions data if API fails"""
    print("Generating sample emissions data...")
    years = range(1900, 2024)
    countries = ['United States', 'China', 'India', 'Russian Federation', 
                'Japan', 'Germany', 'United Kingdom', 'Canada']
    
    data = []
    for country in countries:
        base_emissions = np.random.uniform(100, 1000)
        growth_rate = np.random.uniform(1.01, 1.03)
        population_base = np.random.uniform(10e6, 500e6)
        
        for year in years:
            emissions = base_emissions * (growth_rate ** (year - 1900))
            population = population_base * (1.01 ** (year - 1900))
            data.append({
                'country': country,
                'year': year,
                'co2': emissions,
                'population': population,
                'co2_per_capita': emissions / population * 1e6
            })
    
    return pd.DataFrame(data)

def fetch_co2_emissions():
    """
    Fetch CO2 emissions data from Our World in Data
    Returns processed DataFrame
    """
    try:
        url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
        response = fetch_with_retry(url)
        
        if response is None:
            return generate_sample_emissions_data()
            
        df = pd.read_csv(io.StringIO(response.text))
        
        # Select relevant columns and filter for major countries
        columns = ['country', 'year', 'co2', 'co2_per_capita', 'population']
        major_countries = ['United States', 'China', 'India', 'Russian Federation', 
                         'Japan', 'Germany', 'United Kingdom', 'Canada']
        
        df = df[df['country'].isin(major_countries)][columns]
        df = df[df['year'] >= 1900]
        
        return df
    except Exception as e:
        print(f"Error processing CO2 emissions data: {e}")
        return generate_sample_emissions_data()

def fetch_weather_events():
    """
    Fetch extreme weather events data from NOAA
    Returns processed DataFrame
    """
    try:
        # For demo purposes, we'll generate sample weather events data
        # In a real application, you would fetch this from NOAA's API
        years = range(1990, 2024)
        events = []
        event_types = ['Hurricane', 'Flood', 'Drought', 'Extreme Temperature']
        
        for year in years:
            for event_type in event_types:
                # Generate increasing trend in events
                base_events = 10 + (year - 1990) * 0.5
                num_events = int(np.random.normal(base_events, 2))
                events.append({
                    'Year': year,
                    'Event_Type': event_type,
                    'Count': max(0, num_events)
                })
        
        return pd.DataFrame(events)
    except Exception as e:
        print(f"Error generating weather events data: {e}")
        return None

def create_geographic_data():
    """
    Create geographic data for emissions visualization
    """
    try:
        emissions_df = fetch_co2_emissions()
        if emissions_df is None:
            return None
            
        # Get the most recent year's data
        latest_year = emissions_df['year'].max()
        latest_data = emissions_df[emissions_df['year'] == latest_year]
        
        # Add latitude and longitude for each country (simplified)
        country_coords = {
            'United States': {'lat': 37.0902, 'lon': -95.7129},
            'China': {'lat': 35.8617, 'lon': 104.1954},
            'India': {'lat': 20.5937, 'lon': 78.9629},
            'Russian Federation': {'lat': 61.5240, 'lon': 105.3188},
            'Japan': {'lat': 36.2048, 'lon': 138.2529},
            'Germany': {'lat': 51.1657, 'lon': 10.4515},
            'United Kingdom': {'lat': 55.3781, 'lon': -3.4360},
            'Canada': {'lat': 56.1304, 'lon': -106.3468}
        }
        
        geo_data = []
        for _, row in latest_data.iterrows():
            country_data = country_coords.get(row['country'])
            if country_data:
                geo_data.append({
                    'country': row['country'],
                    'co2': row['co2'],
                    'lat': country_data['lat'],
                    'lon': country_data['lon']
                })
        
        return pd.DataFrame(geo_data)
    except Exception as e:
        print(f"Error creating geographic data: {e}")
        return None

def process_and_save_data():
    """
    Process and save all data to CSV files
    """
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Process temperature data
    temp_df = fetch_temperature_data()
    if temp_df is not None:
        temp_df.to_csv('data/temperature_data.csv', index=False)
    
    # Process CO2 emissions data
    emissions_df = fetch_co2_emissions()
    if emissions_df is not None:
        emissions_df.to_csv('data/emissions_data.csv', index=False)
    
    # Process weather events data
    weather_df = fetch_weather_events()
    if weather_df is not None:
        weather_df.to_csv('data/weather_events.csv', index=False)
    
    # Create and save geographic data
    geo_df = create_geographic_data()
    if geo_df is not None:
        geo_df.to_csv('data/geographic_data.csv', index=False)

if __name__ == "__main__":
    process_and_save_data() 