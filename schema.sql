/* 
1. Open SQL Server Management Studio (SSMS).
2. Create a new database (e.g., MoodMusicDB).
3. Open a New Query and run the code below: 
*/

CREATE TABLE SavedSongs (
    id INT IDENTITY(1,1) PRIMARY KEY,
    song_name NVARCHAR(255) NOT NULL,
    artist_name NVARCHAR(255) NOT NULL,
    spotify_link NVARCHAR(MAX),
    created_at DATETIME DEFAULT GETDATE()
);

-- Optional: Insert a test song
-- INSERT INTO SavedSongs (song_name, artist_name, spotify_link) 
-- VALUES ('Midnight City', 'M83', 'https://open.spotify.com/track/1eyzqe2QqGZUmfc2Pdv9qC');
