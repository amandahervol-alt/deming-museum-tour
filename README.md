# 🏛️ Deming Luna Mimbres Museum — AI-Powered QR Tour & Docent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/Hosting-GitHub%20Pages%20($0)-green.svg)](https://pages.github.com/)
[![Accessibility](https://img.shields.io/badge/Accessibility-Transcripts%20Included-blue.svg)](#accessibility)

An interactive, zero-cost audio guide and AI Docent web application built for the **Deming Luna Mimbres Museum** (housed in the historic 1916 National Guard Armory in Deming, New Mexico). 

This project delivers a seamless mobile experience for museum visitors scanning QR codes across 15 exhibit rooms, paired with a grounded **AI Museum Docent** chatbot.

---

## 📢 Board Presentation & Plain-Language Guide

Are you presenting this system to museum board members, community leaders, or volunteer docents?

👉 **[Read the Full Board Presentation & Plain-Language Breakdown (BOARD_PRESENTATION.md)](BOARD_PRESENTATION.md)**

Includes:
* **The 60-Second Opening Pitch** (Word-for-word conversational script)
* **The 4 Key Things the Board Cares About** ($0 Cost, No App Store Downloads, Thick Armory Walls, Grounded AI)
* **Anticipated Board Questions & Answers** (Common objections handled in plain English)
* **The 15 Exhibit Rooms Breakdown**

---

## 🌟 Portfolio & Architecture Highlights

* **Zero-Cost Serverless Hosting**: Runs 100% free on **GitHub Pages** with zero backend infrastructure or server maintenance fees.
* **Mobile-First & Accessible**: Designed specifically for smartphone screens in portrait orientation, featuring large touch controls, high contrast, and full text transcripts for hard-of-hearing visitors.
* **Grounded AI Museum Docent (RAG)**: Integrates Google Gemini API with a local museum knowledge base (`museum_knowledge.json`) covering 1,000+ years of Southwestern history, Mimbres pottery, the 1881 Railroad junction, Bataan veterans, and local attractions.
* **Turnkey Offline / Demo Mode**: Built-in intelligent pattern matcher provides instant docent answers even when offline or running without an API key.
* **Printable QR Code Generator**: Includes a Python CLI script to generate 15 high-res QR codes formatted for exhibit room placards.

---

## 📁 Repository Structure

```
deming-museum-tour/
├── index.html                  # Main responsive single-page web app
├── css/
│   └── styles.css              # Southwestern parchment/terracotta theme
├── js/
│   ├── app.js                  # Room router, state, and audio playback controls
│   └── ai-docent.js            # Gemini API & offline RAG knowledge matcher
├── data/
│   ├── rooms.json              # Structured data & transcripts for 15 exhibit rooms
│   └── museum_knowledge.json   # Deep historical grounding context for AI Docent
├── qr_codes/                   # Generated printable room QR code cards
├── scripts/
│   └── generate_qr_codes.py    # Python QR code generator tool
├── BOARD_PRESENTATION.md       # Board meeting guide & plain-language script
├── AGENTS.md                   # Antigravity Orchestration Architecture
├── LICENSE                     # MIT License
└── README.md                   # Project documentation
```

---

## 🚀 How to Deploy on GitHub Pages

1. **Push the Code to GitHub**:
   ```bash
   git push origin main
   ```

2. **Enable GitHub Pages**:
   - Go to your repository **Settings** → **Pages**.
   - Under **Build and deployment** → **Source**, select **Deploy from a branch**.
   - Select branch `main` / folder `/ (root)` and click **Save**.
   - Your site will be live at: `https://amandahervol-alt.github.io/deming-museum-tour/`

3. **Generate Room QR Codes**:
   ```bash
   cd scripts
   python generate_qr_codes.py --base-url "https://amandahervol-alt.github.io/deming-museum-tour"
   ```

---

## 💡 Optional: Enabling Live Gemini API Key

To enable real-time Gemini LLM answers:
1. Obtain a free Gemini API key from [Google AI Studio](https://aistudio.google.com/).
2. In your browser console on the site, run:
   ```javascript
   localStorage.setItem('GEMINI_API_KEY', 'YOUR_ACTUAL_API_KEY');
   ```
*(If no API key is provided, the app automatically uses the smart offline docent matcher for seamless demo presentations!)*

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
*Proudly developed for the Deming Luna Mimbres Museum & Luna County Historical Society.*
