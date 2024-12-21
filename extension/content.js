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
    
    // Style the button with 50% transparency
    Object.assign(button.style, {
        position: 'absolute',
        zIndex: '1000',
        backgroundColor: 'rgba(255, 0, 0, 1)', // 50% transparent red
        opacity : 0.2,
        color: 'white',
        border: 'none',
        padding: '5px 10px',
        cursor: 'pointer',
        borderRadius: '4px',
        fontSize: '12px',
        fontWeight: 'bold',
        boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
        transition: 'all 0.3s ease' // Smooth transition for hover effect
    });

    // Add hover effect
    button.addEventListener('mouseenter', () => {
        button.style.opacity = 1; // Fully opaque on hover
    });

    button.addEventListener('mouseleave', () => {
        button.style.backgroundColor = 'rgba(255, 0, 0, 0.5)'; // Back to 50% transparent
    });

    const updateButtonPosition = () => {
        const rect = image.getBoundingClientRect();
        button.style.top = `${rect.top + window.scrollY + 10}px`;
        button.style.left = `${rect.left + window.scrollX + 10}px`;
    };

    button.addEventListener('click', (e) => {
        e.stopPropagation();
        console.log('Detecting deepfake for:', image.src);
        // Add your deepfake detection logic here
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