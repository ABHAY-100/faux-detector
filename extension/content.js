// Function to create and display the Detect button
function addDetectButton(image) {
    const button = document.createElement('button');
    button.innerText = 'Detect Deepfake';
    button.style.position = 'absolute';
    button.style.top = '10px'; // Adjust as needed
    button.style.left = '10px'; // Adjust as needed
    button.style.zIndex = '1000'; // Ensure it's on top of other elements
    button.style.backgroundColor = 'red'; // Customize button style
    button.style.color = 'white';
    button.style.border = 'none';
    button.style.padding = '5px 10px';
    button.style.cursor = 'pointer';

    // Position the button relative to the image
    const rect = image.getBoundingClientRect();
    button.style.top = `${rect.top + window.scrollY}px`;
    button.style.left = `${rect.left + window.scrollX}px`;

    // Add click event listener to the button
    button.addEventListener('click', () => {
        console.log('Detecting deepfake...');
        // Logic for deepfake detection goes here
        chrome.runtime.sendMessage({ action: 'detect' });
    });

    document.body.appendChild(button);
}

// Function to find images and add buttons
function findImagesAndAddButtons() {
    const images = document.querySelectorAll('img');
    
    images.forEach(image => {
        // Check if the detect button already exists on this image
        if (!image.dataset.detectButtonAdded) {
            addDetectButton(image);
            image.dataset.detectButtonAdded = true; // Mark this image as processed
        }
    });
}

// Observe changes in the DOM to dynamically add buttons to newly loaded images
const observer = new MutationObserver(findImagesAndAddButtons);
observer.observe(document.body, { childList: true, subtree: true });

// Initial call to add buttons for existing images
findImagesAndAddButtons();
