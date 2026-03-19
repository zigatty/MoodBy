from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64
import pyodbc  # Required for MSSQL

app = Flask(__name__)
CORS(app)

# ---------------------------------------------------------
# DATABASE CONFIGURATION
# ---------------------------------------------------------
# Update these values to match your local system
DB_CONFIG = {
    "server": "YOUR_SERVER_NAME",        # e.g., "localhost" or ".\SQLEXPRESS"
    "database": "MoodMusicDB",           # The database you created
    "driver": "{ODBC Driver 17 for SQL Server}" # Ensure this driver is installed
}

def get_db_connection():
    # Using Windows Authentication (Trusted_Connection=yes)
    conn_str = (
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)

# ---------------------------------------------------------
# SPOTIFY CONFIGURATION
# ---------------------------------------------------------
CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID'
CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET'

MOOD_MAP = {
    'calm': 'acoustic chill ambient',
    'happy': 'happy pop upbeat',
    'focus': 'lofi study focus classical',
    'energetic': 'energetic dance workout rock'
}

def get_spotify_token():
    try:
        auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
        auth_base64 = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={"Authorization": f"Basic {auth_base64}", "Content-Type": "application/x-www-form-urlencoded"},
            data={"grant_type": "client_credentials"}
        )
        return response.json().get('access_token') if response.status_code == 200 else None
    except Exception as e:
        print(f"Token Error: {e}")
        return None

# ---------------------------------------------------------
# ENDPOINTS
# ---------------------------------------------------------

@app.route('/recommend', methods=['GET'])
def recommend():
    mood = request.args.get('mood', '').lower()
    query = MOOD_MAP.get(mood, 'pop')
    token = get_spotify_token()
    if not token: return jsonify({"error": "Spotify Auth Failed"}), 500
    
    headers = {"Authorization": f"Bearer {token}"}
    params = {'q': query, 'type': 'track', 'limit': 10}
    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        tracks = data.get('tracks', {}).get('items', [])
        return jsonify([{"song": t['name'], "artist": ", ".join([a['name'] for a in t['artists']]), "link": t['external_urls']['spotify']} for t in tracks])
    return jsonify({"error": "Spotify Search Failed"}), response.status_code

@app.route('/songs', methods=['GET'])
def get_all_songs():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT song_name, artist_name, spotify_link FROM SavedSongs ORDER BY created_at DESC")
        rows = cursor.fetchall()
        songs = [{"song": r[0], "artist": r[1], "link": r[2]} for r in rows]
        conn.close()
        return jsonify(songs)
    except Exception as e:
        print(f"DB Fetch Error: {e}")
        return jsonify({"error": "Database error"}), 500

@app.route('/select-song', methods=['POST'])
def select_song():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO SavedSongs (song_name, artist_name, spotify_link) VALUES (?, ?, ?)",
            (data.get('song'), data.get('artist'), data.get('link'))
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Song saved to MSSQL"}), 200
    except Exception as e:
        print(f"DB Insert Error: {e}")
        return jsonify({"error": "Could not save song"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
