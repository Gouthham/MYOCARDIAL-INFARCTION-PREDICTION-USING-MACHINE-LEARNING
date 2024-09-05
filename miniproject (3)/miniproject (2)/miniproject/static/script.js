document.addEventListener('DOMContentLoaded', function () {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const reloadBtn = document.getElementById('reload-btn');

    // Initialize the chatbot conversation
    const botResponses = [
        "Hi there! What’s your name?",
        name => `Nice to meet you, ${name}! How can I help you today?`,
        "Can you tell me more about your symptoms?",
        "Thank you for sharing. I will need to ask you a few more questions to assist you better.",
        "It was nice talking to you. If you have more questions, feel free to ask. Have a great day!"
    ];

    let step = 0;
    let patientName = '';

    function addMessage(content, isBot) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        if (isBot) {
            messageElement.classList.add('chatbot-message');
            messageElement.innerHTML = `
                <img src="https://via.placeholder.com/50" alt="Chatbot Avatar">
                <div class="message-content">
                    <p>${content}</p>
                </div>
            `;
        } else {
            messageElement.classList.add('patient-message');
            messageElement.innerHTML = `
                <div class="patient-icon">
                    <i class="fi fi-ss-user"></i>
                </div>
                <div class="message-content">
                    <p>${content}</p>
                </div>
            `;
        }
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;  // Auto-scroll to the latest message
    }

    function handleUserInput() {
        const text = userInput.value.trim();
        if (text) {
            addMessage(text, false);
            userInput.value = '';

            // Handle chatbot responses
            if (step === 0) {
                patientName = text;
                addMessage(botResponses[1](patientName), true);
                step++;
            } else if (step === 1) {
                addMessage(botResponses[2], true);
                step++;
            } else if (step === 2) {
                addMessage(botResponses[3], true);
                step++;
            } else {
                addMessage(botResponses[4], true);
                step = 0;  // Reset the conversation
            }
        }
    }

    function resetChat() {
        chatMessages.innerHTML = '';
        userInput.value = '';
        step = 0;
        addMessage(botResponses[0], true);
    }

    sendBtn.addEventListener('click', handleUserInput);
    userInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            handleUserInput();
        }
    });

    reloadBtn.addEventListener('click', function () {
        resetChat();
    });

    // Initialize the first message from the bot
    addMessage(botResponses[0], true);
});
