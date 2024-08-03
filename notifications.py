import os
import sqlite3
from dotenv import load_dotenv
import math
from discord_webhook import DiscordWebhook

earth_radius = 3960.0
degrees_to_radians = math.pi/180.0
radians_to_degrees = 180.0/math.pi

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

def checkNotifications():
    conn = sqlite3.connect('tileD.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT alerts.name, alerts.device_id, alerts.distance, locations.longitude, locations.latitude FROM alerts
        JOIN locations ON locations.id=alerts.location
        WHERE alerts.status = true''')
    alerts = cursor.fetchall()
    for alert in alerts:
        cursor.execute('''
            SELECT * FROM device_history
            WHERE uuid = ?
            LIMIT 1''', (str(alert[1]),))
        location = cursor.fetchone()
        long_tol = change_in_longitude(location[3], alert[2])
        lat_tol = change_in_latitude(alert[3])
        if (abs(alert[3]) + abs(long_tol) <= location[3] or abs(alert[4]) + abs(lat_tol) <= location[4]):
            # this one is fine
            content = (f"ALERT. {alert[0]} has been triggered.\nPlease log into the TileD webapp to see your device on a map.")
            webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=content)
            response = webhook.execute()
    cursor.close()
    




def change_in_latitude(miles):
    "Given a distance north, return the change in latitude."
    return (miles/earth_radius)*radians_to_degrees

def change_in_longitude(latitude, miles):
    "Given a latitude and a distance west, return the change in longitude."
    # Find the radius of a circle around the earth at given latitude.
    r = earth_radius*math.cos(latitude*degrees_to_radians)
    return (miles/r)*radians_to_degrees