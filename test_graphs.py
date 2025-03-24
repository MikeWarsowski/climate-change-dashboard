print("Starting test graphs...")

import dash
from dash import html, dcc
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load emissions data
print("\nLoading emissions data...")
emissions_df = pd.read_csv('data/emissions_data.csv')
print(f"Emissions data loaded with shape: {emissions_df.shape}")

# Create emissions figure
emissions_fig = go.Figure()
for country in ['United States', 'China', 'India', 'Russian Federation', 'Japan']:
    df_country = emissions_df[emissions_df['country'] == country]
    emissions_fig.add_trace(
        go.Scatter(
            x=df_country['year'],
            y=df_country['co2'],
            name=country,
            mode='lines+markers'
        )
    )
emissions_fig.update_layout(
    title='CO2 Emissions by Country',
    xaxis_title='Year',
    yaxis_title='CO2 Emissions',
    showlegend=True
)

# Load weather data
print("\nLoading weather data...")
weather_df = pd.read_csv('data/weather_events.csv')
print(f"Weather data loaded with shape: {weather_df.shape}")

# Create weather figure
weather_fig = go.Figure()
for event in weather_df['Event_Type'].unique():
    df_event = weather_df[weather_df['Event_Type'] == event]
    weather_fig.add_trace(
        go.Scatter(
            x=df_event['Year'],
            y=df_event['Count'],
            name=event,
            mode='lines+markers'
        )
    )
weather_fig.update_layout(
    title='Weather Events Over Time',
    xaxis_title='Year',
    yaxis_title='Number of Events',
    showlegend=True
)

# Create layout
app.layout = html.Div([
    html.H1("Test Graphs", style={'textAlign': 'center', 'marginBottom': 30}),
    
    # Emissions Graph
    html.Div([
        html.H2("CO2 Emissions", style={'textAlign': 'center'}),
        dcc.Graph(
            id='emissions-graph',
            figure=emissions_fig,
            style={'height': '500px'}
        )
    ], style={'marginBottom': 50}),
    
    # Weather Graph
    html.Div([
        html.H2("Weather Events", style={'textAlign': 'center'}),
        dcc.Graph(
            id='weather-graph',
            figure=weather_fig,
            style={'height': '500px'}
        )
    ])
])

if __name__ == '__main__':
    print("\nStarting server on port 8502...")  # Using a different port
    print("Dashboard will be available at: http://localhost:8502")
    print("Press Ctrl+C to quit\n")
    
    app.run_server(debug=False, port=8502, host='localhost') 