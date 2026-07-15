// =========================================================
// NOVELLA — Frontend Chat Logic 

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

const API_BASE_URL = "https://novella-6j9x.onrender.com";

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