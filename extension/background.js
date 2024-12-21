chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'detect') {
        console.log("Starting deepfake detection...");
        // Add your deepfake detection logic here.
        
        // Example response after processing
        sendResponse({ status: 'Detection completed' });
    }
});
