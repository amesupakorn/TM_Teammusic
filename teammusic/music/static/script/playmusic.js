let audio = null; // ประกาศตัวแปร audio สำหรับควบคุมการเล่นเพลง
let isPlaying = false;

function playSong(title, album, albumCover, singer, songUrl) {
    // ส่งข้อมูลเพลงไปยังเซสชันผ่าน AJAX
    fetch("/teammusic/set_song_session/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'  // ส่ง CSRF Token
        },
        body: JSON.stringify({
            'title': title,
            'album': album,
            'albumCover': albumCover,
            'singer': singer
        })
    }).then(response => {
        if (response.ok) {
            console.log("Song data added to session");
            openPlayer(title, album, albumCover, singer, songUrl);
        } else {
            console.error("Failed to set song in session");
        }
    });
}

function openPlayer(title, album, albumCover, singer, songUrl) {
    // อัพเดตข้อมูลใน player control
    document.getElementById("playerSongTitle").textContent = title;
    document.getElementById("playerAlbumInfo").textContent = `${singer} - ${album}`;
    document.getElementById("playerAlbumCover").src = albumCover;

    // สร้าง audio object ใหม่สำหรับเล่นเพลง
    if (audio) {
        audio.pause(); // หยุดเพลงเก่าหากกำลังเล่นอยู่
    }
    audio = new Audio(songUrl);
    audio.play();
    isPlaying = true;

    // แสดง player control
    document.getElementById("playerControl").classList.remove("hidden");
    updatePlayPauseIcon();
}

function togglePlayPause() {
    if (audio) {
        if (isPlaying) {
            audio.pause();
        } else {
            audio.play();
        }
        isPlaying = !isPlaying;
        updatePlayPauseIcon();
    }
}

function updatePlayPauseIcon() {
    const playPauseButton = document.getElementById("playPauseButton");
    const playIcon = `
        <svg class="h-8 w-8 text-white" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="5 3 19 12 5 21 5 3" />
        </svg>
    `;
    const pauseIcon = `
        <svg class="h-8 w-8 text-white" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="6" y="4" width="4" height="16"></rect>
            <rect x="14" y="4" width="4" height="16"></rect>
        </svg>
    `;
    playPauseButton.innerHTML = isPlaying ? pauseIcon : playIcon;
}

function previousSong() {
    console.log("Previous song");
    // ใส่ logic การเล่นเพลงก่อนหน้า
}

function nextSong() {
    console.log("Next song");
    // ใส่ logic การเล่นเพลงถัดไป
}
