
# 🩺 Smart Health Analyzer

A simple, AI-powered web application designed to provide informational health advice based on user-described symptoms. The app features a clean user interface, a dark/light theme, and the ability to export the analysis as a PDF report.

## \#\# Description

The Smart Health Analyzer allows users to input their health concerns in a simple text box. The backend, powered by Python, Flask, and the Google Gemini API, analyzes the input and generates a structured response. This response includes a summary of identified symptoms, potential considerations, and recommended actions. The entire application is built to be straightforward and user-friendly.

**Note:** This application is for informational purposes only and is **not a substitute for professional medical advice, diagnosis, or treatment**.

-----

## \#\# Key Features

  * **🤖 AI-Powered Analysis:** Leverages a Large Language Model (LLM) to understand natural language and provide structured health information.
  * **🌗 Dark/Light Theme:** Comes with a sleek dark theme by default and allows users to toggle to a light theme. The preference is saved in the browser.
  * **📄 PDF Report Export:** Users can download a neatly formatted PDF of their analysis results for their records or to share with a healthcare provider.
  * **🌐 Simple Web Interface:** A clean, single-page application that is easy for anyone to use without instructions.

-----

## \#\# Technology Stack

  * **Backend:** Python 3, Flask
  * **AI:** Google Gemini API (`google-generativeai`)
  * **PDF Generation:** `reportlab`
  * **Frontend:** HTML, CSS, JavaScript
  * **Dependencies:** `python-dotenv` for environment variables

-----

## \#\# Setup and Installation

Follow these steps to get the project running on your local machine.

### \#\#\# 1. Prerequisites

  * Python 3.8 or newer
  * Git (for cloning the repository)

### \#\#\# 2. Clone the Repository

Open your terminal and clone the project:

```bash
git clone <your-repository-url>
cd smart-health-analyzer
```

### \#\#\# 3. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

  * **On Windows:**
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```
  * **On macOS / Linux:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

### \#\#\# 4. Install Dependencies

Install all the required Python libraries:

```bash
pip install Flask google-generativeai python-dotenv reportlab
```

### \#\#\# 5. Set Up Environment Variables

You need a Google Gemini API key for the AI to work.

1.  Create a file named `.env` in the root of the project directory.
2.  Add your API key to this file:
    ```
    API_KEY="YOUR_GEMINI_API_KEY_HERE"
    ```
    Replace `"YOUR_GEMINI_API_KEY_HERE"` with your actual key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### \#\#\# 6. Place the PDF Font

For the PDF export to work correctly, you need to add the `DejaVuSans.ttf` font file.

1.  Ensure you have a `static/fonts` directory.
2.  Download the `DejaVuSans.ttf` font and place it inside this directory.

### \#\#\# 7. Run the Application

Start the Flask server with this command:

```bash
python app.py
```

Open your web browser and navigate to `http://127.0.0.1:5000`. The application should now be running.

-----

## \#\# How to Use

1.  **Open the Web Page:** The application will load with the dark theme enabled.
2.  **Describe Symptoms:** Type your health concerns into the large text area.
3.  **Analyze:** Click the "Analyze My Symptoms" button.
4.  **View Results:** The AI-generated analysis will appear below the button.
5.  **Toggle Theme:** Click the ☀️/🌙 icon in the top-right corner to switch between dark and light modes.
6.  **Export PDF:** Once results are visible, click the "Export to PDF" button to download your report.

-----

## \#\# Future Enhancements

  * **Analysis History:** Implement a feature to store past results in the browser's `localStorage` for users to revisit.
  * **Guided Questionnaire:** Add an alternative input method using a step-by-step questionnaire to gather more structured data.

-----

## \#\# ⚠️ Disclaimer

This tool does not provide medical advice. It is intended for informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Never ignore professional medical advice in seeking treatment because of something you have read on this application. **If you think you may have a medical emergency, immediately call your doctor or your local emergency number.**