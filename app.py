print("Starting application...")

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import os
import sys
import traceback
import webbrowser
from threading import Timer

# Initialize the Dash app with a modern theme
try:
    print("Initializing Dash app...")
    app = dash.Dash(
        __name__, 
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        suppress_callback_exceptions=True
    )
    app.title = 'Climate Change Impact Dashboard'
    print("Dash app created successfully")
except Exception as e:
    print(f"Error creating Dash app: {e}")
    traceback.print_exc()
    sys.exit(1)

# Load the processed data
def load_data():
    """Load data with error handling"""
    try:
        print("Loading data files...")
        data_files = {
            'temperature': 'data/temperature_data.csv',
            'emissions': 'data/emissions_data.csv',
            'weather': 'data/weather_events.csv',
            'geo': 'data/geographic_data.csv'
        }
        
        # Check if files exist
        for name, file_path in data_files.items():
            if not os.path.exists(file_path):
                print(f"Error: {file_path} not found")
                return None, None, None, None
            print(f"Found {name} data file")
        
        # Load each file with error handling
        try:
            temp_df = pd.read_csv(data_files['temperature'])
            print("Temperature data loaded successfully")
        except Exception as e:
            print(f"Error loading temperature data: {e}")
            return None, None, None, None
            
        try:
            emissions_df = pd.read_csv(data_files['emissions'])
            print("Emissions data loaded successfully")
        except Exception as e:
            print(f"Error loading emissions data: {e}")
            return None, None, None, None
            
        try:
            weather_df = pd.read_csv(data_files['weather'])
            print("Weather data loaded successfully")
        except Exception as e:
            print(f"Error loading weather data: {e}")
            return None, None, None, None
            
        try:
            geo_df = pd.read_csv(data_files['geo'])
            print("Geographic data loaded successfully")
        except Exception as e:
            print(f"Error loading geographic data: {e}")
            return None, None, None, None
            
        return temp_df, emissions_df, weather_df, geo_df
    except Exception as e:
        print(f"Error in load_data: {e}")
        traceback.print_exc()
        return None, None, None, None

print("Loading data...")
temp_df, emissions_df, weather_df, geo_df = load_data()

try:
    # Check if any of the dataframes is None
    if any(df is None for df in [temp_df, emissions_df, weather_df, geo_df]):
        print("Error: Could not load required data files.")
        app.layout = html.Div([
            html.H1("Error Loading Dashboard",
                   className="text-center text-danger mb-4"),
            html.P("Could not load required data files. Please check the console for error messages.",
                   className="text-center")
        ])
    else:
        print("Data loaded successfully, setting up dashboard layout...")
        
        # Create figures with error handling
        try:
            temp_fig = px.line(temp_df, x='Year', y='Temperature',
                             color='Type',
                             title='Global Temperature Trends')
            print("Temperature figure created successfully")
        except Exception as e:
            print(f"Error creating temperature figure: {e}")
            temp_fig = go.Figure()
            
        try:
            emissions_fig = px.line(emissions_df,
                                  x='year',
                                  y='co2',
                                  color='country',
                                  title='CO2 Emissions Over Time')
            print("Emissions figure created successfully")
        except Exception as e:
            print(f"Error creating emissions figure: {e}")
            emissions_fig = go.Figure()
            
        try:
            weather_fig = px.line(weather_df.groupby(['Year', 'Event_Type'])['Count']
                                .sum()
                                .reset_index(),
                                x='Year',
                                y='Count',
                                color='Event_Type',
                                title='Extreme Weather Events Over Time')
            print("Weather events figure created successfully")
        except Exception as e:
            print(f"Error creating weather events figure: {e}")
            weather_fig = go.Figure()
        
        # Dashboard layout
        app.layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("Climate Change Impact Dashboard",
                           className="text-center text-primary mb-4")
                ])
            ]),
            
            # Temperature Trends
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Global Temperature Trends"),
                        dbc.CardBody([
                            dcc.Graph(
                                id='temperature-trend',
                                figure=temp_fig
                            )
                        ])
                    ])
                ])
            ]),
            
            # CO2 Emissions
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("CO2 Emissions by Country"),
                        dbc.CardBody([
                            dcc.Graph(
                                id='emissions-trend',
                                figure=emissions_fig
                            )
                        ])
                    ])
                ])
            ]),
            
            # Weather Events
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Extreme Weather Events"),
                        dbc.CardBody([
                            dcc.Graph(
                                id='weather-events',
                                figure=weather_fig
                            )
                        ])
                    ])
                ])
            ])
        ], fluid=True)
        print("Layout created successfully")
except Exception as e:
    print(f"Error creating layout: {e}")
    traceback.print_exc()
    sys.exit(1)

def open_browser():
    webbrowser.open_new('http://localhost:8501/')

if __name__ == '__main__':
    try:
        port = 8501  # Using the same working port as the test app
        print(f"\nStarting server on port {port}...")
        print(f"Dashboard will be available at: http://localhost:{port}")
        print("Press Ctrl+C to quit\n")
        
        # Open the browser after a short delay
        Timer(1.5, open_browser).start()
        
        # Run the server with minimal settings
        app.run_server(
            debug=False,  # Disable debug mode
            port=port,
            host='localhost',
            use_reloader=False  # Disable reloader
        )
    except Exception as e:
        print(f"\nError starting server: {e}")
        traceback.print_exc()
        print("\nTroubleshooting steps:")
        print(f"1. Make sure port {port} is not in use")
        print("2. Check your firewall settings")
        print("3. Make sure you have internet access for loading the Bootstrap theme") 