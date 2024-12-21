chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'activate') {
        console.log("Extension activated.");
        // Add activation logic here
    } else if (request.action === 'deactivate') {
        console.log("Extension deactivated.");
        // Add deactivation logic here
    }
});
