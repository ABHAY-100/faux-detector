document.getElementById('onButton').addEventListener('click', () => {
    chrome.runtime.sendMessage({ action: 'activate' });
});

document.getElementById('offButton').addEventListener('click', () => {
    chrome.runtime.sendMessage({ action: 'deactivate' });
});
