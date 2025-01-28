document.addEventListener('DOMContentLoaded', () => {
    const messageContainer = document.getElementById('message-container');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const feedbackInput = document.getElementById('feedback-input');
    const feedbackButton = document.getElementById('feedback-button');
    const langToggle = document.getElementById('lang-toggle');
    const chatHeaderTitle = document.getElementById('chat-header-title');

    let currentLanguage = 'en';

    const greetings = {
        "hello": "Hello! How can I assist you today?",
        "hi": "Hi there! How can I help you?",
        "good morning": "Good morning! How can I assist you today?",
        "good afternoon": "Good afternoon! How can I help you?",
        "good evening": "Good evening! How can I assist you today?",
        "good night": "Good night! If you have any more questions, feel free to ask tomorrow.",
        "thank you": "You're welcome! If you have any more questions, feel free to ask.",
        "thanks": "You're welcome! If you have any more questions, feel free to ask.",
        "ok" : "Yes, I'm always here to assit you"
    };

    const tamilGreetings = {
        "வணக்கம்": "வணக்கம்! என்னால் எப்படி உதவ முடியும்?",
        "ஹலோ": "ஹலோ! நான் உங்களுக்கு எப்படி உதவ முடியும்?",
        "நலம்": "நலம்! நான் உங்களுக்கு எப்படி உதவ முடியும்?",
    };

    langToggle.addEventListener('click', () => {
        // Toggle the language
        if (currentLanguage === 'en') {
            currentLanguage = 'ta';
            langToggle.textContent = 'English';
            // Translate the UI to Tamil
            translateUITamil();
        } else {
            currentLanguage = 'en';
            langToggle.textContent = 'Tamil';
            // Translate the UI to English
            translateUIEnglish();
        }
    });

    function translateUITamil() {
        // Translate the UI elements to Tamil
        chatHeaderTitle.textContent = 'வேளாண் சாட்போட்';
        userInput.placeholder = 'உங்கள் கேள்வியை இங்கே எழுதவும்...';
        sendButton.textContent = 'அனுப்பு';
        feedbackInput.placeholder = 'உங்கள் கருத்துக்களை இங்கே எழுதவும்...';
        feedbackButton.textContent = 'சமர்ப்பிக்கவும்';
    }
    
    function translateUIEnglish() {
        // Translate the UI elements to English
        chatHeaderTitle.textContent = 'Veterinary Chatbot';
        userInput.placeholder = 'Type your question here...';
        sendButton.textContent = 'Send';
        feedbackInput.placeholder = 'Enter your feedback here...';
        feedbackButton.textContent = 'Submit Feedback';
    }
});

document.getElementById('send-button').addEventListener('click', async () => {
    const userInput = document.getElementById('user-input');
    const messageContainer = document.getElementById('message-container');
    const langToggle = document.getElementById('lang-toggle');

    let currentLanguage = 'en';
    if (langToggle.textContent === 'English') {
        currentLanguage = 'ta';
    }

    const greetings = {
        "hello": "Hello! How can I assist you today?",
        "hi": "Hi there! How can I help you?",
        "good morning": "Good morning! How can I assist you today?",
        "good afternoon": "Good afternoon! How can I help you?",
        "good evening": "Good evening! How can I assist you today?",
        "good night": "Good night! If you have any more questions, feel free to ask tomorrow.",
        "thank you": "You're welcome! If you have any more questions, feel free to ask.",
        "thanks": "You're welcome! If you have any more questions, feel free to ask.",
        "ok" : "Yes, I'm always here to assit you"
    };

    const tamilGreetings = {
        "வணக்கம்": "வணக்கம்! என்னால் எப்படி உதவ முடியும்?",
        "ஹலோ": "ஹலோ! நான் உங்களுக்கு எப்படி உதவ முடியும்?",
        "நலம்": "நலம்! நான் உங்களுக்கு எப்படி உதவ முடியும்?",
    };

    const userQuery = userInput.value.trim().toLowerCase();
    if (!userQuery) {
        alert('Please enter a query!');
        return;
    }

    const userQueryDiv = document.createElement('div');
    userQueryDiv.className = 'user-query';
    userQueryDiv.innerText = `User: ${userQuery}`;
    messageContainer.appendChild(userQueryDiv);

    let chatbotResponse;

    try {
        // Check for predefined greetings
        if (currentLanguage === 'ta') {
            if (tamilGreetings[userQuery]) {
                chatbotResponse = tamilGreetings[userQuery];
            } else {
                // Send query to the backend for processing
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: userQuery }),
                });

                const data = await response.json();
                chatbotResponse = data.response.treatment;
            }
        } else {
            if (greetings[userQuery]) {
                chatbotResponse = greetings[userQuery];
            } else {
                // Send query to the backend for processing
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: userQuery }),
                });

                const data = await response.json();
                chatbotResponse = data.response.treatment;
            }
        }

        const responseDiv = document.createElement('div');
        responseDiv.className = 'chatbot-response';
        responseDiv.innerHTML = chatbotResponse
            .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
            .replace(/\n/g, '<br>');
        messageContainer.appendChild(responseDiv);

        userInput.value = '';
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to process your query. Please try again.');
    }
});

document.getElementById('feedback-button').addEventListener('click', async () => {
    const feedbackInput = document.getElementById('feedback-input');

    const feedback = feedbackInput.value.trim();
    if (!feedback) {
        alert('Please enter your feedback!');
        return;
    }

    try {
        const response = await fetch('/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ feedback: feedback }),
        });

        const data = await response.json();
        if (data.success) {
            alert('Thank you for your feedback!');
            feedbackInput.value = '';
        } else {
            alert('Failed to submit feedback. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to submit feedback. Please try again.');
    }
});
