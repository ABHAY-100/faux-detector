let latestResult = null;

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "updateResult") {
    latestResult = message.data;
    chrome.action.openPopup();
  } else if (message.action === "getResult") {
    sendResponse(latestResult);
    latestResult = null;
  } else if (message.action === "openPopup") {
    chrome.action.openPopup();
  }
});
