/**
 * AgriSense AI – Chat Interface JavaScript
 * Handles: message sending, streaming response display, history,
 *          markdown rendering, auto-scroll, copy functionality
 */

'use strict';

// ── State ────────────────────────────────────────────────────────
const chatState = {
  isLoading: false,
  messageCount: 0,
};

// ── DOM References ────────────────────────────────────────────────
const chatForm = document.getElementById('chat-form');
const messageInput = document.getElementById('message-input');
const chatMessages = document.getElementById('chat-messages');
const typingIndicator = document.getElementById('typing-indicator');
const sendBtn = document.getElementById('send-btn');
const charCount = document.getElementById('char-count');
const clearChatBtn = document.getElementById('clear-chat-btn');
const clearChatOffcanvas = document.getElementById('clear-chat-offcanvas');
const welcomeScreen = document.getElementById('welcome-screen');

// ── Initialize ────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  scrollToBottom();
  bindSuggestedQuestions();
  bindChipButtons();

  // Auto-resize textarea
  if (messageInput) {
    messageInput.addEventListener('input', autoResizeTextarea);
    messageInput.addEventListener('input', updateCharCount);

    // Ctrl+Enter to send
    messageInput.addEventListener('keydown', function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        submitMessage();
      }
      // Enter without shift/ctrl sends on desktop
      if (e.key === 'Enter' && !e.shiftKey && window.innerWidth > 768) {
        e.preventDefault();
        submitMessage();
      }
    });
  }

  // Form submit
  if (chatForm) {
    chatForm.addEventListener('submit', function (e) {
      e.preventDefault();
      submitMessage();
    });
  }

  // Clear chat buttons
  [clearChatBtn, clearChatOffcanvas].forEach(btn => {
    if (btn) btn.addEventListener('click', clearChat);
  });

  // Copy buttons (for existing messages on page load)
  bindCopyButtons();
});

// ── Message Submission ────────────────────────────────────────────
async function submitMessage() {
  if (chatState.isLoading) return;

  const message = (messageInput.value || '').trim();
  if (!message) return;

  // Clear input
  messageInput.value = '';
  autoResizeTextarea.call(messageInput);
  updateCharCount.call(messageInput);

  // Hide welcome screen
  if (welcomeScreen) {
    welcomeScreen.style.display = 'none';
  }

  // Append user message
  appendMessage('user', message);

  // Show typing indicator
  setLoading(true);

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      throw new Error(err.error || `HTTP ${response.status}`);
    }

    const data = await response.json();
    setLoading(false);

    appendMessage('ai', data.html_response, data.meta);

  } catch (error) {
    setLoading(false);
    appendMessage('ai', `<p>⚠️ <strong>Error:</strong> ${escapeHtml(error.message)}</p>`, null);
  }
}

// ── Append Message to DOM ─────────────────────────────────────────
function appendMessage(role, content, meta = null) {
  const row = document.createElement('div');
  row.className = `message-row ${role === 'user' ? 'user-row' : 'ai-row'}`;

  if (role === 'user') {
    row.innerHTML = `
      <div class="message-bubble user-bubble">
        <p class="mb-0">${escapeHtml(content)}</p>
      </div>
      <div class="message-avatar user-avatar">
        <i class="bi bi-person-fill"></i>
      </div>
    `;
  } else {
    const metaHtml = meta ? `
      <div class="d-flex align-items-center gap-2 mt-2 message-meta">
        <span class="text-muted" style="font-size:11px;">
          <i class="bi bi-cpu me-1"></i>${escapeHtml(meta.model)}
        </span>
        <span class="text-muted" style="font-size:11px;">${escapeHtml(meta.timestamp)}</span>
        ${meta.mode === 'demo' ? '<span class="badge bg-warning-subtle text-warning" style="font-size:10px;">Demo</span>' : ''}
      </div>
    ` : '';

    row.innerHTML = `
      <div class="message-avatar ai-avatar-chat">
        <i class="bi bi-tree-fill"></i>
      </div>
      <div class="message-bubble ai-bubble">
        <div class="ai-response-content">${content}</div>
        <div class="message-actions mt-2">
          <button class="action-btn copy-btn" title="Copy response">
            <i class="bi bi-clipboard"></i> Copy
          </button>
          ${metaHtml}
        </div>
      </div>
    `;
  }

  // Insert before typing indicator
  if (typingIndicator && typingIndicator.parentNode === chatMessages) {
    chatMessages.insertBefore(row, typingIndicator);
  } else {
    chatMessages.appendChild(row);
  }

  // Bind copy button
  const copyBtn = row.querySelector('.copy-btn');
  if (copyBtn) {
    copyBtn.addEventListener('click', function () {
      const textContent = row.querySelector('.ai-response-content');
      copyToClipboard(textContent ? textContent.innerText : content, this);
    });
  }

  scrollToBottom();
  chatState.messageCount++;
}

// ── Loading State ─────────────────────────────────────────────────
function setLoading(loading) {
  chatState.isLoading = loading;

  if (typingIndicator) {
    typingIndicator.classList.toggle('d-none', !loading);
  }
  if (sendBtn) {
    sendBtn.disabled = loading;
    sendBtn.innerHTML = loading
      ? '<span class="spinner-border spinner-border-sm" role="status"></span>'
      : '<i class="bi bi-send-fill"></i>';
  }
  if (messageInput) {
    messageInput.disabled = loading;
    if (!loading) messageInput.focus();
  }

  if (loading) scrollToBottom();
}

// ── Clear Chat ────────────────────────────────────────────────────
function clearChat() {
  if (!confirm('Clear all chat history? This cannot be undone.')) return;

  fetch('/api/chat/clear', { method: 'POST' })
    .then(() => {
      // Remove all message rows
      const rows = chatMessages.querySelectorAll('.message-row:not(#typing-indicator)');
      rows.forEach(row => row.remove());

      // Show welcome screen
      if (welcomeScreen) {
        welcomeScreen.style.display = '';
      }

      chatState.messageCount = 0;
    })
    .catch(err => console.error('Clear chat error:', err));
}

// ── Suggested Questions ───────────────────────────────────────────
function bindSuggestedQuestions() {
  document.querySelectorAll('.suggested-btn[data-q]').forEach(btn => {
    btn.addEventListener('click', function () {
      const q = this.dataset.q;
      if (messageInput) {
        messageInput.value = q;
        autoResizeTextarea.call(messageInput);
        updateCharCount.call(messageInput);
      }
      submitMessage();
    });
  });
}

function bindChipButtons() {
  document.querySelectorAll('.chip-btn[data-q]').forEach(btn => {
    btn.addEventListener('click', function () {
      const q = this.dataset.q;
      if (messageInput) {
        messageInput.value = q;
        autoResizeTextarea.call(messageInput);
        updateCharCount.call(messageInput);
      }
      submitMessage();
    });
  });
}

// ── Copy Buttons ──────────────────────────────────────────────────
function bindCopyButtons() {
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      const bubble = this.closest('.ai-bubble');
      if (bubble) {
        const content = bubble.querySelector('.ai-response-content');
        copyToClipboard(content ? content.innerText : '', this);
      }
    });
  });
}

async function copyToClipboard(text, btn) {
  try {
    await navigator.clipboard.writeText(text);
    const original = btn.innerHTML;
    btn.innerHTML = '<i class="bi bi-check-lg"></i> Copied!';
    btn.style.color = '#22c55e';
    setTimeout(() => {
      btn.innerHTML = original;
      btn.style.color = '';
    }, 2000);
  } catch (err) {
    console.error('Copy failed:', err);
  }
}

// ── Utility Functions ─────────────────────────────────────────────
function scrollToBottom() {
  if (chatMessages) {
    requestAnimationFrame(() => {
      chatMessages.scrollTop = chatMessages.scrollHeight;
    });
  }
}

function autoResizeTextarea() {
  this.style.height = 'auto';
  this.style.height = Math.min(this.scrollHeight, 150) + 'px';
}

function updateCharCount() {
  if (charCount) {
    const len = (this.value || '').length;
    charCount.textContent = `${len}/2000`;
    charCount.style.color = len > 1800 ? '#ef4444' : '';
  }
}

function escapeHtml(str) {
  if (!str) return '';
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
