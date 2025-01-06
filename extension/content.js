const fontLink = document.createElement('link');
fontLink.href = 'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap';
fontLink.rel = 'stylesheet';
document.head.appendChild(fontLink);

function findImagesAndAddButtons() {
    const images = document.querySelectorAll('img');

    images.forEach(image => {
        if (image.dataset.detectButtonAdded) {
            return;
        }

        const checkImageAndAddButton = () => {
            const width = image.offsetWidth || image.naturalWidth;
            const height = image.offsetHeight || image.naturalHeight;

            if (width > 80 && height > 80) {
                addDetectButton(image);
                image.dataset.detectButtonAdded = true;
            }
        };

        if (image.complete) {
            checkImageAndAddButton();
        } else {
            image.addEventListener('load', checkImageAndAddButton);
        }
    });
}


function addDetectButton(image) {
    const button = document.createElement('button');
    button.innerText = 'Detect Deepfake';
    button.id = 'detect-button'

    Object.assign(button.style, {
        position: 'absolute',
        zIndex: '1000',
        backgroundColor: 'rgb(22, 24, 28)',
        color: 'white',
        border: 'none',
        padding: '8px 16px',
        cursor: 'pointer',
        borderRadius: '16px',
        fontSize: '14px',
        fontWeight: '500',
        fontFamily: '"DM Sans", sans-serif',
        transition: 'all 0.3s ease',
        opacity: '0.1',
        border: 'solid 1px grey'
    });

    button.addEventListener('mouseenter', () => {
        button.style.opacity = '1';
    });

    button.addEventListener('mouseleave', () => {
        button.style.opacity = '0.1';
    });

    const updateButtonPosition = () => {
        const rect = image.getBoundingClientRect();
        button.style.top = `${rect.top + window.scrollY + 10}px`;
        button.style.left = `${rect.left + window.scrollX + 10}px`;
    };

    button.addEventListener('click', async (e) => {
        e.stopPropagation();
        console.log('Detecting deepfake for:', image.src);
    
        try {
            // Fetch the image URL as a Blob
            const imageBlob = await fetch(image.src).then((res) => {
                if (!res.ok) {
                    throw new Error(`Failed to fetch image: ${res.statusText}`);
                }
                return res.blob();
            });
    
            // Convert the Blob to a File
            const imageFile = new File([imageBlob], 'image.png', { type: 'image/png' });
    
            // Create FormData and append the file
            const formData = new FormData();
            formData.append('mediaFile', imageFile); // Use 'mediaFile' here
            formData.append('metadata', JSON.stringify({
                width: image.naturalWidth,
                height: image.naturalHeight,
            }));
    
            // Send the POST request to the server
            const response = await fetch('https://4b25-49-37-227-89.ngrok-free.app/classify', {
                method: 'POST',
                body: formData,
            });
    
            const result = await response.json();
            if (!result) {
                throw new Error("Can't detect");
            }
    
            function formatFloat(value, decimalPlaces = 6) {
                return parseFloat(value.toFixed(decimalPlaces));
            }
            
            const prediction = formatFloat(parseFloat(result.best_prediction));
            
            chrome.runtime.sendMessage({
                action: "updateResult",
                data: {
                    best_prediction: prediction,
                    classification: result.classification
                }
            });
    
            if (response.ok) {
                console.log('Detection result:', result);
            } else {
                throw new Error(result.message || 'Detection failed');
            }
        } catch (error) {
            console.error('Error making POST request:', error);
        }
    });
    


    window.addEventListener('scroll', updateButtonPosition);
    window.addEventListener('resize', updateButtonPosition);

    updateButtonPosition();
    document.body.appendChild(button);

}

const observer = new MutationObserver((mutations) => {
    mutations.forEach(mutation => {
        if (mutation.addedNodes.length) {
            findImagesAndAddButtons();
        }
    });
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});

findImagesAndAddButtons();
setInterval(findImagesAndAddButtons, 2000);
