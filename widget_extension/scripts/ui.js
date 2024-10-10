(function () {
    'use strict';

    window.createChatbotUI = function () {
        const toggleButton = document.createElement('div');
        toggleButton.id = 'chatbot-toggle-button';
        toggleButton.innerHTML = '💬';
        document.body.appendChild(toggleButton);

        const chatbotContainer = document.createElement('div');
        chatbotContainer.id = 'chatbot';
        document.body.appendChild(chatbotContainer);

        chatbotContainer.innerHTML = `
            <div id="chatbot-header">
                <h2>Wiki Helper</h2>
            </div>
            <div id="chatbot-messages"></div>
            <div id="chatbot-input">
                <input type="text" id="user-input" placeholder="Type your question here..." autocomplete="off" />
                <button id="send-button">Send</button>
            </div>
            <!-- Resize Handles -->
            <div class="resize-handle nw"></div>
            <div class="resize-handle ne"></div>
            <div class="resize-handle sw"></div>
            <div class="resize-handle se"></div>
            <div class="resize-handle n"></div>
            <div class="resize-handle s"></div>
            <div class="resize-handle e"></div>
            <div class="resize-handle w"></div>
        `;

        return {
            toggleButton,
            chatbotContainer
        };
    };

    window.appendMessage = function (sender, message, senderType) {
        const messagesDiv = document.getElementById('chatbot-messages');
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', senderType + '-message');

        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.innerHTML = message;

        messageElement.appendChild(messageContent);
        messagesDiv.appendChild(messageElement);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    };

    window.disableInput = function () {
        document.getElementById('user-input').disabled = true;
        document.getElementById('send-button').disabled = true;
    };

    window.enableInput = function () {
        document.getElementById('user-input').disabled = false;
        document.getElementById('send-button').disabled = false;
    };
})();
