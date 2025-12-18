// Test Management - Fixed Version
document.addEventListener("DOMContentLoaded", () => {
    
    // Check if we're on the test page
    if (typeof questionsData === 'undefined' || !questionsData || questionsData.length === 0) {
        console.log("No questions data found or not on test page");
        return;
    }

    console.log("Test initialized with", questionsData.length, "questions");

    let currentQuestion = 0;
    let answers = {};
    let timerInterval;
    let timeRemaining = 3600; // 1 hour in seconds

    const btnMulaiTes = document.getElementById("btn-start-test");
    const introContent = document.getElementById("introContent");
    const questionContent = document.getElementById("questionContent");
    const tesWrapper = document.getElementById("test-wrapper");
    const btnNext = document.getElementById("btnNextTest");
    const btnPrev = document.getElementById("btnPrevTest");
    const answerButtons = document.querySelectorAll(".tes-answer-btn");
    const questionText = document.getElementById("questionText");
    const questionCounter = document.getElementById("questionCounter");
    const progressBar = document.getElementById("progressBar");
    const timerDisplay = document.getElementById("timer");
    const confirmTestModal = document.getElementById("ConfirmTestModal");
    const finishTestModal = document.getElementById("FinishTestModal");
    const btnConfirmSubmit = document.getElementById("btnConfirmSubmit");

    // Start Timer
    function startTimer() {
        timerInterval = setInterval(() => {
            timeRemaining--;
            
            const hours = Math.floor(timeRemaining / 3600);
            const minutes = Math.floor((timeRemaining % 3600) / 60);
            const seconds = timeRemaining % 60;
            
            timerDisplay.textContent = 
                `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            
            if (timeRemaining <= 0) {
                clearInterval(timerInterval);
                autoSubmitTest();
            }
        }, 1000);
    }

    // Load Question
    function loadQuestion(index) {
        if (!questionsData || !questionsData[index]) {
            console.error("Question not found at index", index);
            return;
        }

        const question = questionsData[index];
        console.log("Loading question", index + 1, ":", question);
        
        questionText.textContent = question.text;
        questionCounter.textContent = `Pertanyaan ${index + 1} dari ${questionsData.length}`;
        
        // Update progress bar
        const progress = ((index + 1) / questionsData.length) * 100;
        progressBar.style.width = `${progress}%`;

        // Reset answer buttons
        answerButtons.forEach(btn => btn.classList.remove("active"));

        // Load saved answer if exists
        if (answers[question.id]) {
            answerButtons.forEach(btn => {
                if (parseInt(btn.dataset.value) === answers[question.id]) {
                    btn.classList.add("active");
                }
            });
        }

        // Show/hide navigation buttons
        btnPrev.style.display = index > 0 ? "block" : "none";
        
        // Change next button to finish on last question
        if (index === questionsData.length - 1) {
            btnNext.innerHTML = 'Selesai <i class="bi bi-check-circle"></i>';
        } else {
            btnNext.innerHTML = 'Selanjutnya <i class="bi bi-arrow-right"></i>';
        }
    }

    // Start Test
    if (btnMulaiTes && introContent && questionContent && tesWrapper) {
        btnMulaiTes.addEventListener("click", () => {
            console.log("Starting test...");
            introContent.classList.add("d-none");
            questionContent.classList.remove("d-none");
            tesWrapper.classList.add("no-paper");
            startTimer();
            loadQuestion(0);
        });
    }

    // Select Answer
    answerButtons.forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.preventDefault();
            
            // Remove active from all buttons
            answerButtons.forEach(b => b.classList.remove("active"));
            
            // Add active to clicked button
            btn.classList.add("active");
            
            const questionId = questionsData[currentQuestion].id;
            answers[questionId] = parseInt(btn.dataset.value);
            
            console.log("Answer selected for question", questionId, ":", answers[questionId]);
            console.log("Total answers:", Object.keys(answers).length);
        });
    });

    // Next Button
    if (btnNext) {
        btnNext.addEventListener("click", (e) => {
            e.preventDefault();
            
            const questionId = questionsData[currentQuestion].id;
            
            // Check if answer is selected
            if (!answers[questionId]) {
                alert("Silakan pilih jawaban terlebih dahulu!");
                return;
            }

            console.log("Next button clicked. Current question:", currentQuestion);

            if (currentQuestion === questionsData.length - 1) {
                // Last question - show confirmation modal
                console.log("Last question reached. Showing confirmation modal.");
                const modal = new bootstrap.Modal(confirmTestModal);
                modal.show();
            } else {
                // Go to next question
                currentQuestion++;
                console.log("Moving to question:", currentQuestion + 1);
                loadQuestion(currentQuestion);
            }
        });
    }

    // Previous Button
    if (btnPrev) {
        btnPrev.addEventListener("click", (e) => {
            e.preventDefault();
            
            if (currentQuestion > 0) {
                currentQuestion--;
                console.log("Moving back to question:", currentQuestion + 1);
                loadQuestion(currentQuestion);
            }
        });
    }

    // Confirm Submit
    if (btnConfirmSubmit) {
        btnConfirmSubmit.addEventListener("click", (e) => {
            e.preventDefault();
            console.log("Submit confirmed");
            submitTest();
        });
    }

    // Submit Test
    function submitTest() {
        console.log("Submitting test...");
        
        // Close confirmation modal
        const confirmModal = bootstrap.Modal.getInstance(confirmTestModal);
        if (confirmModal) confirmModal.hide();

        // Stop timer
        clearInterval(timerInterval);

        // Prepare data
        const testData = {
            user_id: userId,
            answers: answers,
            time_taken: 3600 - timeRemaining
        };

        console.log("Submitting data:", testData);

        // Send to server
        fetch('/api/submit-test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(testData)
        })
        .then(response => {
            console.log("Response status:", response.status);
            return response.json();
        })
        .then(data => {
            console.log("Response data:", data);
            
            if (data.success) {
                // Show finish modal
                const modal = new bootstrap.Modal(finishTestModal);
                modal.show();

                // Redirect after 2 seconds
                setTimeout(() => {
                    window.location.href = '/hasil-tes';
                }, 2000);
            } else {
                alert('Terjadi kesalahan: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Terjadi kesalahan saat mengirim data: ' + error.message);
        });
    }

    // Auto Submit when time runs out
    function autoSubmitTest() {
        alert("Waktu habis! Tes akan otomatis di-submit.");
        submitTest();
    }

    // Save progress before leaving
    window.addEventListener('beforeunload', (e) => {
        if (Object.keys(answers).length > 0 && currentQuestion < questionsData.length - 1) {
            e.preventDefault();
            e.returnValue = '';
            
            // Save progress to server
            fetch('/api/save-progress', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: userId,
                    answers: answers,
                    current_question: currentQuestion
                })
            });
        }
    });
});