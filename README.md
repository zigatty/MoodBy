# 🎵 Mood-Based Music Recommendation App

A simple full-stack application that recommends music based on user mood using **Spotify API**, allows playback, and stores selected songs in **MSSQL**.

---

## 🚀 Features

* 🎯 Select mood (Calm, Happy, Focus, Energetic)
* 🎧 Fetch songs from Spotify
* ▶️ Play songs directly on Spotify
* 💾 Save selected songs to MSSQL database
* 🌐 Simple frontend using HTML, CSS, JavaScript
* ⚙️ Backend powered by Flask (Python)

---

## 🛠️ Tech Stack

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Python (Flask)
* **Database:** Microsoft SQL Server (MSSQL)
* **API:** Spotify Web API

---

## 📂 Project Structure

```
project-folder/
│
├── app.py              # Flask backend
├── index.html          # Frontend UI
├── script.js           # Frontend logic
├── styles.css          # Styling
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```
git clone https://github.com/your-username/mood-music-app.git
cd mood-music-app
```

---

### 2️⃣ Install Dependencies

```
pip install flask flask-cors pyodbc requests
```

---

### 3️⃣ Configure Spotify API

* Go to: https://developer.spotify.com/dashboard
* Create an app
* Copy:

  * Client ID
  * Client Secret

Update in `app.py`:

```
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
```

---

### 4️⃣ Setup MSSQL Database

Create table:

```
CREATE TABLE user_selections (
    id INT IDENTITY(1,1) PRIMARY KEY,
    song VARCHAR(255),
    artist VARCHAR(255),
    link VARCHAR(500)
);
```

Update DB credentials in `app.py`:

```
SERVER=localhost;
DATABASE=your_db_name;
UID=your_username;
PWD=your_password;
```

---

### 5️⃣ Run Backend

```
python app.py
```

Server runs at:

```
http://127.0.0.1:5000
```

---

### 6️⃣ Run Frontend

```
python -m http.server 5500
```

Open:

```
http://127.0.0.1:5500
```

---

## 🔄 API Endpoints

### 🎵 Get Songs

```
GET /songs
```

Returns list of songs from Spotify

---

### 💾 Save Song

```
POST /select-song
```

Body:

```
{
  "song": "Song Name",
  "artist": "Artist Name",
  "link": "Spotify URL"
}
```

---

## 🎯 How It Works

1. User selects a mood
2. Frontend sends request to Flask backend
3. Backend fetches songs from Spotify
4. Songs displayed in UI
5. User can:

   * ▶️ Play song
   * 💾 Save song to database

---

## ⚠️ Notes

* Uses Spotify Search API (no premium required)
* Ensure Flask server is running before frontend
* Enable CORS in backend

---

## 📌 Future Improvements

* Mood-based dynamic filtering
* User authentication
* Playlist creation
* Deployment to cloud

---

## 👨‍💻 Author

Your Name

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
