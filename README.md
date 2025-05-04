**Detection-Ai-Generated-Phishing**
📦 **Backend Architecture Overview** (XGBoost-Powered)

```
project/
├─ app/  
│   ├─ __init__.py  
│   ├─ config.py          ← Developer toggle and model paths  
│   ├─ main.py            ← FastAPI server exposes /predict-email  
│   ├─ models/            ← Inference artifacts  
│   │    • xgboost_phishing_model.json  
│   │    • xgboost_ai_generated_model.json  
│   │    • tfidf_vectorizer.pkl  
│   └─ utils/             ← Preprocessing and prediction logic  
│        • preprocess.py  ← Loads the TF-IDF vectorizer, prepares features  
│        • predict.py     ← Loads the two XGBoost boosters, applies thresholds  
│  
├─ gmail/  
│   ├─ __init__.py  
│   ├─ gmail_auth.py      ← OAuth2 flow for Gmail API with read/modify/labels scopes  
│   ├─ label_utils.py     ← Helpers to create or fetch Gmail labels  
│   └─ fetch_emails.py    ← Retrieves unread messages, calls backend, applies labels  
│  
├─ requirements.txt        ← Listing of all Python dependencies  
└─ README.md               ← Setup instructions and usage guide  
```

**Component Descriptions **

1. **app/config.py**
   Contains a simple flag (`SHOW_AI_GENERATED`) and file paths for models and the TF-IDF vectorizer.

2. **app/main.py**
   Launches a FastAPI app with a single POST endpoint (`/predict-email`). It accepts a JSON payload of subject, body, and metadata, then returns classification results.

3. **app/utils/preprocess.py**
   Loads the saved TF-IDF vectorizer, combines incoming subject and body text, and transforms them into the numerical feature vector required by both XGBoost models.

4. **app/utils/predict.py**
   Instantiates and loads the two XGBoost booster models, runs predictions for phishing and (optionally) AI-generation, applies configured decision thresholds, and returns a JSON object with boolean flags plus a body preview.

5. **gmail/gmail\_auth.py**
   Manages Google’s OAuth2 login sequence with the necessary Gmail scopes (read, modify, labels). Credentials are cached locally in `token.pickle`.

6. **gmail/label\_utils.py**
   Offers functions to check for existing Gmail labels (e.g., “🚨 Phishing” and “🤖 AI-Generated”) or to create them if missing.

7. **gmail/fetch\_emails.py**
   Pulls unread messages from your inbox, extracts the subject and plain-text body, sends that data to the FastAPI backend, and then—based on the returned flags—applies the appropriate Gmail labels. The user sees only “🚨 Phishing” by default; if developer mode is enabled, “🤖 AI-Generated” labels also appear.

8. **requirements.txt**
   Lists all required packages—FastAPI, Uvicorn, scikit-learn, XGBoost, joblib, and Google Auth libraries—so you can recreate the environment with a single `pip install -r requirements.txt`.

9. **README.md**
   Walks through initial setup (installing dependencies, placing `credentials.json`, performing the OAuth flow), starting the FastAPI service, and running the email fetch-and-label script.


