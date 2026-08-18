/**
 * Deming Luna Mimbres Museum - Audio Guide App
 */
let currentRoomId = 1;
let roomsData = [];
let audioInstance = null;
let isPlaying = false;

document.addEventListener('DOMContentLoaded', async () => {
  await loadRoomsData();
  parseUrlRoomParam();
  setupEventListeners();
  renderRoom(currentRoomId);
});

async function loadRoomsData() {
  try {
    const res = await fetch('data/rooms.json');
    roomsData = await res.json();
    populateRoomDropdown();
  } catch (err) {
    console.error('Failed to load rooms.json:', err);
  }
}

function parseUrlRoomParam() {
  const urlParams = new URLSearchParams(window.location.search);
  const roomParam = parseInt(urlParams.get('room'), 10);
  if (roomParam && roomParam >= 1 && roomParam <= 15) {
    currentRoomId = roomParam;
  }
}

function populateRoomDropdown() {
  const selectEl = document.getElementById('roomSelect');
  if (!selectEl) return;
  selectEl.innerHTML = '';
  roomsData.forEach((room) => {
    const opt = document.createElement('option');
    opt.value = room.id;
    opt.textContent = `Room ${room.id}: ${room.title}`;
    selectEl.appendChild(opt);
  });
  selectEl.value = currentRoomId;
}

function renderRoom(id) {
  const room = roomsData.find((r) => r.id === id);
  if (!room) return;

  currentRoomId = id;
  
  // Update URL search param without reload
  const newUrl = `${window.location.pathname}?room=${id}`;
  window.history.replaceState({ path: newUrl }, '', newUrl);

  // Update UI Elements
  document.getElementById('roomBadge').textContent = `Room ${room.id} of 15`;
  document.getElementById('exhibitTitle').textContent = room.title;
  document.getElementById('exhibitSubtitle').textContent = room.subtitle;
  document.getElementById('transcriptText').textContent = room.transcript;
  document.getElementById('totalTimeDisplay').textContent = room.duration || '2:00';
  document.getElementById('currentTimeDisplay').textContent = '0:00';
  document.getElementById('progressBarFill').style.width = '0%';
  document.getElementById('roomSelect').value = id;

  // Render Highlights Pills
  const pillsContainer = document.getElementById('highlightsPills');
  pillsContainer.innerHTML = '';
  if (room.highlights && room.highlights.length) {
    room.highlights.forEach((h) => {
      const pill = document.createElement('span');
      pill.className = 'pill';
      pill.textContent = h;
      pillsContainer.appendChild(pill);
    });
  }

  // Update Navigation Buttons
  document.getElementById('btnPrevRoom').disabled = id === 1;
  document.getElementById('btnNextRoom').disabled = id === 15;

  // Reset Audio
  stopAudio();
}

function setupEventListeners() {
  document.getElementById('roomSelect').addEventListener('change', (e) => {
    renderRoom(parseInt(e.target.value, 10));
  });

  document.getElementById('btnPrevRoom').addEventListener('click', () => {
    if (currentRoomId > 1) renderRoom(currentRoomId - 1);
  });

  document.getElementById('btnNextRoom').addEventListener('click', () => {
    if (currentRoomId < 15) renderRoom(currentRoomId + 1);
  });

  document.getElementById('btnPlayPause').addEventListener('click', toggleAudio);
}

// Audio Playback Handler
let playInterval = null;
let playTimeSeconds = 0;

function toggleAudio() {
  if (isPlaying) {
    pauseAudio();
  } else {
    playAudio();
  }
}

function playAudio() {
  isPlaying = true;
  updatePlayPauseIcon();

  // Try real HTML5 audio or synthesize speech demo
  const room = roomsData.find((r) => r.id === currentRoomId);
  if (!audioInstance) {
    audioInstance = new Audio(room.audio);
    audioInstance.addEventListener('ended', onAudioEnded);
  }

  audioInstance.play().catch(() => {
    // Fallback speech synthesis demo if MP3 file doesn't exist yet
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(room.transcript);
      utterance.rate = 0.95;
      utterance.onend = onAudioEnded;
      window.speechSynthesis.speak(utterance);
    }
  });

  // Simulated progress timer
  if (playInterval) clearInterval(playInterval);
  playInterval = setInterval(() => {
    playTimeSeconds += 1;
    const totalSecs = 115; // default 1:55
    const pct = Math.min((playTimeSeconds / totalSecs) * 100, 100);
    document.getElementById('progressBarFill').style.width = `${pct}%`;
    document.getElementById('currentTimeDisplay').textContent = formatSeconds(playTimeSeconds);
    if (pct >= 100) {
      onAudioEnded();
    }
  }, 1000);
}

function pauseAudio() {
  isPlaying = false;
  updatePlayPauseIcon();
  if (audioInstance) audioInstance.pause();
  if ('speechSynthesis' in window) window.speechSynthesis.pause();
  if (playInterval) clearInterval(playInterval);
}

function stopAudio() {
  pauseAudio();
  playTimeSeconds = 0;
  if (audioInstance) {
    audioInstance.currentTime = 0;
    audioInstance = null;
  }
  if ('speechSynthesis' in window) window.speechSynthesis.cancel();
  document.getElementById('progressBarFill').style.width = '0%';
  document.getElementById('currentTimeDisplay').textContent = '0:00';
}

function onAudioEnded() {
  isPlaying = false;
  updatePlayPauseIcon();
  if (playInterval) clearInterval(playInterval);
  playTimeSeconds = 0;
}

function updatePlayPauseIcon() {
  const btn = document.getElementById('btnPlayPause');
  if (isPlaying) {
    btn.innerHTML = `<svg viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>`;
    btn.setAttribute('aria-label', 'Pause Audio');
  } else {
    btn.innerHTML = `<svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>`;
    btn.setAttribute('aria-label', 'Play Audio');
  }
}

function formatSeconds(secs) {
  const m = Math.floor(secs / 60);
  const s = Math.floor(secs % 60);
  return `${m}:${s < 10 ? '0' : ''}${s}`;
}
