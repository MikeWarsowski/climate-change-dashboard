print("Starting callback application...")

import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Initialize the app
app = dash.Dash(__name__)

# Define the layout first
app.layout = html.Div([
    html.H1("Climate Change Dashboard", style={'textAlign': 'center'}),
    
    # Hidden div for triggering callbacks
    html.Div(id='trigger', style={'display': 'none'}),
    
    # Temperature Section
    html.Div([
        html.H2("Temperature Trends"),
        dcc.Graph(id='temperature-graph')
    ]),
    
    # Emissions Section
    html.Div([
        html.H2("CO2 Emissions"),
        dcc.Graph(id='emissions-graph')
    ]),
    
    # Weather Section
    html.Div([
        html.H2("Weather Events"),
        dcc.Graph(id='weather-graph')
    ])
])

@app.callback(
    Output('temperature-graph', 'figure'),
    Input('trigger', 'children')
)
def update_temperature_graph(_):
    print("Loading temperature data...")
    df = pd.read_csv('data/temperature_data.csv')
    fig = px.line(df, x='Year', y='Temperature', color='Type',
                  title='Global Temperature Trends')
    return fig

@app.callback(
    Output('emissions-graph', 'figure'),
    Input('trigger', 'children')
)
def update_emissions_graph(_):
    print("Loading emissions data...")
    df = pd.read_csv('data/emissions_data.csv')
    
    fig = go.Figure()
    for country in ['United States', 'China', 'India', 'Russian Federation', 'Japan']:
        country_data = df[df['country'] == country]
        fig.add_trace(
            go.Scatter(
                x=country_data['year'],
                y=country_data['co2'],
                name=country,
                mode='lines+markers'
            )
        )
    
    fig.update_layout(
        title='CO2 Emissions by Country',
        xaxis_title='Year',
        yaxis_title='CO2 Emissions',
        showlegend=True
    )
    return fig

@app.callback(
    Output('weather-graph', 'figure'),
    Input('trigger', 'children')
)
def update_weather_graph(_):
    print("Loading weather data...")
    df = pd.read_csv('data/weather_events.csv')
    
    fig = go.Figure()
    for event in df['Event_Type'].unique():
        event_data = df[df['Event_Type'] == event]
        fig.add_trace(
            go.Scatter(
                x=event_data['Year'],
                y=event_data['Count'],
                name=event,
                mode='lines+markers'
            )
        )
    
    fig.update_layout(
        title='Weather Events Over Time',
        xaxis_title='Year',
        yaxis_title='Number of Events',
        showlegend=True
    )
    return fig

if __name__ == '__main__':
    print("\nStarting server on port 8502...")  # Using a different port
    print("Dashboard will be available at: http://localhost:8502")
    print("Press Ctrl+C to quit\n")
    
    app.run_server(debug=True, port=8502, host='localhost') 