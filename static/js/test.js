/* ============================================================
   TES OMNI - Test Logic with Auto-Save & Exit Warning
   ============================================================ */
/* ============================================================
   TES OMNI - Test Logic with Auto-Save & Exit Warning
   ============================================================ */

let currentQuestionIndex = 0;
let totalQuestions = 0;
let answers = {};
let timer = null;
let timeRemaining = 3600;
let hasUnsavedChanges = false;
let currentAnswer = null;
let isSubmitting = false; // TAMBAHKAN INI

document.addEventListener('DOMContentLoaded', function() {
  loadSavedProgress();
  setupTestEventListeners();
  setupExitWarning();
});

function loadSavedProgress() {
  fetch('/api/load-saved-answers')
    .then(response => response.json())
    .then(data => {
      if (data.success && data.has_saved_progress) {
        answers = data.answers;
        console.log('✅ Loaded saved answers:', Object.keys(answers).length);
      }
    })
    .catch(error => console.error('Error loading saved progress:', error));
}

function setupTestEventListeners() {
  // Start test button
  const btnStart = document.getElementById('btn-start-test');
  if (btnStart) {
    btnStart.addEventListener('click', startTest);
  }
  
  // Answer buttons
  document.querySelectorAll('.tes-answer-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      selectAnswer(this);
    });
  });
  
  // Navigation buttons
  const btnNext = document.getElementById('btnNextTest');
  const btnPrev = document.getElementById('btnPrevTest');
  
  if (btnNext) {
    btnNext.addEventListener('click', nextQuestion);
  }
  
  if (btnPrev) {
    btnPrev.addEventListener('click', prevQuestion);
  }
  
  // Submit confirmation
  const btnConfirmSubmit = document.getElementById('btnConfirmSubmit');
  if (btnConfirmSubmit) {
    btnConfirmSubmit.addEventListener('click', submitTest);
  }
}

function setupExitWarning() {
  // HAPUS beforeunload - ganti dengan ini:
  window.addEventListener('beforeunload', function(e) {
    const questionContent = document.getElementById('questionContent');
    // Hanya warn jika test sedang berjalan DAN belum submit
    if (questionContent && 
        !questionContent.classList.contains('d-none') && 
        Object.keys(answers).length > 0 && 
        !isSubmitting) {
      e.preventDefault();
      return '';
    }
  });
  
  // Event delegation untuk semua link
  document.addEventListener('click', function(e) {
    const questionContent = document.getElementById('questionContent');
    
    // Cek apakah test sedang aktif
    if (!questionContent || questionContent.classList.contains('d-none') || isSubmitting) {
      return; // Test belum mulai atau sudah submit, izinkan navigasi
    }
    
    // Cek apakah yang diklik adalah link navigasi
    const link = e.target.closest('a, button[onclick*="location"]');
    
    if (link) {
      const href = link.getAttribute('href');
      const onclick = link.getAttribute('onclick');
      const isSignOut = link.id === 'signOutBtn' || link.closest('#signOutBtn');
      
      // Skip jika signout (sudah punya modal sendiri)
      if (isSignOut) {
        return;
      }
      
      // Skip jika button dalam test (prev/next)
      if (link.id === 'btnNextTest' || link.id === 'btnPrevTest') {
        return;
      }
      
      // Cek jika ada jawaban dan user mau keluar
      if (Object.keys(answers).length > 0) {
        let targetUrl = null;
        
        if (href && href !== '#' && !href.startsWith('javascript:')) {
          targetUrl = href;
        } else if (onclick) {
          const match = onclick.match(/['"](.*?)['"]/);
          if (match) targetUrl = match[1];
        }
        
        if (targetUrl) {
          e.preventDefault();
          e.stopPropagation();
          e.stopImmediatePropagation();
          showExitWarningModal(targetUrl);
        }
      }
    }
  }, true); // PENTING: useCapture = true
}

function showExitWarningModal(targetUrl) {
  const exitModal = new bootstrap.Modal(document.getElementById('ExitWarningModal'));
  exitModal.show();
  
  document.getElementById('btnConfirmExit').onclick = function() {
    isSubmitting = true; // Bypass warning
    exitModal.hide();
    setTimeout(() => {
      window.location.href = targetUrl;
    }, 300);
  };
}

function showExitWarningModal(targetUrl) {
  const exitModal = new bootstrap.Modal(document.getElementById('ExitWarningModal'));
  exitModal.show();
  
  // Handle confirm exit
  document.getElementById('btnConfirmExit').onclick = function() {
    hasUnsavedChanges = false;
    // Tutup modal dulu
    exitModal.hide();
    // Redirect setelah modal ditutup
    setTimeout(() => {
      window.location.href = targetUrl;
    }, 300);
  };
}

function showExitWarningPopup(targetUrl) {
  const popup = document.getElementById('exitWarningPopup');
  if (popup) {
    popup.classList.add('active');
    
    // Save and exit
    document.getElementById('btnSaveAndExit').onclick = function() {
      saveProgressAndExit(targetUrl);
    };
    
    // Exit without saving
    document.getElementById('btnExitWithoutSave').onclick = function() {
      hasUnsavedChanges = false;
      window.location.href = targetUrl;
    };
    
    // Cancel
    document.getElementById('btnCancelExit').onclick = function() {
      popup.classList.remove('active');
    };
  }
}

function saveProgressAndExit(targetUrl) {
  const saveData = {
    user_id: userId,
    answers: answers,
    current_question: currentQuestionIndex
  };
  
  fetch('/api/save-progress', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(saveData)
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      hasUnsavedChanges = false;
      window.location.href = targetUrl;
    }
  })
  .catch(error => {
    console.error('Error saving progress:', error);
    alert('Gagal menyimpan progress. Coba lagi.');
  });
}

function startTest() {
  if (!questionsData || questionsData.length === 0) {
    showValidationModal('Data Tidak Tersedia', 'Data pertanyaan tidak tersedia. Silakan hubungi admin.');
    return;
  }
  
  totalQuestions = questionsData.length;
  
  document.getElementById('introContent').classList.add('d-none');
  document.getElementById('questionContent').classList.remove('d-none');
  
  startTimer();
  loadQuestion();
  hasUnsavedChanges = true;
}

function startTimer() {
  timer = setInterval(function() {
    timeRemaining--;
    updateTimerDisplay();
    
    if (timeRemaining <= 0) {
      clearInterval(timer);
      showValidationModal('Waktu Habis!', 'Tes akan otomatis disubmit.');
      setTimeout(() => {
        submitTest();
      }, 2000);
    }
  }, 1000);
}

function updateTimerDisplay() {
  const hours = Math.floor(timeRemaining / 3600);
  const minutes = Math.floor((timeRemaining % 3600) / 60);
  const seconds = timeRemaining % 60;
  
  const display = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  document.getElementById('timer').textContent = display;
  
  // Warning when time is running out
  if (timeRemaining <= 300) { // 5 minutes
    document.getElementById('timer').style.color = '#dc2626';
  }
}

function loadQuestion() {
  const question = questionsData[currentQuestionIndex];
  
  // Update question text
  document.getElementById('questionText').textContent = question.text;
  
  // Update counter
  document.getElementById('questionCounter').textContent = 
    `Pertanyaan ${currentQuestionIndex + 1} dari ${totalQuestions}`;
  
  // Update progress bar
  const progress = ((currentQuestionIndex + 1) / totalQuestions) * 100;
  document.getElementById('progressBar').style.width = progress + '%';
  
  // Reset answer buttons
  document.querySelectorAll('.tes-answer-btn').forEach(btn => {
    btn.classList.remove('active');
  });
  
  // Reset current answer
  currentAnswer = null;
  document.getElementById('btnNextTest').style.opacity = '0.6';
  
  // Restore saved answer if exists
  const questionId = question.id;
  if (answers[questionId]) {
    currentAnswer = answers[questionId];
    const selectedBtn = document.querySelector(`[data-value="${currentAnswer}"]`);
    if (selectedBtn) {
      selectedBtn.classList.add('active');
      document.getElementById('btnNextTest').style.opacity = '1';
    }
  }
  
  // Update navigation buttons
  const btnPrev = document.getElementById('btnPrevTest');
  const btnNext = document.getElementById('btnNextTest');
  
  btnPrev.style.display = currentQuestionIndex > 0 ? 'block' : 'none';
  
  if (currentQuestionIndex === totalQuestions - 1) {
    btnNext.innerHTML = 'Selesai <i class="bi bi-check-circle"></i>';
  } else {
    btnNext.innerHTML = 'Selanjutnya <i class="bi bi-arrow-right"></i>';
  }
}

function selectAnswer(button) {
  // Remove active from all buttons
  document.querySelectorAll('.tes-answer-btn').forEach(btn => {
    btn.classList.remove('active');
  });
  
  // Add active to clicked button
  button.classList.add('active');
  
  // Save answer temporarily
  currentAnswer = parseInt(button.dataset.value);
  
  // Enable next button
  document.getElementById('btnNextTest').style.opacity = '1';
  
  // Mark as having unsaved changes
  hasUnsavedChanges = true;
}


function prevQuestion() {
  if (currentQuestionIndex > 0) {
    currentQuestionIndex--;
    loadQuestion();
  }
}

function nextQuestion() {
  // Validate answer selected - LANGSUNG MODAL, TANPA ALERT
  if (currentAnswer === null) {
    showValidationModal('Mohon Pilih Jawaban Terlebih Dahulu', 
                        'Anda harus memilih salah satu jawaban sebelum melanjutkan.');
    return;
  }
  
  const questionId = questionsData[currentQuestionIndex].id;
  answers[questionId] = currentAnswer;
  
  autoSaveProgress();
  currentAnswer = null;
  
  if (currentQuestionIndex < totalQuestions - 1) {
    currentQuestionIndex++;
    loadQuestion();
  } else {
    const confirmModal = new bootstrap.Modal(document.getElementById('ConfirmTestModal'));
    confirmModal.show();
  }
}

function showValidationModal(title, message) {
  const modal = document.getElementById('ValidationModal');
  const modalTitle = modal.querySelector('h4');
  const modalMessage = modal.querySelector('p');
  
  if (modalTitle) modalTitle.innerHTML = `<b>${title}</b>`;
  if (modalMessage) modalMessage.textContent = message;
  
  const validationModal = new bootstrap.Modal(modal);
  validationModal.show();
}

function showValidationModal() {
  const validationModal = new bootstrap.Modal(document.getElementById('ValidationModal'));
  validationModal.show();
}

// Hapus fungsi showValidationPopup() yang lama jika ada

// Close validation popup
document.getElementById('btnValidationOk')?.addEventListener('click', function() {
  document.getElementById('validationPopup').classList.remove('active');
});

// Close popup when clicking outside
document.getElementById('validationPopup')?.addEventListener('click', function(e) {
  if (e.target === this) {
    this.classList.remove('active');
  }
});

function autoSaveProgress() {
  // Debounced auto-save
  clearTimeout(window.autoSaveTimeout);
  window.autoSaveTimeout = setTimeout(() => {
    fetch('/api/auto-save-progress', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        answers: answers,
        current_question: currentQuestionIndex
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        console.log('✅ Auto-saved:', data.answers_saved, 'answers');
        hasUnsavedChanges = false;
      }
    })
    .catch(error => console.error('Auto-save error:', error));
  }, 1000); // Save after 1 second of no activity
}

function submitTest() {
  if (Object.keys(answers).length < totalQuestions) {
    showValidationModal('Pertanyaan Belum Lengkap', 
                        `Masih ada ${totalQuestions - Object.keys(answers).length} pertanyaan yang belum dijawab!`);
    return;
  }
  
  if (timer) clearInterval(timer);
  
  const timeTaken = 3600 - timeRemaining;
  const submitData = {
    user_id: userId,
    answers: answers,
    time_taken: timeTaken
  };
  
  isSubmitting = true; // Bypass exit warning
  
  fetch('/api/submit-test', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(submitData)
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      hasUnsavedChanges = false;
      const finishModal = new bootstrap.Modal(document.getElementById('FinishTestModal'));
      finishModal.show();
      
      setTimeout(() => {
        window.location.href = data.redirect || '/hasil-tes';
      }, 2000);
    } else {
      isSubmitting = false;
      showValidationModal('Gagal Submit', 'Terjadi kesalahan: ' + data.message);
    }
  })
  .catch(error => {
    console.error('Submit error:', error);
    isSubmitting = false;
    showValidationModal('Gagal Submit', 'Gagal submit tes. Silakan coba lagi.');
  });
}