// Add DM Sans font import to the document head
const fontLink = document.createElement('link');
fontLink.href = 'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap';
fontLink.rel = 'stylesheet';
document.head.appendChild(fontLink);

// Main function to find images and add detection buttons
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
    
    // Style the button with DM Sans
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
        fontFamily: '"DM Sans", sans-serif', // Updated to DM Sans
        //boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
        transition: 'all 0.3s ease',
        opacity: '0.1',
        border : 'solid 1px grey'
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
            // Convert the image URL to a File (Blob)
            console.log("in try catch");
            const imageBlob = await fetch(image.src).then((res) => res.blob());
            const imageFile = new File([imageBlob], 'image.png', { type: 'image/png' }); // Adjust to desired format
    
            // Create a FormData object
            const formData = new FormData();
            formData.append('image', imageFile);
            formData.append('metadata', JSON.stringify({
                width: image.naturalWidth,
                height: image.naturalHeight,
            }));
    
            // Send POST request with image file and metadata
            const response = await fetch('https://snvdv9b8-8000.inc1.devtunnels.ms/classify', {
                method: 'POST',
                body: formData,
            });
    
            const result = await response.json();
            console.log("here" ,result)
            if (response.ok) {
                console.log('Checking ');
            }
        } catch (error) {
            console.error('Error making POST request:', error);
            button.innerText = 'Error';
            button.style.backgroundColor = 'grey';
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