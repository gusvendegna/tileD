import asyncio
from aiohttp import ClientSession
from pytile import async_login
import requests
import datetime
from requests.structures import CaseInsensitiveDict
import os
from dotenv import load_dotenv
import sqlite3


load_dotenv()

EMAIL = os.getenv('TILE_EMAIL')
PASSWORD = os.getenv('TILE_PASSWORD')

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"



async def fetchDevices():
    """Fetch Tile devices."""
    async with ClientSession() as session:
        api = await async_login(EMAIL, PASSWORD, session)
        conn = sqlite3.connect('tileD.db')
        cursor = conn.cursor()
        tiles = await api.async_get_tiles()
        devices = []
        for tile_uuid, tile in tiles.items():
            device_info = {
                "name": tile.name,
                "longitude": tile.longitude,
                "latitude": tile.latitude,
                "last_timestamp": tile.last_timestamp,
                "uuid": tile.uuid
            }
            devices.append(device_info)

            updated_check = '''
                            SELECT * from device_history 
                            WHERE last_timestamp = ? AND uuid = ?'''
            cursor.execute(updated_check, (tile.last_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f'), tile.uuid,))
            results = cursor.fetchall()
            # print(results)
            if (len(results) > 0):
                # dont add to database if we dont have to
                continue
            else:
                print("new entry to db")
                db_entry = (tile.uuid, tile.name, tile.longitude, tile.latitude, tile.last_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f'))
                cursor.executemany('''
                INSERT INTO device_history (uuid, name, longitude, latitude, last_timestamp)
                VALUES (?, ?, ?, ?, ?)
                ''', [db_entry])
                conn.commit()
        return devices



def reverseGeocode(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1"
    headers = {
        'User-Agent': 'YourAppName/1.0 (bob@gmail.com)'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('display_name')
    else:
        return None

async def geocodeAddress(address):
    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1"
    print(url)
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data:
                    return {
                        "latitude": data[0]['lat'],
                        "longitude": data[0]['lon']
                    }
                else:
                    return None
            else:
                return None

async def createHistoryMap(device_id):
    conn = sqlite3.connect('tileD.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM device_history 
                   WHERE uuid = ?
                   ORDER BY id DESC
                   LIMIT 10''')
    location_history = cursor.fetchall()
    print(location_history)




def initDatabase():
    conn = sqlite3.connect('tileD.db')
    cursor = conn.cursor()
    # Create a table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        longitude REAL NOT NULL,
        latitude REAL NOT NULL,
        address TEXT,
        description TEXT
    );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS device_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uuid TEXT NOT NULL,
        name TEXT NOT NULL,
        longitude REAL NOT NULL,
        latitude REAL NOT NULL,
        address TEXT,
        last_timestamp DATETIME
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        device_id TEXT NOT NULL,
        location INTEGER REFERENCES locations(id) NOT NULL,
        type TEXT DEFAULT 'leave' NOT NULL,
        distance INTEGER NOT NULL,
        status BOOLEAN NOT NULL
    );
    ''')

    conn.commit()

# def createAlert():
