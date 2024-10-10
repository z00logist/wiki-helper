chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'trainModel') {
        fetch('http://localhost:8080/training/train', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: request.url })
        })
        .then(response => response.json())
        .then(data => {
            sendResponse({ result: data.result });
        })
        .catch(error => {
            console.error('Error during trainModel:', error);
            sendResponse({ result: false, error: error.message });
        });
        return true;
    }
});
