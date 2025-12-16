// Chat Widget JavaScript
let sessionId = localStorage.getItem('rugipo_chat_session') || '';
let isOpen = false;

// Initialize chatbot
document.addEventListener('DOMContentLoaded', function () {
  const chatToggle = document.getElementById('chat-toggle');
  const chatClose = document.getElementById('chat-close');
  const chatWindow = document.getElementById('chat-window');
  const chatForm = document.getElementById('chat-form');
  const chatInput = document.getElementById('chat-input');
  const chatMessages = document.getElementById('chat-messages');

  // Toggle chat window
  chatToggle.addEventListener('click', function () {
    isOpen = !isOpen;
    if (isOpen) {
      chatWindow.classList.remove('hidden');
      chatToggle.classList.add('hidden');
      chatInput.focus();
    }
  });

  // Close chat window
  chatClose.addEventListener('click', function () {
    isOpen = false;
    chatWindow.classList.add('hidden');
    chatToggle.classList.remove('hidden');
  });

  // Handle form submission
  chatForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (message) {
      sendMessage(message);
      chatInput.value = '';
    }
  });
});

// Send message to backend
function sendMessage(message) {
  const chatMessages = document.getElementById('chat-messages');

  // Add user message to chat
  addMessage('user', message);

  // Show typing indicator
  showTypingIndicator();

  // Send to backend
  fetch('/chat/send-message/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: message,
      session_id: sessionId,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      hideTypingIndicator();

      if (data.success) {
        // Save session ID
        sessionId = data.session_id;
        localStorage.setItem('rugipo_chat_session', sessionId);

        // Add bot response
        addMessage('bot', data.bot_response);
      } else {
        addMessage('bot', 'Sorry, something went wrong. Please try again.');
      }
    })
    .catch((error) => {
      hideTypingIndicator();
      addMessage(
        'bot',
        'Sorry, I could not connect. Please check your internet connection.'
      );
    });
}

// Add message to chat window
function addMessage(type, content) {
  const chatMessages = document.getElementById('chat-messages');
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${type}-message`;

  if (type === 'user') {
    messageDiv.innerHTML = `
            <div class="bg-[#017C01] text-white rounded-lg py-2 px-4 max-w-xs ml-auto">
                ${escapeHtml(content)}
            </div>
        `;
  } else {
    messageDiv.innerHTML = `
            <div class="bg-gray-200 text-gray-800 rounded-lg py-2 px-4 max-w-xs text-sm">
                ${formatBotMessage(content)}
            </div>
        `;
  }

  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Format bot message (handle markdown-style formatting)
function formatBotMessage(content) {
  // Convert **text** to bold
  content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  // Convert newlines to <br>
  content = content.replace(/\n/g, '<br>');
  return content;
}

// Show typing indicator
function showTypingIndicator() {
  const chatMessages = document.getElementById('chat-messages');
  const typingDiv = document.createElement('div');
  typingDiv.id = 'typing-indicator';
  typingDiv.className = 'message bot-message';
  typingDiv.innerHTML = `
        <div class="bg-gray-200 text-gray-800 rounded-lg py-2 px-4 max-w-xs">
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
        </div>
    `;
  chatMessages.appendChild(typingDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Hide typing indicator
function hideTypingIndicator() {
  const typingIndicator = document.getElementById('typing-indicator');
  if (typingIndicator) {
    typingIndicator.remove();
  }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
