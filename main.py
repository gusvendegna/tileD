import sqlite3
from flask import Flask, render_template, jsonify, request
import asyncio
from functions import fetchDevices, reverseGeocode, geocodeAddress, initDatabase
import folium

app = Flask(__name__)

@app.route("/")
async def index():

    initDatabase()
    devices = await fetchDevices()
    locations = await getLocations()
    alerts = await getAlerts()
    avg_long = 0
    avg_lat = 0
    
    for device in devices:
        avg_long += device['longitude']
        avg_lat += device['latitude']

    avg_long = avg_long / len(devices)
    avg_lat = avg_lat / len(devices)
    m = folium.Map([avg_lat, avg_long], zoom_start=12)
    for device in devices:
        folium.Marker(
            location=[device['latitude'], device['longitude']],
            tooltip=device['name'],
            popup="Mt. Hood Meadows",
        ).add_to(m)


    
    

    
    

    m.save("static/map.html")


    return render_template('dashboard.html', locations=locations, devices=devices, alerts=alerts)

@app.route("/api/locations")
async def getLocations():
    conn = sqlite3.connect('tiler.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM locations''')
    locations = cursor.fetchall()
    return locations

@app.route("/api/alerts")
async def getAlerts():
    conn = sqlite3.connect('tiler.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM alerts''')
    alerts = cursor.fetchall()
    return alerts

@app.route('/api/createAlert', methods=['POST'])
async def create_alert():
    # Get form data
    device = request.form.get('device')
    alert_name = request.form.get('alert-name')
    distance = request.form.get('distance')
    # convert distance to long/lat
    location = request.form.get('location')

    # Retrieve location details
    locations = await getLocations()

    # parse out target location from db
    location_target = [t for t in locations if t[0] == int(location)][0]

    # Process and save the alert (e.g., to a database)
    conn = sqlite3.connect('tiler.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO alerts (name, device_id, location, type, distance, status)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (alert_name, device, location, 'leave', distance, True))
    conn.commit()
    # Respond with confirmation or details
    response = {
        'status': 'success',
        'data': {
            'device': device,
            'alert_name': alert_name,
            'distance': distance,
            'location': location,

        }
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)