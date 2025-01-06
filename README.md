# Faux Detector

## Overview

Faux Detector is a user-friendly Chrome Extension designed to address the increasing threat of deepfakes and manipulated images online. By providing real-time detection capabilities, Faux Detector empowers users to verify the authenticity of images while browsing the web. Utilizing advanced AI technology, it makes navigating the digital landscape safer and more trustworthy, ensuring that users can make informed decisions about the content they encounter.

<br />


## The Problem we Solve

Deepfakes present a significant challenge in our digital lives, as they can impersonate individuals and spread misinformation. These manipulated images can damage reputations, facilitate scams, and create confusion in public discourse. Faux Detector tackles these issues by equipping users with the tools needed to identify manipulated content quickly and easily. By empowering individuals to spot fakes, Faux Detector helps foster a safer online environment where trust in digital media can be restored.

<br />


## Features

- **Real-Time Detection**: Identify manipulated videos and images instantly.
- **AI-Powered Analysis**: Advanced algorithms that adapt to evolving deepfake technologies.
- **User-Friendly Interface**: Simple and intuitive design for seamless user experience.

<br />


## Built With

![Tech Stack](https://skillicons.dev/icons?i=html,css,js,flask,tensorflow,opencv)

<br />

## How to Set It Up 

### Prerequisites

Ensure you have the following installed:
- Python (use v3.10, idk abt other versions)
- pip (try updating to the latest)
- Ngrok (we use it for exposing your local server to the internet)

### Installation

#### Backend Setup

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/ABHAY-100/faux-detector.git
    ```

2. **Navigate to the Backend Directory**:

    ```bash
    cd faux-detector/backend
    ```

3. **Download the `.h5` file from [Dropbox](https://www.dropbox.com/scl/fi/0zh88gmiw79j6wozdzhxe/cnn_model.h5?rlkey=oh0g202fnkssq0r1imlz0u4s3&st=aahgdn49&dl=0) and put it in `backend folder`**:

4. **Set Up a Virtual Environment**:

    ```bash
    python -m venv venv

    venv\Scripts\activate  # For Windows
    source venv/bin/activate  # For Linux/Mac
    ```

5. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

6. **Run the Flask Application**:

    ```bash
    python app.py
    ```

    *Note: Now your Flask backend will now be running on port `8000`*

#### Expose Your Backend with Ngrok

1. **Install Ngrok**:

    If you haven't already installed Ngrok, download it from [Ngrok's official website](https://ngrok.com/download) and set it up.

2. **Start Ngrok**:

    Open a new command prompt or terminal window and run the following command:

      ```bash
      ngrok http 8000
      ```

3. **Get Your Ngrok HTTPS URL**:

    After running the command, Ngrok will provide you with a public HTTPS URL that looks something like this: `https://6eba-49-37-227-89.ngrok-free.app`


#### Chrome Extension Setup

1. **Prepare Your Extension Folder**:

    Ensure your Chrome extension files are ready in a folder containing `manifest.json`, JavaScript files, and any other necessary resources.

2. **Update `manifest.json`**:

    Open your `manifest.json` file and update the `host_permissions` to include your Ngrok URL:

      ```bash
      "host_permissions": [
        "https://<your-ngrok-subdomain>.ngrok-free.app/*"
      ]
      ```
    *Make sure to replace `<your-ngrok-subdomain>` with the actual subdomain provided by Ngrok when you start it.*

3. **Update `content.js`**:

    Modify your `content.js` file to point to your Ngrok URL for API requests:

    ```bash
    // Send the POST request to the server
    const response = await fetch('https://<your-ngrok-subdomain>.ngrok-free.app/classify', {
    method: 'POST',
    body: formData,
    });
    ```

4. **Open Chrome Extensions Page**:

    Open Google Chrome and navigate to `chrome://extensions/`.

5. **Enable Developer Mode**:

    In the top right corner of the extensions page, toggle the **Developer mode** switch to **ON**.

6. **Load Unpacked Extension**:

    - Click on the **Load unpacked** button.
    - Select the folder containing your extension files.

### Final Steps

Now ensure the extension is active; you will see a popup button over each image on your current website. Just click on the "Detect Deepfake" button, and you can see the results!

<br />


## Team Members

1. [Abhay Balakrishnan](https://github.com/ABHAY-100)
2. [Aadithya Madhav](https://github.com/aadithyayy)
3. [Asil Mehaboob](https://github.com/AsilMehaboob)
4. [Sreyas B Anand](https://github.com/sreyas-b-anand)

<br />

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<br />


## Contribution

At this time, we are not accepting external contributions. We appreciate your interest in Faux! Please feel free to use the project, provide feedback, and report any issues you encounter.


<br />


**Thank you for your interest in Faux! 🤝**
