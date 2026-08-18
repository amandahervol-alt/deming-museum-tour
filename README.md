# 🏛️ Deming Luna Mimbres Museum — AI-Powered QR Tour & Docent

An interactive, zero-cost audio guide and AI Docent web application built for the **Deming Luna Mimbres Museum** (housed in the historic 1916 National Guard Armory in Deming, New Mexico). 

This project delivers a seamless mobile experience for museum visitors scanning QR codes across 15 exhibit rooms, paired with a grounded **AI Museum Docent** chatbot.

---

## 🌟 Portfolio & Architecture Highlights

This project showcases modern full-stack web engineering, accessibility, and AI integration designed for zero-cost civic deployment:

* **Zero-Cost Serverless Hosting**: Runs 100% free on **GitHub Pages** with zero backend infrastructure or server maintenance fees.
* **Mobile-First & Accessible**: Designed specifically for smartphone screens in portrait orientation, featuring large touch controls, high contrast, and full text transcripts for hard-of-hearing visitors.
* **Grounded AI Museum Docent (RAG)**: Integrates Google Gemini API with a local museum knowledge base (`museum_knowledge.json`) covering 1,000+ years of Southwestern history, Mimbres pottery, the 1881 Railroad junction, Bataan veterans, and local attractions.
* **Turnkey Offline / Demo Mode**: Built-in intelligent pattern matcher provides instant docent answers even when offline or running without an API key.
* **Printable QR Code Generator**: Includes a Python CLI script to generate 15 high-res QR codes formatted for exhibit room placards.

---

## 📋 Board Meeting Cheat Sheet (Thursday's Presentation)

Use these key points when answering questions at Thursday's museum board meeting:

1. **Hosting & Software Cost ($0)**: 
   - Hosted completely free on GitHub Pages. No monthly software licenses, no hosting bills.
2. **Visitor Convenience (No App Required)**:
   - Visitors simply open their phone's native camera and scan the QR code. The tour loads in 2 seconds directly in Safari or Chrome.
3. **Weak Signal / Thick Armory Walls**:
   - Audio files are compressed for fast loading, and full written transcripts appear right on screen if Wi-Fi or cellular service is slow inside the 1916 brick building.
4. **Maintenance & Content Updates**:
   - Updating room text or uploading new audio takes just minutes and requires no technical re-coding.
5. **Accessibility Compliance**:
   - Every audio speech includes a full text transcript for deaf or hard-of-hearing guests and visitors without headphones.
6. **Privacy & Security**:
   - No visitor tracking, no sign-ups, and no personal data collection.

---

## 📁 Repository Structure

```
deming-museum-ai-tour/
├── index.html                  # Main responsive single-page web app
├── css/
│   └── styles.css              # Southwestern parchment/terracotta theme
├── js/
│   ├── app.js                  # Room router, state, and audio playback controls
│   └── ai-docent.js            # Gemini API & offline RAG knowledge matcher
├── data/
│   ├── rooms.json              # Structured data & transcripts for 15 exhibit rooms
│   └── museum_knowledge.json   # Deep historical grounding context for AI Docent
├── scripts/
│   └── generate_qr_codes.py    # Python QR code generator tool
└── README.md                   # Project documentation & board guide
```

---

## 🚀 How to Deploy on GitHub Pages

1. **Create a GitHub Repository**:
   - Go to GitHub and create a new public repository named `deming-museum-tour`.

2. **Push the Code**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of Deming Museum QR Tour & AI Docent"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/deming-museum-tour.git
   git push -u origin main
   ```

3. **Enable GitHub Pages**:
   - Go to your repository **Settings** → **Pages**.
   - Under **Build and deployment** → **Source**, select **Deploy from a branch**.
   - Select branch `main` / folder `/ (root)` and click **Save**.
   - Your site will be live at: `https://YOUR_USERNAME.github.io/deming-museum-tour/`

4. **Generate Room QR Codes**:
   ```bash
   cd scripts
   python generate_qr_codes.py --base-url "https://YOUR_USERNAME.github.io/deming-museum-tour"
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

*Proudly developed for the Deming Luna Mimbres Museum & Luna County Historical Society.*
