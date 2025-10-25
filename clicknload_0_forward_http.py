import http.server
import requests # pip install requests
from urllib.parse import urlparse

LISTEN_PORT = 9666  # Der Zielport
# Ziel-IP und -Port für die Weiterleitung
TARGET_IP = "192.168.0.201"
TARGET_PORT = LISTEN_PORT  # Der Zielport

class SimpleProxyHandler(http.server.BaseHTTPRequestHandler):
    def send_cors_headers(self):
        """Sende CORS-Header für alle Antworten"""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Credentials", "true")

    def do_OPTIONS(self):
        """Handle CORS preflight request"""
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        """Handle GET-Anfragen"""
        target_url = f"http://{TARGET_IP}:{TARGET_PORT}{self.path}"

        try:
            # An die Ziel-URL weiterleiten
            response = requests.get(target_url, headers=self.headers)

            # Setze den Statuscode der Antwort
            self.send_response(response.status_code)
            
            # CORS Header setzen
            self.send_cors_headers()
            self.end_headers()

            # Schicke den Inhalt der Antwort zurück
            self.wfile.write(response.content)
        except requests.exceptions.RequestException as e:
            self.send_response(500)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(f"Fehler bei der Weiterleitung: {e}".encode())

    def do_POST(self):
        """Handle POST-Anfragen"""
        target_url = f"http://{TARGET_IP}:{TARGET_PORT}{self.path}"

        try:
            content_length = int(self.headers['Content-Length'])  # Hole die Länge des Post-Body
            post_data = self.rfile.read(content_length)  # Lese die Post-Daten

            # An die Ziel-URL weiterleiten
            response = requests.post(target_url, data=post_data, headers=self.headers)

            # Setze den Statuscode der Antwort
            self.send_response(response.status_code)
            
            # CORS Header setzen
            self.send_cors_headers()
            self.end_headers()

            # Schicke den Inhalt der Antwort zurück
            self.wfile.write(response.content)
        except requests.exceptions.RequestException as e:
            self.send_response(500)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(f"Fehler bei der Weiterleitung: {e}".encode())

# Starte den HTTP-Server
def run(server_class=http.server.HTTPServer, handler_class=SimpleProxyHandler, port=8080):
    server_address = ('', port)  # Lokale Adresse und der Port, auf dem der Server läuft
    httpd = server_class(server_address, handler_class)
    print(f"Proxy-Server läuft auf http://localhost:{port}")
    print(f"Forwarding to http://{TARGET_IP}:{TARGET_PORT}")
    httpd.serve_forever()

if __name__ == '__main__':
    run(port=LISTEN_PORT)
