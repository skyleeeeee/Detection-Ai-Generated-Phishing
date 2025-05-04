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
   SHOW_AI_GENERATED = True/False
   Paths to models & vectorizer under app/models/

3. **app/main.py**
   Loads tfidf_vectorizer.pkl via joblib
   preprocess_input(data)
      * Combines subject + body
      * Returns TF-IDF vector for both phishing & AI models
4. **app/utils/preprocess.py**
   Loads the saved TF-IDF vectorizer, combines incoming subject and body text, and transforms them into the numerical feature vector required by both XGBoost models.

5. **app/utils/predict.py**
   Handles Google OAuth2 with scopes
      gmail.readonly, gmail.modify, gmail.labels
   Persists credentials in token.pickle

6. **gmail/gmail\_auth.py**
   get_or_create_label(service, label_name)
   Creates custom labels (🚨 Phishing, 🤖 AI-Generated)

7. **gmail/fetch_emails.py**
   Connects via get_gmail_service()
   Queries is:unread inbox messages
   Extracts subject/body, posts to FastAPI
   Reads back {"phishing":…, "ai_generated":…}
   Applies only 🚨 Phishing when phishing=True
8. **gmail/label\_utils.py**
   Offers functions to check for existing Gmail labels (e.g., “🚨 Phishing” and “🤖 AI-Generated”) or to create them if missing.

9. **gmail/fetch\_emails.py**
   Pulls unread messages from your inbox, extracts the subject and plain-text body, sends that data to the FastAPI backend, and then—based on the returned flags—applies the appropriate Gmail labels. The user sees only “🚨 Phishing” by default; if developer mode is enabled, “🤖 AI-Generated” labels also appear.

10. **requirements.txt**
   Lists all required packages—FastAPI, Uvicorn, scikit-learn, XGBoost, joblib, and Google Auth libraries—so you can recreate the environment with a single `pip install -r requirements.txt`.

11. **README.md**
   Walks through initial setup (installing dependencies, placing `credentials.json`, performing the OAuth flow), starting the FastAPI service, and running the email fetch-and-label script.


