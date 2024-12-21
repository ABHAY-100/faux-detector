// popup.js
document.addEventListener('DOMContentLoaded', function() {
    const score = document.getElementById('score');
    const output = document.getElementById('output');
    
    // Set initial/default values
    
    //Instead of listening for a message, send a message to get the result.
    chrome.runtime.sendMessage({action: "getResult"}, (response) => {
        if (response) {
            score.textContent = response.best_prediction;
            output.textContent = response.classification;
            
            const body = document.querySelector('body');
            if (response.classification.includes('Fake')) {
                body.style.backgroundImage = "url('bg_false.png')";
            } else {
                body.style.backgroundImage = "url('bg_true.png')";
            }
        }
    });
    
    //Remove the message listener as it's no longer needed.
    // chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    //     console.log("Received message:", message); // Debug log
        
    //     if (message.action === "updateResult") {
    //         // Update the text content of the elements
    //         score.textContent = message.data.best_prediction;
    //         output.textContent = message.data.classification;
            
    //         // Update background based on the classification
    //         const body = document.querySelector('body');
    //         if (message.data.classification.includes('fake')) {
    //             body.style.backgroundImage = "url('bg_false.png')";
    //         } else {
    //             body.style.backgroundImage = "url('bg_true.png')";
    //         }
    //     }
    // });
});

