import os
import sqlite3
from dotenv import load_dotenv

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
        print(alert)
        cursor.execute('''
            SELECT * FROM device_history
            WHERE uuid = ?
            LIMIT 1''', (str(alert[1]),))
        location = cursor.fetchone()
        print(location)
    cursor.close()
    
    print(DISCORD_WEBHOOK_URL)
    