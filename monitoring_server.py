from flask import Flask, jsonify, render_template
import psutil
import threading
import time

app = Flask(__name__)

# Daten für Monitoring speichern
monitor_data = {
    "cpu_usage": 0,
    "ram_usage": 0,
    "network_sent": 0,
    "network_received": 0,
    "disk_usage": 0
}

def monitor_system():
    """Überwacht CPU-, RAM-, Netzwerk- und Festplattenauslastung und aktualisiert die Daten."""
    global monitor_data
    previous_net_io = psutil.net_io_counters()  # Startwerte für Netzwerküberwachung
    while True:
        # CPU- und RAM-Nutzung
        monitor_data["cpu_usage"] = psutil.cpu_percent(interval=1)
        monitor_data["ram_usage"] = psutil.virtual_memory().percent

        # Netzwerk-Nutzung (in kB/s)
        current_net_io = psutil.net_io_counters()
        monitor_data["network_sent"] = (current_net_io.bytes_sent - previous_net_io.bytes_sent) / 1024
        monitor_data["network_received"] = (current_net_io.bytes_recv - previous_net_io.bytes_recv) / 1024
        previous_net_io = current_net_io

        # Festplattennutzung
        monitor_data["disk_usage"] = psutil.disk_usage('/').percent

        time.sleep(1)  # Aktualisierung alle 1 Sekunde

# API-Endpunkt für Monitoring-Daten
@app.route('/api/monitoring')
def get_monitoring_data():
    return jsonify(monitor_data)

# Route für die Website
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Monitoring in einem separaten Thread ausführen
    monitor_thread = threading.Thread(target=monitor_system, daemon=True)
    monitor_thread.start()
    app.run(debug=True)
