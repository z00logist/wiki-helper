// network.js
(function () {
    'use strict';

    window.trainModelWithCurrentPage = function (url) {
        chrome.runtime.sendMessage({ action: 'trainModel', url: url }, function (response) {
            window.isTraining = false;
            window.requestInProgress = false;
            enableInput();
            if (response && response.result) {
                window.isTrained = true;
                if (window.messageQueue.length > 0) {
                    const firstQuestion = window.messageQueue.shift();
                    sendQuestion(firstQuestion);
                }
            } else {
                appendMessage('Wiki Helper', 'Error occurred while reading. Try again.', 'bot');
                window.messageQueue = [];
            }
        });
    };

    // Send a question to the backend
    window.sendQuestion = function (question) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'bot-message');
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.innerHTML = ''; 
        messageElement.appendChild(messageContent);
        document.getElementById('chatbot-messages').appendChild(messageElement);
        document.getElementById('chatbot-messages').scrollTop = document.getElementById('chatbot-messages').scrollHeight;

        const typingIndicator = document.createElement('div');
        typingIndicator.classList.add('typing-indicator');
        typingIndicator.innerHTML = '<span></span><span></span><span></span>';
        messageContent.appendChild(typingIndicator);

        fetch('http://localhost:8080/inference/answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: question })
        })
        .then(response => {
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let botMessageContent = '';

            function read() {
                return reader.read().then(({ done, value }) => {
                    if (done) {
                        typingIndicator.remove();
                        if (window.messageQueue.length > 0) {
                            const nextQuestion = window.messageQueue.shift();
                            sendQuestion(nextQuestion); 
                        } else {
                            window.requestInProgress = false;
                            enableInput();
                        }
                        return;
                    }
                    const chunk = decoder.decode(value, { stream: true });
                    botMessageContent += chunk;
                    // Update message content
                    messageContent.innerHTML = botMessageContent;
                    // Append typing indicator again
                    messageContent.appendChild(typingIndicator);
                    document.getElementById('chatbot-messages').scrollTop = document.getElementById('chatbot-messages').scrollHeight;
                    return read();
                });
            }

            return read();
        })
        .catch(error => {
            console.error('Error:', error);
            typingIndicator.remove();
            appendMessage('Wiki Helper', 'Unable to answer the question.', 'bot');

            if (window.messageQueue.length > 0) {
                const nextQuestion = window.messageQueue.shift();
                sendQuestion(nextQuestion);
            } else {
                window.requestInProgress = false;
                enableInput();
            }
        });
    };
})();
