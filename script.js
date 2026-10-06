// =========================================================
// STUDENT PROFILE
// =========================================================

let studentProfile = {
    name: "",
    education: "",
    career: "",
    skills: []
};


// Selected AI Tutor learning level
let selectedLearningMode = "Beginner";


// =========================================================
// CHECK LOGIN
// =========================================================

async function checkLogin() {

    try {

        const response =
            await fetch("/api/current-user");

        const data =
            await response.json();

        if (!data.logged_in) {

            window.location.href = "/login";

            return;

        }

        studentProfile =
            data.user;

        // Fill profile
        document.getElementById(
            "studentName"
        ).value =
            studentProfile.name || "";

        document.getElementById(
            "educationLevel"
        ).value =
            studentProfile.education || "";

        document.getElementById(
            "profileCareer"
        ).value =
            studentProfile.career || "";

        document.getElementById(
            "profileSkills"
        ).value =
            studentProfile.skills.join(", ");

        // Update dashboard
        document.getElementById(
            "dashboardTitle"
        ).innerText =
            `Welcome, ${studentProfile.name}! 👋`;

        // Automatically fill skill analysis
        document.getElementById(
            "skills"
        ).value =
            studentProfile.skills.join(", ");

        document.getElementById(
            "career"
        ).value =
            studentProfile.career || "";

        // If profile exists, analyze automatically
        if (
            studentProfile.career &&
            studentProfile.skills.length > 0
        ) {

            analyzeSkills();

        }

        // Tutor greeting
        document.getElementById(
            "chatMessages"
        ).innerHTML = `

            <div class="bot-message">

                👋 Hello
                <strong>
                    ${studentProfile.name}
                </strong>!

                <br><br>

                Welcome back to your
                personalized EduTech learning journey.

                <br><br>

                You are currently in
                <strong>
                    ${selectedLearningMode} Mode
                </strong>.

            </div>

        `;

    }

    catch (error) {

        console.error(error);

        window.location.href = "/login";

    }

}


// =========================================================
// LOGOUT
// =========================================================

async function logout() {

    try {

        await fetch(
            "/api/logout",
            {
                method: "POST"
            }
        );

        window.location.href =
            "/login";

    }

    catch (error) {

        console.error(error);

    }

}


// =========================================================
// SCROLL
// =========================================================

function scrollToSection(id) {

    const element =
        document.getElementById(id);

    if (element) {

        element.scrollIntoView({
            behavior: "smooth"
        });

    }

}


// =========================================================
// SELECT LEARNING MODE
// =========================================================

function selectLearningMode(
    level,
    button
) {

    selectedLearningMode =
        level;

    document
        .querySelectorAll(".mode-btn")
        .forEach(btn => {

            btn.classList.remove(
                "active"
            );

        });

    button.classList.add(
        "active"
    );

    document.getElementById(
        "currentLearningMode"
    ).innerText =
        "● " + level + " Mode";

}


// =========================================================
// SAVE PROFILE
// =========================================================

async function saveProfile() {

    const name =
        document
        .getElementById("studentName")
        .value
        .trim();

    const education =
        document
        .getElementById("educationLevel")
        .value;

    const career =
        document
        .getElementById("profileCareer")
        .value;

    const skillsInput =
        document
        .getElementById("profileSkills")
        .value;

    if (
        !name ||
        !education ||
        !career ||
        !skillsInput
    ) {

        alert(
            "Please complete your full profile!"
        );

        return;

    }

    const skills =
        skillsInput
        .split(",")
        .map(
            skill => skill.trim()
        )
        .filter(
            skill => skill !== ""
        );


    try {

        const response =
            await fetch(
                "/api/profile",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        education:
                            education,

                        career:
                            career,

                        skills:
                            skills

                    })

                }
            );


        const data =
            await response.json();


        if (!data.success) {

            alert(
                data.message ||
                "Could not save profile."
            );

            return;

        }


        studentProfile = {

            name: name,

            education: education,

            career: career,

            skills: skills

        };


        document.getElementById(
            "dashboardTitle"
        ).innerText =
            `Welcome, ${name}! 👋`;


        const welcome =
            document.getElementById(
                "profileWelcome"
            );


        welcome.innerHTML = `

            <h2>
                Welcome, ${name}! 🎉
            </h2>

            <p>
                Your personalized learning journey
                has been created.
            </p>

            <p>
                <strong>Education:</strong>
                ${education}
            </p>

            <p>
                <strong>Career Goal:</strong>
                ${career}
            </p>

            <p>
                <strong>Current Skills:</strong>
                ${skills.join(", ")}
            </p>

        `;


        welcome.classList.remove(
            "hidden"
        );


        document.getElementById(
            "skills"
        ).value =
            skills.join(", ");


        document.getElementById(
            "career"
        ).value =
            career;


        document.getElementById(
            "chatMessages"
        ).innerHTML = `

            <div class="bot-message">

                👋 Hello
                <strong>${name}</strong>!

                <br><br>

                I know you are a
                <strong>${education}</strong>
                working toward becoming a
                <strong>${career}</strong>.

                <br><br>

                Your AI Tutor is currently in
                <strong>
                    ${selectedLearningMode}
                    Mode
                </strong>.

                <br><br>

                Ask me anything about your
                learning journey!

            </div>

        `;


        await analyzeSkills();


        welcome.scrollIntoView({
            behavior: "smooth"
        });

    }

    catch (error) {

        console.error(error);

        alert(
            "Could not save your profile."
        );

    }

}


// =========================================================
// QUIZ
// =========================================================

async function submitQuiz() {

    let answers = [];


    for (
        let i = 1;
        i <= 5;
        i++
    ) {

        const selected =
            document.querySelector(
                `input[name="q${i}"]:checked`
            );


        if (!selected) {

            alert(
                "Please answer all questions!"
            );

            return;

        }


        answers.push(
            selected.value
        );

    }


    try {

        const response =
            await fetch(
                "/api/quiz-result",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        answers: answers
                    })

                }
            );


        const data =
            await response.json();


        const resultBox =
            document.getElementById(
                "quizResult"
            );


        let greeting = "";


        if (studentProfile.name) {

            greeting =
                `Great job, ${studentProfile.name}!`;

        }


        resultBox.innerHTML = `

            <h2>
                🎓 ${greeting}
            </h2>

            <h3>
                Your Learning Analysis
            </h3>

            <br>

            <h1>
                ${data.score}/${data.total}
            </h1>

            <h3>
                ${data.percentage}%
                •
                ${data.level}
            </h3>

            <br>

            <p>
                ${data.recommendation}
            </p>

        `;


        resultBox.classList.remove(
            "hidden"
        );


        document.getElementById(
            "quizStat"
        ).innerText =
            data.level;


        resultBox.scrollIntoView({
            behavior: "smooth"
        });

    }

    catch (error) {

        alert(
            "Something went wrong."
        );

        console.error(error);

    }

}


// =========================================================
// ANALYZE SKILLS
// =========================================================

async function analyzeSkills() {

    const skillsInput =
        document
        .getElementById("skills")
        .value;

    const career =
        document
        .getElementById("career")
        .value;


    if (
        !skillsInput ||
        !career
    ) {

        return;

    }


    const skills =
        skillsInput
        .split(",")
        .map(
            skill => skill.trim()
        )
        .filter(
            skill => skill !== ""
        );


    try {

        const response =
            await fetch(
                "/api/skill-gap",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        skills: skills,

                        career: career

                    })

                }
            );


        const data =
            await response.json();


        document.getElementById(
            "careerTitle"
        ).innerText =
            data.career;


        document.getElementById(
            "progressNumber"
        ).innerText =
            data.progress + "%";


        document.getElementById(
            "progressStat"
        ).innerText =
            data.progress + "%";


        document.getElementById(
            "skillsStat"
        ).innerText =
            data.matched_skills.length +
            "/" +
            data.required_skills.length;


        const matchedContainer =
            document.getElementById(
                "matchedSkills"
            );


        const missingContainer =
            document.getElementById(
                "missingSkills"
            );


        matchedContainer.innerHTML =
            "";

        missingContainer.innerHTML =
            "";


        if (
            data.matched_skills.length === 0
        ) {

            matchedContainer.innerHTML =
                "<p>No matching skills yet.</p>";

        }

        else {

            data.matched_skills.forEach(
                skill => {

                    matchedContainer.innerHTML +=
                        `<span class="skill-tag">
                            ${skill}
                        </span>`;

                }
            );

        }


        if (
            data.missing_skills.length === 0
        ) {

            missingContainer.innerHTML =
                "<p>🎉 No major skill gaps found!</p>";

        }

        else {

            data.missing_skills.forEach(
                skill => {

                    missingContainer.innerHTML +=
                        `<span class="skill-tag missing">
                            ${skill}
                        </span>`;

                }
            );

        }


        document.getElementById(
            "skillResult"
        ).classList.remove(
            "hidden"
        );


        generateRoadmap(data);

    }

    catch (error) {

        console.error(error);

        alert(
            "Could not analyze skills. Please try again."
        );

    }

}


// =========================================================
// ROADMAP
// =========================================================

function generateRoadmap(data) {

    const roadmap =
        document.getElementById(
            "roadmapContainer"
        );


    roadmap.innerHTML =
        "";


    if (studentProfile.name) {

        roadmap.innerHTML += `

            <div class="roadmap-item">

                <div class="step">
                    👤
                </div>

                <div>

                    <h3>
                        ${studentProfile.name}'s
                        Learning Journey
                    </h3>

                    <p>
                        Personalized roadmap for
                        becoming a
                        ${data.career}.
                    </p>

                </div>

            </div>

        `;

    }


    if (
        data.matched_skills.length > 0
    ) {

        roadmap.innerHTML += `

            <div class="roadmap-item">

                <div class="step">
                    ✓
                </div>

                <div>

                    <h3>
                        Current Strengths
                    </h3>

                    <p>
                        You already know:
                        ${data.matched_skills.join(", ")}
                    </p>

                </div>

            </div>

        `;

    }


    data.missing_skills.forEach(
        (skill, index) => {

            roadmap.innerHTML += `

                <div class="roadmap-item">

                    <div class="step">
                        ${index + 1}
                    </div>

                    <div>

                        <h3>
                            Learn ${skill}
                        </h3>

                        <p>
                            Build your understanding
                            of ${skill} to move closer
                            to your career goal.
                        </p>

                    </div>

                </div>

            `;

        }
    );


    if (
        data.missing_skills.length === 0
    ) {

        roadmap.innerHTML += `

            <div class="roadmap-item">

                <div class="step">
                    🚀
                </div>

                <div>

                    <h3>
                        Congratulations!
                    </h3>

                    <p>
                        You have all the core
                        skills required for
                        this career.
                    </p>

                </div>

            </div>

        `;

    }

}


// =========================================================
// AI TUTOR
// =========================================================

async function askTutor() {

    const input =
        document.getElementById(
            "userQuestion"
        );


    const question =
        input.value.trim();


    if (!question) {

        return;

    }


    const chatMessages =
        document.getElementById(
            "chatMessages"
        );


    const userMessage =
        document.createElement(
            "div"
        );


    userMessage.className =
        "user-message";


    userMessage.textContent =
        question;


    chatMessages.appendChild(
        userMessage
    );


    input.value = "";


    chatMessages.scrollTop =
        chatMessages.scrollHeight;


    try {

        const response =
            await fetch(
                "/api/tutor",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        question:
                            question,

                        level:
                            selectedLearningMode

                    })

                }
            );


        if (!response.ok) {

            throw new Error(
                "Tutor API error"
            );

        }


        const data =
            await response.json();


        const botMessage =
            document.createElement(
                "div"
            );


        botMessage.className =
            "bot-message";


        let answer =
            data.answer;


        if (
            studentProfile.name
        ) {

            answer =
                `${studentProfile.name}, ${answer}`;

        }


        botMessage.textContent =
            "🤖 " + answer;


        chatMessages.appendChild(
            botMessage
        );


        chatMessages.scrollTop =
            chatMessages.scrollHeight;

    }

    catch (error) {

        console.error(error);


        const errorMessage =
            document.createElement(
                "div"
            );


        errorMessage.className =
            "bot-message";


        errorMessage.textContent =
            "🤖 Sorry, I couldn't connect right now. Please try again.";


        chatMessages.appendChild(
            errorMessage
        );


        chatMessages.scrollTop =
            chatMessages.scrollHeight;

    }

}


// =========================================================
// ENTER KEY
// =========================================================

function handleEnter(event) {

    if (
        event.key === "Enter"
    ) {

        askTutor();

    }

}


// =========================================================
// START
// =========================================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        checkLogin();

    }
);