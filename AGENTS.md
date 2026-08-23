# Deming Luna Mimbres Museum Tour — AI Orchestration Guide
AGENTS.md — Antigravity Orchestration Architecture

This repository delivers an interactive mobile web application and AI Docent for the historic Deming Luna Mimbres Museum in Deming, New Mexico.

## Architecture

### 1. Zero-Cost Frontend Layer (`index.html`, `css/`, `js/`)
- Single-page application optimized for mobile portrait screens.
- Room router driven by URL query parameters (`?room=1` to `?room=15`) scanned from physical QR codes.
- Audio player with play/pause/scrub and full synchronized text transcripts.

### 2. Knowledge Retrieval & Grounded AI Docent (`data/`, `js/ai-docent.js`)
- `data/rooms.json`: Curated room narratives, audio paths, and visual highlights.
- `data/museum_knowledge.json`: Deep historical grounding data across 1,000+ years of Luna County history.
- `js/ai-docent.js`: Dual-mode intelligence:
  - **Live Mode**: Google Gemini API integration with custom museum docent system prompt.
  - **Offline Fallback**: Client-side pattern matcher providing instant answers without external API dependency.

### 3. QR Placard Generator Tooling (`scripts/generate_qr_codes.py`)
- Python script generating printable room QR code graphics formatted for museum placards.

### 4. Board Governance & Presentation (`BOARD_PRESENTATION.md`)
- Non-technical presentation script and FAQ breakdown for museum directors and historical society boards.
