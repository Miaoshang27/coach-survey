# Coach Survey

A Streamlit-based web app for collecting coach feedback, including image uploads and user-customized branding. This app uses Google Cloud services and Google sheets for storage.

## 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Authentication & Credentials](#-authentication--credentials)
- [Running the App](#-running-the-app)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📌 Project Overview 
This project provides a web interface where coaches (or users) can:
- Answer a series of questions to define their brand and coaching focus  
- Select the main goals and areas they support clients with 
- Share their preferred app layout, shape style, and visual tone
- Upload logos and visual assets (portrait, background, content images)  
- Submit all inputs to guide the design of a personalized coaching app

---

## 📁 Project Structure

<pre>
coach-survey/
├── .streamlit/
│ └── config.toml # UI theming and layout config
├── Dockerfile # Container setup for deployment
├── main.py # Main application entry point
├── requirements.txt # Python dependencies
└── README.md # Project documentation
</pre>
---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/coach-survey.git
cd coach-survey
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

✅ Recommended: Use a virtual environment like venv or conda.

## 🔐 Authentication & Credentials

This app integrates with Google services such as Google Sheets and Google Cloud Storage. Before using it, make sure you're authenticated to:
- **BigQuery dataset** (read/write)
- **Cloud Storage bucket** (read/write)
- **Google Sheets** (if used)

### Authenticate with Google

```bash
gcloud auth application-default login --scopes=https://www.googleapis.com/auth/spreadsheets,https://www.googleapis.com/auth/cloud-platform
```

This creates a file at ``` ~/.config/gcloud/application_default_credentials.json``` that allows the app to access your Google resources securely.

## ▶️ Running the App

### Run locally

```bash
streamlit run main.py
```
Once running:
- A web interface will open in your browser.
- Users can fill out the survey step-by-step.
- Uploaded assets will be stored in Cloud Buckets under folders named after the user ```bi-lenus-staging/coach_app_survey/user_uploads```.
- Survey responses will be logged to Google Sheets ```https://docs.google.com/spreadsheets/d/1vIn_wz9TwCiqzqAT3JV8E_84Ck_cHIiybvdDZgfcoug/edit?gid=0#gid=0```


## 🤝 Contributing

To get started:
1. Create your feature branch: ``` git checkout -b feature/YourFeatureName ```
2. Commit your changes: ``` git commit -m 'Add new feature' ```
3. Push to the branch: ``` git push origin feature/YourFeatureName ```
4. Submit a pull request



