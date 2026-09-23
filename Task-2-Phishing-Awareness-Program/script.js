function showDemoMessage() {
    const message = document.getElementById("demo-message");

    message.textContent =
        "Training example: Never enter real credentials into a suspicious login page.";

    message.style.display = "block";
}


function calculateScore() {

    const correctAnswers = {
        q1: "a",
        q2: "c",
        q3: "a",
        q4: "b",
        q5: "a"
    };

    let score = 0;
    let answered = 0;

    for (const question in correctAnswers) {

        const selected = document.querySelector(
            `input[name="${question}"]:checked`
        );

        if (selected) {
            answered++;

            if (selected.value === correctAnswers[question]) {
                score++;
            }
        }
    }

    const result = document.getElementById("quiz-result");

    let message;

    if (answered < 5) {

        message = `
            <h3>Please answer all questions.</h3>
            <p>
                You answered ${answered} out of 5 questions.
            </p>
        `;

    } else {

        const percentage = (score / 5) * 100;

        if (percentage === 100) {

            message = `
                <h3>Excellent work!</h3>
                <p>
                    Your score is ${score}/5 (${percentage}%).
                    You demonstrated strong phishing awareness.
                </p>
            `;

        } else if (percentage >= 60) {

            message = `
                <h3>Good effort!</h3>
                <p>
                    Your score is ${score}/5 (${percentage}%).
                    Review the warning signs and security tips to improve
                    your phishing awareness.
                </p>
            `;

        } else {

            message = `
                <h3>Keep learning.</h3>
                <p>
                    Your score is ${score}/5 (${percentage}%).
                    Review the training material and try the quiz again.
                </p>
            `;
        }
    }

    result.innerHTML = message;
    result.classList.add("show");

    result.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}