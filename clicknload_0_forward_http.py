# This script shall help you after4 you outsorced your Jdownloader2 from your local machine to a remote instance.
# It will simulate a CORS-relaxed Webserver, receiving and forwarding all ClickNLoad requests
# There is no logic to decrypt any link or interfere with them
# Your remote JDownloader2 Instance must be configured to recfeive ClickNLoad on Port 9666 (or whatever you specify)
# 
# Bonus:
# If you paste links into the runing script, it will send them to the depricated API (NOT ClickNLoad) usually running on port 3128
import threading
import http.server
import requests # pip install requests
from urllib.parse import urlparse

LISTEN_PORT = 9666  # Der Zielport
# Ziel-IP und -Port für die Weiterleitung
TARGET_IP = "192.168.0.201"
TARGET_PORT_CLICKNLOAD = LISTEN_PORT  # ClickNLoad crypted stuff
TARGET_PORT_API= 3128  # plain API for sending links

JD_API = f"http://{TARGET_IP}:{TARGET_PORT_API}/linkgrabberv2/addLinks"

def cli_input_loop():
    # this loop receives URLs by keyboard-interactive and forwards them plaintext to the depcricated Jwodnloader2 API
    print("CLI aktiv – einfach Link eingeben und ENTER drücken:")
    while True:
        link = input("> ").strip()
        if link.startswith("http"):
            try:
                r = requests.post(JD_API, json={"links": link})
                print("▶ JD:", r.status_code, r.text)
            except Exception as e:
                print("Fehler:", e)
        else:
            print("Kein gültiger Link")


class SimpleProxyHandler(http.server.BaseHTTPRequestHandler):
    # this will act as "dumb" proxy between your local machine and the remote Jdownloader2 instance.
    # It will forward all requests there without understanding or decrypting them
    # when active, it will seem like your JDownloader2 ClickNLoad is running locally
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
        target_url = f"http://{TARGET_IP}:{TARGET_PORT_CLICKNLOAD}{self.path}"

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
        target_url = f"http://{TARGET_IP}:{TARGET_PORT_CLICKNLOAD}{self.path}"

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

def run(server_class=http.server.HTTPServer, handler_class=SimpleProxyHandler, port=8080):
    # Start CLI thread to receive plaintext links by keyboard
    threading.Thread(target=cli_input_loop, daemon=True).start()

    # Starte den HTTP-Server
    server_address = ('', port)  # Lokale Adresse und der Port, auf dem der Server läuft
    httpd = server_class(server_address, handler_class)
    print(f"Proxy-Server läuft auf http://localhost:{port}")
    print(f"Forwarding to http://{TARGET_IP}:{TARGET_PORT_CLICKNLOAD}")
    httpd.serve_forever()

if __name__ == '__main__':
    run(port=LISTEN_PORT)
