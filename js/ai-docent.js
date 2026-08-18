/**
 * Deming Luna Mimbres Museum - AI Docent Assistant
 * Supports direct Google Gemini API integration and an offline RAG knowledge matcher fallback.
 */

let museumKnowledge = null;

document.addEventListener('DOMContentLoaded', async () => {
  setupChatModal();
  await loadKnowledgeBase();
});

async function loadKnowledgeBase() {
  try {
    const res = await fetch('data/museum_knowledge.json');
    museumKnowledge = await res.json();
  } catch (err) {
    console.error('Failed to load museum_knowledge.json:', err);
  }
}

function setupChatModal() {
  const fabBtn = document.getElementById('aiDocentFab');
  const overlay = document.getElementById('chatModalOverlay');
  const closeBtn = document.getElementById('chatCloseBtn');
  const sendBtn = document.getElementById('btnSendChat');
  const chatInput = document.getElementById('chatInput');

  if (!fabBtn || !overlay) return;

  fabBtn.addEventListener('click', () => {
    overlay.classList.add('active');
    chatInput.focus();
  });

  closeBtn.addEventListener('click', () => {
    overlay.classList.remove('active');
  });

  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
      overlay.classList.remove('active');
    }
  });

  sendBtn.addEventListener('click', handleUserSendMessage);
  chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleUserSendMessage();
  });
}

async function handleUserSendMessage() {
  const inputEl = document.getElementById('chatInput');
  const query = inputEl.value.trim();
  if (!query) return;

  // Render User Message
  appendChatMessage(query, 'user');
  inputEl.value = '';

  // Render Typing Indicator
  const typingId = appendChatMessage('AI Docent is thinking...', 'bot');

  // Generate Answer
  const answer = await generateAIDocentResponse(query);
  
  // Replace Typing Indicator with Response
  const typingEl = document.getElementById(typingId);
  if (typingEl) {
    typingEl.textContent = answer;
  }
}

function appendChatMessage(text, sender) {
  const container = document.getElementById('chatMessages');
  const bubble = document.createElement('div');
  const msgId = 'msg-' + Date.now() + '-' + Math.random().toString(36).substr(2, 4);
  bubble.id = msgId;
  bubble.className = `message-bubble ${sender}`;
  bubble.textContent = text;
  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
  return msgId;
}

async function generateAIDocentResponse(query) {
  const lowerQuery = query.toLowerCase();

  // Check if Gemini API key is configured in localStorage
  const apiKey = localStorage.getItem('GEMINI_API_KEY');
  if (apiKey) {
    try {
      return await callGeminiAPI(query, apiKey);
    } catch (e) {
      console.warn('Gemini API call failed, falling back to local docent match:', e);
    }
  }

  // Smart Local Fallback Knowledge Engine (RAG match)
  if (lowerQuery.includes('kill hole') || lowerQuery.includes('hole') || lowerQuery.includes('mimbres') || lowerQuery.includes('pottery') || lowerQuery.includes('bowl')) {
    return "The Mimbres people (A.D. 1000–1130) are famous for their black-on-white painted ceramic bowls. The small hole punched in the center is called a 'kill hole'—a ceremonial puncture created before burial to release the vessel's spirit!";
  }

  if (lowerQuery.includes('armory') || lowerQuery.includes('building') || lowerQuery.includes('1916') || lowerQuery.includes('architect')) {
    return "Our museum is housed in the historic 1916 red-brick National Guard Armory, listed on the National Register of Historic Places. It was built for Company I during border tensions and served as an armory and community center before becoming our museum!";
  }

  if (lowerQuery.includes('pancho villa') || lowerQuery.includes('columbus') || lowerQuery.includes('raid') || lowerQuery.includes('pershing')) {
    return "On March 9, 1916, Pancho Villa raided Columbus, NM (30 miles south of Deming). In response, President Woodrow Wilson sent General John J. 'Black Jack' Pershing on the Punitive Expedition out of Camp Furlong. You can view original weapons, dispatches, and expedition gear in Room 13!";
  }

  if (lowerQuery.includes('rock') || lowerQuery.includes('geode') || lowerQuery.includes('rockhound') || lowerQuery.includes('thunder egg')) {
    return "Deming is a rockhound's paradise! Nearby Rockhound State Park (12 miles SE) is one of the only state parks where visitors can legally keep up to 15 lbs of minerals they find. Check out Room 12 to see our fluorescent UV mineral display and polished thunder eggs!";
  }

  if (lowerQuery.includes('bataan') || lowerQuery.includes('military') || lowerQuery.includes('veteran') || lowerQuery.includes('war')) {
    return "Luna County has a proud military legacy. Room 3 honors local service members, including the brave soldiers of the 200th Coast Artillery (AA) who fought in the Philippines during WWII and survived the Bataan Death March.";
  }

  if (lowerQuery.includes('railroad') || lowerQuery.includes('train') || lowerQuery.includes('name') || lowerQuery.includes('deming')) {
    return "Deming became America's 2nd transcontinental railroad junction on March 8, 1881, when the Southern Pacific and Santa Fe tracks joined here! The town was named after Mary Ann Deming, wife of railroad tycoon Charles Crocker.";
  }

  if (lowerQuery.includes('quilt') || lowerQuery.includes('sew') || lowerQuery.includes('textile')) {
    return "Our Quilt Collection in Room 5 is one of the largest in the American Southwest! It features 19th-century hand-stitched Victorian crazy quilts, log cabin patterns, and Depression-era feedsack textiles.";
  }

  if (lowerQuery.includes('eat') || lowerQuery.includes('food') || lowerQuery.includes('restaurant') || lowerQuery.includes('wine')) {
    return "Deming is famous for delicious Southwestern New Mexican green chile dishes and local wineries! Don't miss visiting St. Clair / Lescombes Winery & Bistro nearby on Highway 549.";
  }

  if (lowerQuery.includes('cost') || lowerQuery.includes('admission') || lowerQuery.includes('ticket') || lowerQuery.includes('price')) {
    return "Admission to the Deming Luna Mimbres Museum is completely FREE! Donations are warmly accepted to support our volunteer-run historical society.";
  }

  // Default friendly docent answer
  return "That's a great question! Deming Luna Mimbres Museum houses over 85,000 historic items across 47 exhibit spaces in our historic 1916 Armory. Feel free to explore our 15 featured rooms or ask me about Mimbres pottery, the 1881 Railroad junction, Rockhound State Park, or local military history!";
}

async function callGeminiAPI(query, apiKey) {
  const room = roomsData.find(r => r.id === currentRoomId);
  const systemPrompt = `You are the friendly, expert AI Docent for the Deming Luna Mimbres Museum in Deming, New Mexico. 
Current Visitor Location: Room ${currentRoomId} (${room ? room.title : 'Museum'}).
Context: ${JSON.stringify(museumKnowledge)}.
Answer the visitor's question warmly, accurately, and concisely (2-4 sentences max).`;

  const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;
  
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      contents: [{
        parts: [
          { text: systemPrompt },
          { text: query }
        ]
      }]
    })
  });

  const data = await response.json();
  return data.candidates[0].content.parts[0].text;
}
