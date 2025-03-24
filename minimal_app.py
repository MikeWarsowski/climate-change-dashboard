print("Starting minimal application...")

import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from datetime import datetime

# Initialize the app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout with Bootstrap components
app.layout = dbc.Container([
    # Interval component for triggering initial load
    dcc.Interval(
        id='interval-component',
        interval=1*1000,
        n_intervals=0,
        max_intervals=1
    ),
    
    # Store components for holding data
    dcc.Store(id='temperature-data-store'),
    dcc.Store(id='emissions-data-store'),
    dcc.Store(id='weather-data-store'),
    
    # Header
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
                    html.P("This graph shows the historical temperature trends and future predictions."),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Select Date Range:"),
                            dcc.RangeSlider(
                                id='temperature-year-slider',
                                min=1880,
                                max=2024,
                                value=[1880, 2024],
                                marks={
                                    1880: '1880',
                                    1920: '1920',
                                    1960: '1960',
                                    2000: '2000',
                                    2024: '2024'
                                }
                            )
                        ])
                    ], className="mb-3"),
                    dcc.Loading(
                        id="loading-temperature",
                        type="default",
                        children=dcc.Graph(
                            id='temperature-graph',
                            style={'height': '400px'}
                        )
                    )
                ])
            ], className="mb-4")
        ])
    ]),
    
    # CO2 Emissions
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("CO2 Emissions by Major Countries"),
                dbc.CardBody([
                    html.P("This graph shows CO2 emissions trends for major countries over time."),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Select Countries:"),
                            dcc.Dropdown(
                                id='country-selector',
                                multi=True,
                                value=['United States', 'China', 'India', 'Russian Federation', 'Japan'],
                                placeholder="Select countries to display"
                            )
                        ], width=6),
                        dbc.Col([
                            html.Label("Select Year Range:"),
                            dcc.RangeSlider(
                                id='emissions-year-slider',
                                min=1950,
                                max=2024,
                                value=[1950, 2024],
                                marks={
                                    1950: '1950',
                                    1970: '1970',
                                    1990: '1990',
                                    2010: '2010',
                                    2024: '2024'
                                }
                            )
                        ], width=6)
                    ], className="mb-3"),
                    dcc.Loading(
                        id="loading-emissions",
                        type="default",
                        children=dcc.Graph(
                            id='emissions-graph',
                            style={'height': '400px'}
                        )
                    )
                ])
            ], className="mb-4")
        ])
    ]),
    
    # Weather Events
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Extreme Weather Events"),
                dbc.CardBody([
                    html.P("This graph shows the frequency of different types of extreme weather events over time."),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Select Event Types:"),
                            dcc.Dropdown(
                                id='event-type-selector',
                                multi=True,
                                placeholder="Select event types to display"
                            )
                        ], width=6),
                        dbc.Col([
                            html.Label("Select Year Range:"),
                            dcc.RangeSlider(
                                id='weather-year-slider',
                                min=1950,
                                max=2024,
                                value=[1950, 2024],
                                marks={
                                    1950: '1950',
                                    1970: '1970',
                                    1990: '1990',
                                    2010: '2010',
                                    2024: '2024'
                                }
                            )
                        ], width=6)
                    ], className="mb-3"),
                    dcc.Loading(
                        id="loading-weather",
                        type="default",
                        children=dcc.Graph(
                            id='weather-graph',
                            style={'height': '400px'}
                        )
                    )
                ])
            ], className="mb-4")
        ])
    ])
], fluid=True, className="p-4")

# Callback to load initial data
@app.callback(
    [Output('temperature-data-store', 'data'),
     Output('emissions-data-store', 'data'),
     Output('weather-data-store', 'data'),
     Output('country-selector', 'options'),
     Output('event-type-selector', 'options'),
     Output('event-type-selector', 'value')],
    Input('interval-component', 'n_intervals')
)
def load_data(_):
    print("Loading initial data...")
    # Load temperature data
    temp_df = pd.read_csv('data/temperature_data.csv')
    
    # Load emissions data
    emissions_df = pd.read_csv('data/emissions_data.csv')
    countries = sorted(emissions_df['country'].unique())
    country_options = [{'label': country, 'value': country} for country in countries]
    
    # Load weather data
    weather_df = pd.read_csv('data/weather_events.csv')
    event_types = sorted(weather_df['Event_Type'].unique())
    event_options = [{'label': event, 'value': event} for event in event_types]
    
    return (temp_df.to_dict('records'), 
            emissions_df.to_dict('records'),
            weather_df.to_dict('records'),
            country_options,
            event_options,
            event_types)  # Select all event types by default

@app.callback(
    Output('temperature-graph', 'figure'),
    [Input('temperature-data-store', 'data'),
     Input('temperature-year-slider', 'value')]
)
def update_temperature_graph(data, years):
    print("Updating temperature graph...")
    if not data:
        return {}
    
    df = pd.DataFrame(data)
    df = df[(df['Year'] >= years[0]) & (df['Year'] <= years[1])]
    
    fig = px.line(df, x='Year', y='Temperature', color='Type',
                  title=f'Global Temperature Trends ({years[0]}-{years[1]})')
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Temperature (°C)",
        showlegend=True
    )
    return fig

@app.callback(
    Output('emissions-graph', 'figure'),
    [Input('emissions-data-store', 'data'),
     Input('country-selector', 'value'),
     Input('emissions-year-slider', 'value')]
)
def update_emissions_graph(data, selected_countries, years):
    print("Updating emissions graph...")
    if not data or not selected_countries:
        return {}
    
    df = pd.DataFrame(data)
    df = df[(df['year'] >= years[0]) & (df['year'] <= years[1])]
    
    fig = go.Figure()
    for country in selected_countries:
        country_data = df[df['country'] == country]
        if not country_data.empty:
            fig.add_trace(
                go.Scatter(
                    x=country_data['year'],
                    y=country_data['co2'],
                    name=country,
                    mode='lines+markers'
                )
            )
    
    fig.update_layout(
        title=f'CO2 Emissions by Country ({years[0]}-{years[1]})',
        xaxis_title='Year',
        yaxis_title='CO2 Emissions (million tonnes)',
        showlegend=True
    )
    return fig

@app.callback(
    Output('weather-graph', 'figure'),
    [Input('weather-data-store', 'data'),
     Input('event-type-selector', 'value'),
     Input('weather-year-slider', 'value')]
)
def update_weather_graph(data, selected_events, years):
    print("Updating weather graph...")
    if not data or not selected_events:
        return {}
    
    df = pd.DataFrame(data)
    df = df[(df['Year'] >= years[0]) & (df['Year'] <= years[1])]
    
    fig = go.Figure()
    for event in selected_events:
        event_data = df[df['Event_Type'] == event]
        if not event_data.empty:
            fig.add_trace(
                go.Scatter(
                    x=event_data['Year'],
                    y=event_data['Count'],
                    name=event,
                    mode='lines+markers'
                )
            )
    
    fig.update_layout(
        title=f'Weather Events Over Time ({years[0]}-{years[1]})',
        xaxis_title='Year',
        yaxis_title='Number of Events',
        showlegend=True
    )
    return fig

if __name__ == '__main__':
    print("\nStarting server on port 8501...")
    print("Dashboard will be available at: http://localhost:8501")
    print("Press Ctrl+C to quit\n")
    
    app.run_server(
        debug=True,
        port=8501,
        host='localhost'
    ) 