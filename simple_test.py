from dash import Dash, html
import sys

try:
    app = Dash(__name__)
    print("Dash app created successfully")
except Exception as e:
    print(f"Error creating Dash app: {e}")
    sys.exit(1)

try:
    app.layout = html.Div([
        html.H1('Simple Test'),
        html.P('Basic test page')
    ])
    print("Layout created successfully")
except Exception as e:
    print(f"Error creating layout: {e}")
    sys.exit(1)

if __name__ == '__main__':
    try:
        port = 8501  # Using a different port
        print(f"\nAttempting to start server on port {port}...")
        print(f"Once started, open http://localhost:{port} in your web browser")
        print("Press Ctrl+C to quit\n")
        
        app.run_server(
            debug=True,
            port=port,
            host='localhost'  # Using localhost instead of 127.0.0.1
        )
    except Exception as e:
        print(f"\nError starting server: {e}")
        print("\nPlease try:")
        print(f"1. Make sure port {port} is not in use")
        print("2. Check your firewall settings")
        print("3. Verify you have an active internet connection") 