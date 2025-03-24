from dash import Dash, html

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Test Dashboard'),
    html.P('If you can see this, the dashboard is working!')
])

if __name__ == '__main__':
    print("Starting test server...")
    print("Please open http://127.0.0.1:8050 in your web browser")
    app.run_server(debug=True, host='127.0.0.1', port=8050) 