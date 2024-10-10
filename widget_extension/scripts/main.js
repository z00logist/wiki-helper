(function () {
    'use strict';

    window.isTraining = false;
    window.isTrained = false;
    window.messageQueue = [];
    window.userInteraction = false;
    window.requestInProgress = false;

    const originalStyles = {
        width: '360px',
        height: '500px',
        top: '',
        left: '',
        bottom: '90px',
        right: '20px'
    };

    const { toggleButton, chatbotContainer } = createChatbotUI();

    initDragElement(chatbotContainer);
    initResizeElement(chatbotContainer);

    initializeListeners(toggleButton, chatbotContainer, originalStyles);

    setTimeout(() => {
        if (!window.userInteraction) {
            appendMessage('Wiki Helper', 'Hi! Ask me anything.', 'bot');
        }
    }, 5000);
})();
