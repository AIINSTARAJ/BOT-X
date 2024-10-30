const chatMessages = document.getElementById('chat-messages');

const messageInput = document.getElementById('message-input');

const sendButton = document.getElementById('send-button');

sendButton.addEventListener('click', sendMessage);

function sendMessage() {

    const userMessage = messageInput.value;

    if (userMessage !== '') {

        displayMessage(userMessage, 'user');

        messageInput.value = '';

        fetch('/bot-api', {

            method: 'POST',

            headers: {

                'Content-Type': 'application/json'

            },

            body: JSON.stringify(
            { message: userMessage }
            )
        })

        .then(response => response.json())

        .then(data => {

            displayMessage(data.response, 'bot');

        });

    }

}

function displayMessage(message, type) {

    const messageElement = document.createElement('div');

    messageElement.classList.add('message');

    if (type === 'user') {

        messageElement.classList.add('user-message');

    } else {

        messageElement.classList.add('bot-message');

    }

    messageElement.innerText = message;

    chatMessages.appendChild(messageElement);

    chatMessages.scrollTop = chatMessages.scrollHeight;

}