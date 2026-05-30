# PDF to Audiobook Converter 🎧

A simple and elegant web application that converts your PDF documents into MP3 audiobooks using Python. Built with [Streamlit](https://streamlit.io/), `pypdf`, and `gTTS` (Google Text-to-Speech).

## Features
- **Easy Uploads:** Upload any PDF document directly from the web interface.
- **Fast Extraction:** Extracts text efficiently from your PDF pages.
- **Text-to-Speech:** Uses Google Text-to-Speech to generate high-quality audio.
- **Listen & Download:** Listen to the generated audiobook right in the browser or download it as an MP3 file.

## How to Run Locally

1. Clone this repository (or download the files).
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
4. Open the provided local URL in your web browser.

## How to Deploy via GitHub

Since GitHub Pages only supports static websites (HTML/CSS/JS) and this app relies on a Python backend, the easiest and most common way to deploy this for free is using **Streamlit Community Cloud**, which directly connects to your GitHub repository.

1. Create a new repository on your GitHub account.
2. Push these project files (`app.py`, `requirements.txt`, and this `README.md`) to your new GitHub repository.
3. Go to [Streamlit Community Cloud](https://streamlit.io/cloud) and sign in with your GitHub account.
4. Click on **New app**.
5. Select the repository, branch (usually `main`), and the main file path (`app.py`).
6. Click **Deploy!**

Your PDF to Audiobook converter will now be live on the web!
