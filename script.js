document.addEventListener('DOMContentLoaded', () => {
    const moodBtns = document.querySelectorAll('.mood-btn');
    const statusMessage = document.getElementById('status-message');
    const loadingEl = document.getElementById('loading');
    const errorEl = document.getElementById('error');
    const resultsContainer = document.getElementById('results-container');
    
    let selectedMood = null;

    // Mood to Backend URL mapping (if applicable, otherwise default to /songs)
    const moodMap = {
        calm: 'calm',
        happy: 'happy',
        focus: 'focus',
        energetic: 'energetic'
    };

    document.querySelectorAll(".mood-btn").forEach(btn => {
        btn.addEventListener('click', () => {
            const mood = btn.getAttribute('data-mood');
            handleMoodSelect(mood, btn);
        });
    });

    function handleMoodSelect(mood, clickedBtn) {
        selectedMood = mood;
        
        // Update Buttons UI
        moodBtns.forEach(b => {
            b.classList.remove('active');
            b.setAttribute('aria-pressed', 'false');
        });
        clickedBtn.classList.add('active');
        clickedBtn.setAttribute('aria-pressed', 'true');

        // Update Theme UI
        document.body.className = `theme-${mood}`;

        // Fetch from backend based on mood
        loadSongs(mood);
    }

    async function loadSongs(mood = null) {
        // Reset View
        if (statusMessage) statusMessage.classList.add('hidden');
        if (errorEl) errorEl.classList.add('hidden');
        resultsContainer.innerHTML = '';
        if (loadingEl) loadingEl.classList.remove('hidden');

        try {
            // If mood is provided, we use a recommend endpoint, otherwise generic songs
            const url = mood 
                ? `http://127.0.0.1:5000/recommend?mood=${encodeURIComponent(mood)}`
                : `http://127.0.0.1:5000/songs`;

            const response = await fetch(url);
            
            if (!response.ok) throw new Error('Backend not responding');
            
            const data = await response.json();
            
            if (loadingEl) loadingEl.classList.add('hidden');
            displaySongs(data);

        } catch (error) {
            console.error(error);
            if (loadingEl) loadingEl.classList.add('hidden');
            showError("Backend not responding");
        }
    }

    function displaySongs(data) {
        if (!data || data.length === 0) {
            if (statusMessage) {
                statusMessage.textContent = 'No songs found.';
                statusMessage.classList.remove('hidden');
            }
            return;
        }

        data.forEach(song => {
            const songCard = document.createElement("div");
            songCard.classList.add("song-card");

            songCard.innerHTML = `
                <div class="song-info">
                    <div class="song-name">${song.song}</div>
                    <div class="artist-name">${song.artist}</div>
                </div>
                <div class="btn-group">
                    <button class="play-btn" onclick="playSong('${song.link}')">Play</button>
                    <button class="play-btn save-btn" onclick="saveSong('${song.song}', '${song.artist}', '${song.link}')">Save</button>
                </div>
            `;

            resultsContainer.appendChild(songCard);
        });
    }

    function showError(message) {
        if (errorEl) {
            errorEl.classList.remove('hidden');
            errorEl.textContent = message;
        }
    }

    // Export internal functions for global scope if needed (though usually defined outside)
    window.loadSongs = loadSongs; 

    // Automatically load songs on startup
    loadSongs();
});

// Functions in global scope for HTML onclick attributes
function playSong(link) {
    if (link && link !== 'undefined') {
        window.open(link, "_blank");
    } else {
        alert("No playback link available for this track.");
    }
}

async function saveSong(song, artist, link) {
    try {
        const response = await fetch("http://127.0.0.1:5000/select-song", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                song: song,
                artist: artist,
                link: link
            })
        });

        if (response.ok) {
            alert("Song saved!");
        } else {
            throw new Error('Save failed');
        }

    } catch (error) {
        console.error("Error saving song:", error);
        alert("Unable to save song. Backend might be offline.");
    }
}
