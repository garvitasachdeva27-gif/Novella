// =========================================================
// NOVELLA — Frontend Chat Logic (Milestone 2: UI only)
//
// IMPORTANT: getBotReply() below is a MOCK. It does not call
// Gemini or our backend yet — that happens in Milestone 4.
// It's written with the same shape (async, returns a string)
// that the real version will have, so swapping it later is a
// one-function change, not a rewrite.
// =========================================================

// ---- Element references -----------------------------------------
const startChatBtn = document.getElementById("start-chat-btn");
const backBtn = document.getElementById("back-btn");
const landingView = document.getElementById("landing-view");
const chatView = document.getElementById("chat-view");
const chatMessages = document.getElementById("chat-messages");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const typingIndicator = document.getElementById("typing-indicator");
const quickActions = document.getElementById("quick-actions");

// Tracks whether we've shown the welcome message yet, so we
// don't repeat it if the user goes back and forth between views.
let hasGreeted = false;

// ---- View switching -----------------------------------------------
// "State" here is just which view has the .hidden class. No framework
// needed for two screens — this is the simplest tool that does the job.
function showChatView() {
  landingView.classList.add("hidden");
  chatView.classList.remove("hidden");
  chatInput.focus();

  if (!hasGreeted) {
    appendMessage("bot", buildWelcomeMessage());
    hasGreeted = true;
  }
}

function showLandingView() {
  chatView.classList.add("hidden");
  landingView.classList.remove("hidden");
}

startChatBtn.addEventListener("click", showChatView);
backBtn.addEventListener("click", showLandingView);

// ---- Welcome message ------------------------------------------------
// Static text, not AI-generated — it renders instantly, with zero
// API latency, the moment the chat view opens.
function buildWelcomeMessage() {
  return (
    "☕ Welcome to Novella.\n" +
    "Where every question finds its next chapter.\n\n" +
    "I can help with:\n" +
    "📖 Membership\n" +
    "📚 Borrowing Books\n" +
    "💻 Digital Library\n" +
    "💳 Fines & Fees\n" +
    "🪑 Study Spaces\n" +
    "🎭 Library Events\n\n" +
    "What can I help you discover today?"
  );
}

// ---- Rendering messages ----------------------------------------------
function appendMessage(sender, text) {
  const li = document.createElement("li");
  li.className = `message ${sender}`;
  // Preserve line breaks from the welcome message / multi-line replies
  li.style.whiteSpace = "pre-line";
  li.textContent = text;
  chatMessages.appendChild(li);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTyping() {
  typingIndicator.classList.remove("hidden");
}

function hideTyping() {
  typingIndicator.classList.add("hidden");
}

// ---- Mock bot reply (placeholder for Milestone 4) ---------------------
// In Milestone 4, this function's body will be replaced with a real
// fetch() call to our FastAPI backend, e.g.:
//
//   async function getBotReply(userMessage) {
//     const res = await fetch("/chat", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ message: userMessage }),
//     });
//     const data = await res.json();
//     return data.reply;
//   }
//
// The rest of the app (appendMessage, typing indicator, form handling)
// will not need to change at all.
// ---- Real bot reply, calling our FastAPI backend -----------------------
// Change this to your deployed backend URL once you deploy (Step 3 below).
// While developing locally, this points at uvicorn running on your machine.
const API_BASE_URL = "http://127.0.0.1:8000";

async function getBotReply(userMessage) {
  try {
    const res = await fetch(`${API_BASE_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMessage }),
    });

    if (!res.ok) {
      throw new Error(`Server responded with ${res.status}`);
    }

    const data = await res.json();
    // data.reply, data.category, data.escalated, data.ticket_id are all
    // available here if you want to show category/ticket info in the UI later.
    return data.reply;
  } catch (error) {
    console.error("Chat request failed:", error);
    return "I'm having trouble connecting right now — please try again in a moment.";
  }
}
// ---- Handling user input -----------------------------------------------
async function handleUserMessage(text) {
  const trimmed = text.trim();
  if (!trimmed) return;

  appendMessage("user", trimmed);
  chatInput.value = "";

  showTyping();
  const reply = await getBotReply(trimmed);
  hideTyping();

  appendMessage("bot", reply);
}

chatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  handleUserMessage(chatInput.value);
});

// ---- Quick action chips --------------------------------------------------
// Each chip sends a natural-language message on the user's behalf,
// as if they'd typed "Tell me about Membership".
quickActions.addEventListener("click", (event) => {
  const chip = event.target.closest(".chip");
  if (!chip) return;
  const topic = chip.dataset.topic;
  handleUserMessage(`Tell me about ${topic}`);
});