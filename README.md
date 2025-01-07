# 🔍 Faux Detector

## What is Faux Detector?

Faux Detector is your friendly Chrome extension that helps you spot fake images and videos while browsing the web. Think of it as your personal digital detective, working in real-time to help you identify what's real and what's not. In a world where deepfakes are becoming increasingly sophisticated, we're here to help you browse the internet with confidence! 

## 🎯 Why We Built This

We're living in an age where seeing isn't always believing. Deepfakes and manipulated media can:
- Spread false information
- Impersonate people
- Create confusion
- Enable various types of scams

That's where Faux Detector comes in! We've created a simple tool that sits right in your browser, ready to analyze any suspicious content you come across. No technical expertise required - just point, click, and know!

## ✨ What Can It Do?

### Image Analysis
- Instant detection of manipulated images
- Works on any website you visit
- Simple one-click analysis
- Clear results showing if an image has been altered

### Video Analysis
- Real-time detection of deepfake videos
- Frame-by-frame analysis for accuracy
- Works with most common video formats
- Quick results to help you make informed decisions

### Cool Features
- 🚀 Real-time detection - no waiting around
- 🧠 Smart AI that keeps learning about new deepfake techniques
- 🎨 Super simple interface - just click and go!
- 📊 Clear results that anyone can understand

## 🛠️ Built With

![Tech Stack](https://skillicons.dev/icons?i=html,css,js,flask,tensorflow,opencv)

## 🚀 Getting Started

### Before You Begin

Make sure you have:
- Python 3.10 (we've tested it thoroughly with this version)
- The latest version of pip
- Ngrok (for sharing your local server with the world)

### Step-by-Step Setup

#### Setting Up the Backend

1. **Get the Code**
   ```bash
   git clone https://github.com/ABHAY-100/faux-detector.git
   cd faux-detector/backend
   ```

2. **Grab the Model File**
   - Download our trained model from [Dropbox](https://www.dropbox.com/scl/fi/0zh88gmiw79j6wozdzhxe/cnn_model.h5?rlkey=oh0g202fnkssq0r1imlz0u4s3&st=aahgdn49&dl=0)
   - Pop it into your `backend` folder

3. **Create Your Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Mac/Linux
   source venv/bin/activate
   ```

4. **Install the Good Stuff**
   ```bash
   pip install -r requirements.txt
   ```

5. **Fire It Up**
   ```bash
   python app.py
   ```
   Your backend will be hanging out on port 8000!

#### Setting Up Ngrok

1. Grab Ngrok from [their website](https://ngrok.com/download) if you haven't already

2. **Share Your Backend**
   ```bash
   ngrok http 8000
   ```
   You'll get a fancy HTTPS URL like `https://something.ngrok-free.app`

#### Adding the Chrome Extension

1. **Update Your Settings**
   - Open `manifest.json`
   - Add your Ngrok URL:
     ```json
     "host_permissions": [
       "https://<your-ngrok-url>.ngrok-free.app/*"
     ]
     ```

2. **Update the Code**
   - Find `content.js`
   - Update the API URL:
     ```javascript
     const response = await fetch('https://<your-ngrok-url>.ngrok-free.app/classify', {
       method: 'POST',
       body: formData,
     });
     ```

3. **Install in Chrome**
   - Go to `chrome://extensions/`
   - Turn on Developer mode
   - Click "Load unpacked"
   - Pick your extension folder

And you're ready to go! Look for the "Detect Deepfake" button on images and videos while browsing. 

## 👥 The Amazing Team Behind This

1. [Abhay Balakrishnan](https://github.com/ABHAY-100)
2. [Aadithya Madhav](https://github.com/aadithyayy)
3. [Asil Mehaboob](https://github.com/AsilMehaboob)
4. [Sreyas B Anand](https://github.com/sreyas-b-anand)

## 📜 License

This project is protected under the MIT License. Check out the [LICENSE](LICENSE) file for all the legal details.

## 🤝 Want to Help?

While we're not accepting contributions right now, we'd love to hear your thoughts! Feel free to:
- Try out Faux Detector
- Let us know what you think
- Report any bugs you find
- Star our repository if you like what we're doing!

## 🎉 Thank You!

Thanks for checking out Faux Detector! Together, we can make the internet a more trustworthy place. If you have any questions or run into issues, don't hesitate to reach out!

**Stay real, stay safe! 🌟**
