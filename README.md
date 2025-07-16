# Simple Malaria Analysis App

A minimal Streamlit app for analyzing microscopy images using Google's Gemini 2.0 Flash AI.

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure API Key:**
```bash
# Copy the example secrets file
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Edit .streamlit/secrets.toml and add your Google API key
# Get your API key from: https://aistudio.google.com/app/apikey
```

3. **Run the app:**
```bash
streamlit run app_simple.py
```

## Usage

1. Open the app in your browser
2. Upload a microscopy image (PNG, JPG, JPEG)
3. Click "Analyze" to get AI-powered malaria analysis
4. View structured results with species identification and morphological details

## Files

- `app_simple.py` - Main Streamlit application
- `.streamlit/secrets.toml` - Your API key (never commit this)
- `.streamlit/secrets.toml.example` - Template for API key setup
- `requirements.txt` - Python dependencies
- `.gitignore` - Protects secrets from version control # malaria-classifier
