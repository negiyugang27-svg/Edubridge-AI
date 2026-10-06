# Edubridge AI

A Flask app for education and career guidance, including account registration, skill-gap analysis, a quiz, and an AI tutor.

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Start the app:

   ```powershell
   python app.py
   ```

   Open `http://127.0.0.1:5000` in your browser.

The app creates its SQLite database locally as `edutech.db`. Database files are excluded from Git so account data is not published.

For a stable session key, set the `FLASK_SECRET_KEY` environment variable before starting the app. If it is not set, a random key is generated each time the app starts.
