import joblib

# Load TF-IDF vectorizer
vectorizer = joblib.load("App/Models/tfidf_vectorizer.pkl")

def preprocess_text(subject, body, structured_features):
    subject_body = subject + " " + body
    tfidf_vector = vectorizer.transform([subject_body])
    return tfidf_vector, structured_features
