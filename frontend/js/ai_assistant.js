/**
 * NASA FIRE-X Floating AI Assistant Controller
 * Handles panel open/close, message rendering, streaming typing,
 * context-aware prompting, and bilingual EN/AZ responses.
 */

class FireXAIAssistant {
  constructor() {
    this.isOpen = false;
    this.isTyping = false;
    this.messages = [];
    this.currentPageContext = null;
    this.drawer = null;
    this.triggerBtn = null;
    this.messagesContainer = null;
    this.inputField = null;
  }

  init() {
    this.drawer = document.getElementById('ai-drawer-panel');
    this.triggerBtn = document.getElementById('ai-trigger-btn');
    this.messagesContainer = document.getElementById('ai-messages-list');
    this.inputField = document.getElementById('ai-input-field');

    if (!this.drawer || !this.triggerBtn) return;

    // Trigger button click
    this.triggerBtn.addEventListener('click', () => this.togglePanel());

    // Input form submit
    const form = document.getElementById('ai-input-form');
    if (form) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        this.sendMessage();
      });
    }

    // Close button
    const closeBtn = document.getElementById('ai-close-btn');
    if (closeBtn) closeBtn.addEventListener('click', () => this.closePanel());

    // Clear button
    const clearBtn = document.getElementById('ai-clear-btn');
    if (clearBtn) clearBtn.addEventListener('click', () => this.clearConversation());

    // Prompt chips
    document.querySelectorAll('.ai-chip-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const prompt = btn.getAttribute('data-prompt');
        if (prompt) {
          this.inputField.value = prompt;
          this.inputField.focus();
        }
      });
    });

    // Show welcome message
    this.renderWelcome();

    // Listen for language changes
    if (window.i18n) {
      window.i18n.onLanguageChange(() => {
        document.querySelectorAll('.ai-chip-btn').forEach(btn => {
          const key = btn.getAttribute('data-i18n');
          if (key) btn.textContent = window.i18n.t(key);
        });
      });
    }
  }

  togglePanel() {
    if (this.isOpen) {
      this.closePanel();
    } else {
      this.openPanel();
    }
  }

  openPanel() {
    this.isOpen = true;
    this.drawer.classList.add('open');
    this.triggerBtn.setAttribute('aria-expanded', 'true');
    if (this.inputField) setTimeout(() => this.inputField.focus(), 400);
  }

  closePanel() {
    this.isOpen = false;
    this.drawer.classList.remove('open');
    this.triggerBtn.setAttribute('aria-expanded', 'false');
  }

  setPageContext(context) {
    this.currentPageContext = context;
    const banner = document.getElementById('ai-context-val');
    if (banner && context) {
      const label = context.experiment_id || context.section || context.scenario || 'Dashboard';
      banner.textContent = label;
    }
  }

  renderWelcome() {
    const lang = window.i18n ? window.i18n.currentLanguage : 'en';
    const welcome = window.i18n ? window.i18n.t('ai.welcome_message') :
      "Welcome to FIRE-X. I am your NASA Microgravity Combustion & Fire Safety specialist. How can I assist you today?";

    this.appendMessage('assistant', welcome);
  }

  async sendMessage() {
    const content = this.inputField ? this.inputField.value.trim() : '';
    if (!content || this.isTyping) return;

    const lang = window.i18n ? window.i18n.currentLanguage : 'en';

    // Append user message
    this.inputField.value = '';
    this.appendMessage('user', content);
    this.messages.push({ role: 'user', content });

    // Show typing indicator
    this.showTypingIndicator();

    try {
      const result = await window.apiClient.sendChatMessage(
        this.messages,
        lang,
        this.currentPageContext
      );

      this.hideTypingIndicator();

      const response = result.response || (lang === 'az'
        ? "Xahiş olunur bir az sonra yenidən cəhd edin."
        : "Please try again in a moment.");

      this.appendMessage('assistant', response);
      this.messages.push({ role: 'assistant', content: response });

      // Keep last 8 messages only
      if (this.messages.length > 8) {
        this.messages = this.messages.slice(-8);
      }

    } catch (err) {
      this.hideTypingIndicator();
      const errMsg = lang === 'az'
        ? "Şəbəkə xətası baş verdi."
        : "A network error occurred. Please try again.";
      this.appendMessage('assistant', errMsg);
    }
  }

  appendMessage(role, content) {
    if (!this.messagesContainer) return;

    const msgDiv = document.createElement('div');
    msgDiv.classList.add('ai-message', role);

    const avatarDiv = document.createElement('div');
    avatarDiv.classList.add('ai-avatar');

    if (role === 'user') {
      avatarDiv.classList.add('ai-avatar-user');
      avatarDiv.textContent = 'U';
    } else {
      const logoImg = document.createElement('img');
      logoImg.src = '/images/Fire-X.jpeg';
      logoImg.alt = 'FIRE-X AI';
      logoImg.style.cssText = 'width:22px;height:22px;object-fit:contain;border-radius:4px;';
      logoImg.onerror = () => { avatarDiv.textContent = 'AI'; };
      avatarDiv.appendChild(logoImg);
    }

    const bubbleDiv = document.createElement('div');
    bubbleDiv.classList.add('ai-bubble');
    // Render basic markdown: bold, newlines
    bubbleDiv.innerHTML = this.parseMarkdown(content);

    msgDiv.appendChild(avatarDiv);
    msgDiv.appendChild(bubbleDiv);
    this.messagesContainer.appendChild(msgDiv);
    this.scrollToBottom();
  }

  parseMarkdown(text) {
    // Escape HTML first
    let safe = text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');

    // Bold: **text**
    safe = safe.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    // Italic: *text*
    safe = safe.replace(/\*(.+?)\*/g, '<em>$1</em>');
    // Inline code: `code`
    safe = safe.replace(/`([^`]+)`/g, '<code style="font-family:var(--font-mono);background:rgba(0,229,255,0.1);padding:2px 5px;border-radius:3px;font-size:0.82em;color:var(--nasa-cyan)">$1</code>');
    // Numbered list
    safe = safe.replace(/^(\d+)\.\s+(.+)$/gm, '<div style="margin-left:8px;margin-bottom:2px"><strong style="color:var(--nasa-cyan)">$1.</strong> $2</div>');
    // Bullet list
    safe = safe.replace(/^[-•]\s+(.+)$/gm, '<div style="margin-left:8px;margin-bottom:2px">&#8250; $1</div>');
    // Newlines to br
    safe = safe.replace(/\n{2,}/g, '<br><br>');
    safe = safe.replace(/\n/g, '<br>');

    return safe;
  }

  showTypingIndicator() {
    if (!this.messagesContainer || this.isTyping) return;
    this.isTyping = true;

    const typingDiv = document.createElement('div');
    typingDiv.classList.add('ai-message', 'assistant');
    typingDiv.id = 'typing-indicator-wrap';

    const avatarDiv = document.createElement('div');
    avatarDiv.classList.add('ai-avatar');
    avatarDiv.style.cssText = 'background:var(--bg-surface-2);border:1px solid var(--border-slate);';
    const logoImg = document.createElement('img');
    logoImg.src = '/images/Fire-X.jpeg';
    logoImg.style.cssText = 'width:22px;height:22px;object-fit:contain;border-radius:4px;';
    logoImg.onerror = () => { avatarDiv.textContent = 'AI'; };
    avatarDiv.appendChild(logoImg);

    const indicatorDiv = document.createElement('div');
    indicatorDiv.classList.add('ai-typing-indicator');
    indicatorDiv.innerHTML = `
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
    `;

    typingDiv.appendChild(avatarDiv);
    typingDiv.appendChild(indicatorDiv);
    this.messagesContainer.appendChild(typingDiv);
    this.scrollToBottom();
  }

  hideTypingIndicator() {
    this.isTyping = false;
    const indicator = document.getElementById('typing-indicator-wrap');
    if (indicator) indicator.remove();
  }

  clearConversation() {
    this.messages = [];
    if (this.messagesContainer) this.messagesContainer.innerHTML = '';
    this.renderWelcome();
  }

  scrollToBottom() {
    if (this.messagesContainer) {
      this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
  }
}

window.aiAssistant = new FireXAIAssistant();
