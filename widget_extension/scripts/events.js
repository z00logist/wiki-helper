(function () {
    'use strict';

    window.initializeListeners = function (toggleButton, chatbotContainer, originalStyles) {
        const sendButton = document.getElementById('send-button');
        const userInputField = document.getElementById('user-input');

        sendButton.addEventListener('click', function () {
            const userInput = userInputField.value.trim();
            if (userInput !== '') {
                if (window.requestInProgress) {
                    appendMessage('Wiki Helper', 'Please wait until the current request is complete.', 'bot');
                    return;
                }

                window.userInteraction = true;
                appendMessage('You', userInput, 'user');
                userInputField.value = '';

                if (!window.isTrained && !window.isTraining) {
                    window.isTraining = true;
                    window.requestInProgress = true;
                    disableInput();
                    appendMessage('Wiki Helper', 'Let me read the article first. Please wait...', 'bot');
                    window.messageQueue.push(userInput);
                    trainModelWithCurrentPage(window.location.href);
                } else if (window.isTraining) {
                    appendMessage('Wiki Helper', 'Still reading. Will answer later.', 'bot');
                    window.messageQueue.push(userInput);
                } else {
                    window.requestInProgress = true;
                    disableInput();
                    sendQuestion(userInput);
                }
            }
        });

        userInputField.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                sendButton.click();
            }
        });

        toggleButton.addEventListener('click', function () {
            if (chatbotContainer.style.display === 'none') {
                chatbotContainer.style.width = originalStyles.width;
                chatbotContainer.style.height = originalStyles.height;
                chatbotContainer.style.top = originalStyles.top;
                chatbotContainer.style.left = originalStyles.left;
                chatbotContainer.style.bottom = originalStyles.bottom;
                chatbotContainer.style.right = originalStyles.right;

                chatbotContainer.style.display = 'flex';
            } else {
                chatbotContainer.style.display = 'none';
            }
        });
    };
})();
