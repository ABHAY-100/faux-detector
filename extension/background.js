let latestResult = null;

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "updateResult") {
        latestResult = message.data;
        chrome.action.openPopup();
    } else if (message.action === "getResult") {
        sendResponse(latestResult);
        latestResult = null; // Clear the result after sending
    } else if (message.action === "openPopup") {
        chrome.action.openPopup();
    }
});
