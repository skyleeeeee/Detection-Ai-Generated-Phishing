# Detection-Ai-Generated-Phishing
# 📦 Backend Architecture Overview for Gmail-Integrated Phishing Detection

```
project/
├── app/                         # Core FastAPI application
│   ├── __init__.py
│   ├── main.py                  # FastAPI server + route for prediction
│   ├── models/                  # Saved models
│   │   ├── xgboost_phishing_model.json
│   │   ├── xgboost_ai_generated_model.json
│   │   └── tfidf_vectorizer.pkl
│   ├── utils/
│   │   ├── preprocess.py        # TF-IDF vectorizer logic
│   │   └── predict.py           # Prediction logic using both models
│   └── config.py                # Paths, constants, label mapping
│
├── gmail/                      # Gmail integration layer
│   ├── gmail_auth.py           # Handles OAuth2 login with Gmail API
│   └── fetch_emails.py         # Fetches unread emails and sends to FastAPI
│
│
├── requirements.txt            # Python dependencies
└── README.md                   # Setup instructions and architecture docs
```

# ✨ Component Descriptions

## 1. app/main.py
FastAPI app with one route: `/predict-email`
- Accepts JSON with `subject`, `body`, and `metadata`
- Calls prediction logic and returns result

## 2. app/utils/preprocess.py
- Loads `tfidf_vectorizer.pkl`
- Preprocesses input (subject + body) into TF-IDF vectors
- Returns vectorized input for XGBoost models

## 3. app/utils/predict.py
- Loads `xgboost_phishing_model.json` and `xgboost_ai_generated_model.json`
- Calls `predict_email()` function:
  - Combines subject + body → TF-IDF
  - Runs both phishing and AI-generated predictions
  - Returns boolean flags and body preview

## 4. gmail/gmail_auth.py
- Uses Google’s OAuth2 flow to authorize Gmail access
- Returns Gmail API service client

## 5. gmail/fetch_emails.py
- Connects to Gmail inbox
- Pulls unread emails
- Extracts subject + body
- Sends data to `http://localhost:8000/predict-email`
- Optionally prints flags or can label messages (next step)

## 6. requirements.txt
```
fastapi
uvicorn
scikit-learn
xgboost
joblib
google-auth
google-auth-oauthlib
google-api-python-client
```

## 7. Output Format (returned by /predict-email)
```json
{
  "phishing": true,
  "ai_generated": false,
  "email": "body preview here..."
}
```
