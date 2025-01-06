# Faux Detector

## Overview

Faux Detector is a Flask-based web application designed to combat the alarming threat posed by deepfakes. By providing real-time detection of manipulated media, Faux Detector empowers users to identify deepfakes as they browse. Utilizing advanced AI technology, it ensures the authenticity of digital content, fostering trust in an increasingly deceptive online environment.

<br />


## The Problem Faux Detector Solves

Deepfakes pose a significant threat to our digital lives. They can impersonate individuals, damaging reputations, leading to fraud, and causing emotional distress. These malicious fakes can be used for harassment, blackmail, or manipulation, with devastating consequences—including extreme cases like suicide.

Moreover, deepfakes can spread false narratives that influence public opinion and create widespread confusion. They can also facilitate financial scams or unauthorized access to sensitive systems by mimicking voices or faces. It is crucial to acknowledge these risks and take steps to mitigate the harm caused by deepfakes.

Faux Detector helps protect individuals and communities by providing real-time detection of deepfakes. By fostering trust in digital media, Faux creates a safer online environment.

<br />


## Features

- **Real-Time Detection**: Identify manipulated videos and images instantly.
- **AI-Powered Analysis**: Advanced algorithms that adapt to evolving deepfake technologies.
- **User-Friendly Interface**: Simple and intuitive design for seamless user experience.

<br />


## 🔧 How to Set It Up 

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

3. **Set Up a Virtual Environment**:

    ```bash
    python -m venv venv

    venv\Scripts\activate  # For Windows
    source venv/bin/activate  # For Linux/Mac
    ```

4. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Run the Flask Application**:

    ```bash
    python app.py
    ```

*Note: Now your Flask backend will now be running on port `8000`.*

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


## 👥 Collaborators

<a href="https://github.com/AsilMehaboob/SpaceGame/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=AsilMehaboob/SpaceGame" />
</a>

<br />


**Thank you for your interest in Faux! 🤝**
