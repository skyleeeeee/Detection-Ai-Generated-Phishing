from xgboost import Booster, DMatrix
from app.utils.preprocess import preprocess_text

# Load XGBoost models
xgb_phishing = Booster()
xgb_phishing.load_model("App/Models/xgboost_phishing_model.json")

xgb_ai = Booster()
xgb_ai.load_model("App/Models/xgboost_ai_generated_model.json")

def predict_email(email_data):
    subject = email_data.get("subject", "")
    body = email_data.get("body", "")
    metadata = email_data.get("metadata", {})

    # Structured features must match training pipeline order
    structured = metadata.get("structured", [0.0]*17)  # Placeholder

    tfidf_vector, _ = preprocess_text(subject, body, structured)
    xgb_input = DMatrix(tfidf_vector)

    phishing_pred = bool(xgb_phishing.predict(xgb_input)[0] > 0.5)
    ai_generated_pred = bool(xgb_ai.predict(xgb_input)[0] > 0.5)

    return {
        "phishing": phishing_pred,
        "ai_generated": ai_generated_pred,
        "email": body[:250] + ("..." if len(body) > 250 else "")
    }
```
