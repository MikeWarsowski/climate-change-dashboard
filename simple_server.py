from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8050):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    local_ip = get_ip()
    print(f"Server started at:")
    print(f"* Local: http://localhost:{port}")
    print(f"* Network: http://{local_ip}:{port}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()

if __name__ == '__main__':
    run() 