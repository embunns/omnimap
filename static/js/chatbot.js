/* =====================================================
   CHATBOT FUNCTIONALITY
   File: chatbot.js
   Deskripsi: JavaScript khusus untuk fitur chatbot
===================================================== */

document.addEventListener("DOMContentLoaded", function () {
  // ✅ Initialize semua di sini
  initSidebarToggle();
  setupEventListeners();
  initChatbot();
});

// =============== CHATBOT INITIALIZATION ===============
function initChatbot() {
  const chatInput = document.getElementById("chatInput");
  const sendButton = document.getElementById("sendButton");
  const chatMessages = document.getElementById("chatMessages");
  const suggestionChips = document.querySelectorAll(".suggestion-chip");
  const suggestionsSection = document.getElementById("suggestionsSection");
  const chatbotTitle = document.getElementById("title");
  const chatbotIllustration = document.getElementById("illustration");

  /* =====================================================
       HELPER FUNCTIONS
    ===================================================== */

  /**
   * Get current time in HH:MM format
   * @returns {string} Formatted time
   */
  function getCurrentTime() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, "0");
    const minutes = now.getMinutes().toString().padStart(2, "0");
    return `${hours}:${minutes}`;
  }

  /**
   * Add message to chat
   * @param {string} text - Message text
   * @param {boolean} isUser - Whether message is from user
   * @param {object} aiResponse - AI response object with text and list
   */
  function addMessage(text, isUser = true, aiResponse = null) {
    // Show chat messages and hide initial UI
    if (!chatMessages.classList.contains("active")) {
      chatMessages.classList.add("active");
      chatbotTitle.style.display = "none";
      chatbotIllustration.style.display = "none";
      suggestionsSection.style.display = "none";
    }

    // Create message group
    const messageGroup = document.createElement("div");
    messageGroup.className = `message-group ${isUser ? "user" : "ai"}`;

    // Create avatar
    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = isUser ? "👩" : "🤖";
    messageGroup.appendChild(avatar);

    // Create message wrapper
    const messageWrapper = document.createElement("div");
    messageWrapper.className = "message-content-wrapper";

    // Create sender name
    const sender = document.createElement("div");
    sender.className = "message-sender";
    sender.textContent = isUser
      ? window.userData?.nama || "Anda"
      : "OMNIMAP AI";
    messageWrapper.appendChild(sender);

    // Create message bubble
    const messageBubble = document.createElement("div");
    messageBubble.className = "message-bubble";

    // Add content to message bubble
    if (isUser) {
      messageBubble.textContent = text;
    } else {
      if (aiResponse && aiResponse.list) {
        // Create text paragraph
        const textPara = document.createElement("p");
        textPara.textContent = aiResponse.text;
        messageBubble.appendChild(textPara);

        // Create ordered list
        const ol = document.createElement("ol");
        aiResponse.list.forEach((item) => {
          const li = document.createElement("li");
          li.textContent = item;
          ol.appendChild(li);
        });
        messageBubble.appendChild(ol);
      } else {
        messageBubble.textContent = text;
      }
    }
    messageWrapper.appendChild(messageBubble);

    // Create timestamp
    const timestamp = document.createElement("div");
    timestamp.className = "message-time";
    timestamp.textContent = getCurrentTime();
    messageWrapper.appendChild(timestamp);

    // Append wrapper to message group
    messageGroup.appendChild(messageWrapper);
    chatMessages.appendChild(messageGroup);

    // Scroll to bottom
    setTimeout(() => {
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
  }

  /**
   * Show typing indicator
   */
  function showTypingIndicator() {
    const typingGroup = document.createElement("div");
    typingGroup.className = "message-group ai";
    typingGroup.id = "typingGroup";

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = "🤖";
    typingGroup.appendChild(avatar);

    const wrapper = document.createElement("div");
    wrapper.className = "message-content-wrapper";

    const sender = document.createElement("div");
    sender.className = "message-sender";
    sender.textContent = "OMNIMAP AI";
    wrapper.appendChild(sender);

    const typing = document.createElement("div");
    typing.className = "typing-indicator active";
    typing.innerHTML =
      '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
    wrapper.appendChild(typing);

    typingGroup.appendChild(wrapper);
    chatMessages.appendChild(typingGroup);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  /**
   * Remove typing indicator
   */
  function removeTypingIndicator() {
    const typingGroup = document.getElementById("typingGroup");
    if (typingGroup) {
      typingGroup.remove();
    }
  }
  /**
 * Show warning toast
 */
  function showWarningToast(message) {
    // Cek apakah sudah ada toast
    let toast = document.getElementById('warningToast');
    
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'warningToast';
      toast.className = 'warning-toast';
      document.body.appendChild(toast);
    }
    
    toast.textContent = message;
    toast.classList.add('show');
    
    // Auto hide after 3 seconds
    setTimeout(() => {
      toast.classList.remove('show');
    }, 3000);
  }
  /* =====================================================
       SEND MESSAGE FUNCTIONALITY
    ===================================================== */

  /**
   * Send message to chatbot API
   */
  /**
 * Send message to chatbot API
 */
  async function sendMessage() {
    const message = chatInput.value.trim();
    if (message === "") return;

    // ✅ CHECK RATE LIMITING (TARUH DI SINI - SEBELUM ADD MESSAGE)
    const canSend = canSendMessage();
    if (!canSend.allowed) {
      // Tampilkan warning toast atau message
      showWarningToast(canSend.message);
      return;
    }
    
    // Update last message time
    lastMessageTime = Date.now();

    // Add user message to chat
    addMessage(message, true);
    chatInput.value = "";
    sendButton.disabled = true;

    // Show typing indicator
    showTypingIndicator();

    try {
      // ✅ TAMBAHKAN TIMEOUT UNTUK REQUEST
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 detik timeout

      // Send message to backend
      const response = await fetch("/api/chatbot/message", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: message }),
        signal: controller.signal // Tambahkan signal untuk timeout
      });

      clearTimeout(timeoutId);

      // ✅ CEK STATUS RESPONSE
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();

      // Remove typing indicator
      removeTypingIndicator();

      // Add AI response to chat
      if (data.success && data.response) {
        addMessage("", false, data.response);
      } else {
        // ✅ TAMPILKAN ERROR MESSAGE YANG LEBIH SPESIFIK
        const errorMsg = data.message || "Maaf, AI sedang sibuk. Silakan coba lagi.";
        addMessage(errorMsg, false);
      }
    } catch (error) {
      console.error("Error:", error);
      removeTypingIndicator();
      
      // ✅ BERBEDA ERROR MESSAGE BERDASARKAN JENIS ERROR
      let errorMessage = "Maaf, terjadi kesalahan. Silakan coba lagi.";
      
      if (error.name === 'AbortError') {
        errorMessage = "Request timeout. AI membutuhkan waktu terlalu lama. Silakan coba pertanyaan yang lebih singkat.";
      } else if (error.message.includes('Failed to fetch')) {
        errorMessage = "Tidak dapat terhubung ke server. Periksa koneksi internet Anda.";
      } else if (error.message.includes('Server error')) {
        errorMessage = "Server sedang sibuk. Silakan tunggu sebentar dan coba lagi.";
      }
      
      addMessage(errorMessage, false);
    }

    // Re-enable send button
    sendButton.disabled = false;
    chatInput.focus(); // ✅ AUTO FOCUS KE INPUT SETELAH KIRIM
  }

  /* =====================================================
       EVENT LISTENERS
    ===================================================== */

  // Send button click
  if (sendButton) {
    sendButton.addEventListener("click", sendMessage);
  }

  // Enter key press in input
  if (chatInput) {
    chatInput.addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        sendMessage();
      }
    });

    // Enable/disable send button based on input
    chatInput.addEventListener("input", function () {
      sendButton.disabled = this.value.trim() === "";
    });
  }

  // Suggestion chips click
  suggestionChips.forEach((chip) => {
    chip.addEventListener("click", function () {
      const question = this.getAttribute("data-question");
      chatInput.value = question;
      sendMessage();
    });
  });

  // Initialize send button as disabled
  if (sendButton) {
    sendButton.disabled = true;
  }
}

// =============== RATE LIMITING ===============
let lastMessageTime = 0;
const MESSAGE_COOLDOWN = 3000; // 3 detik cooldown antara pesan

/**
 * Check if user can send message (rate limiting)
 */
function canSendMessage() {
  const now = Date.now();
  const timeSinceLastMessage = now - lastMessageTime;
  
  if (timeSinceLastMessage < MESSAGE_COOLDOWN) {
    const remainingTime = Math.ceil((MESSAGE_COOLDOWN - timeSinceLastMessage) / 1000);
    return {
      allowed: false,
      message: `Mohon tunggu ${remainingTime} detik sebelum mengirim pesan lagi.`
    };
  }
  
  return { allowed: true };
}

// =============== SIDEBAR TOGGLE ===============
function initSidebarToggle() {
  const sidebar = document.getElementById("sidebar");
  const content = document.getElementById("content");
  const toggleButtons = document.querySelectorAll(".toggle-sidebar");

  toggleButtons.forEach((button) => {
    button.addEventListener("click", function () {
      // Deteksi apakah sedang dalam mode mobile atau desktop
      const isMobile = window.innerWidth <= 768;

      if (isMobile) {
        // Di mobile: toggle class 'mobile-active'
        sidebar.classList.toggle("mobile-active");
      } else {
        // Di desktop: toggle class 'hide'
        sidebar.classList.toggle("hide");
        content.classList.toggle("full-width");
      }
    });
  });
}

// =============== SETUP EVENT LISTENERS ===============
function setupEventListeners() {
  // Logout functionality
  const signOutBtn = document.getElementById("signOutBtn");
  const logoutModal = document.getElementById("logoutModal");
  const logoutCancel = document.getElementById("logoutCancel");
  const logoutConfirm = document.getElementById("logoutConfirm");

  if (signOutBtn && logoutModal) {
    signOutBtn.addEventListener("click", function (e) {
      e.preventDefault();
      logoutModal.classList.add("active");
    });
  }

  if (logoutCancel && logoutModal) {
    logoutCancel.addEventListener("click", function () {
      logoutModal.classList.remove("active");
    });
  }

  if (logoutConfirm) {
    logoutConfirm.addEventListener("click", function () {
      fetch("/api/logout", { method: "POST" })
        .then(() => {
          window.location.href = "/login";
        })
        .catch(() => {
          window.location.href = "/login";
        });
    });
  }
}