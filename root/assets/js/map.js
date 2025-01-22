fetch('assets/world-map.svg')
    .then(response => response.text())
    .then(svg => {
        document.getElementById('world-map').innerHTML = svg;

        // Add click events to countries
        document.querySelectorAll('#world-map path').forEach(country => {
            country.addEventListener('click', () => {
                const countryName = country.getAttribute('data-name');
                if (countryName) {
                    openQuestionModal(countryName);
                }
            });
        });
    });

function openQuestionModal(countryName) {
    const modal = document.getElementById('question-modal');
    const questionDisplay = document.getElementById('question');
    const countryDisplay = document.getElementById('country-name');

    fetch('data/questions.json')
        .then(response => response.json())
        .then(data => {
            const questionData = data.questions.find(q => q.country === countryName);
            if (questionData) {
                countryDisplay.textContent = countryName;
                questionDisplay.textContent = questionData.question;
                modal.dataset.country = countryName;
                modal.classList.remove('hidden');
            } else {
                alert("No question found for this country.");
            }
        });
}

function submitAnswer() {
    const modal = document.getElementById('question-modal');
    const countryName = modal.dataset.country;
    const userAnswer = document.getElementById('answer').value.trim();

    fetch('data/questions.json')
        .then(response => response.json())
        .then(data => {
            const questionData = data.questions.find(q => q.country === countryName);
            const correctAnswerHash = questionData.answerHash;

            const userAnswerHash = sha256(userAnswer); // Use a hashing library
            if (userAnswerHash === correctAnswerHash) {
                alert("Correct! You captured the flag.");
                markCountryCaptured(countryName);
                closeModal();
            } else {
                alert("Incorrect. Try again!");
            }
        });
}

function markCountryCaptured(countryName) {
    const countryElement = document.querySelector(`[data-name="${countryName}"]`);
    if (countryElement) {
        countryElement.classList.add('captured');
    }

    const username = localStorage.getItem('username');
    let scores = JSON.parse(localStorage.getItem('scores')) || {};
    scores[username] = (scores[username] || 0) + 10;
    localStorage.setItem('scores', JSON.stringify(scores));
}

function closeModal() {
    document.getElementById('question-modal').classList.add('hidden');
}
