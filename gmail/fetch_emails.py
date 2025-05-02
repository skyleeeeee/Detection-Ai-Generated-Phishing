import requests
from gmail.gmail_auth import get_gmail_service

BACKEND_URL = "http://localhost:8000/predict-email"

# Connect to Gmail and fetch unread messages
def fetch_and_classify():
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = msg_data.get("payload", {})
        headers = payload.get("headers", [])

        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
        parts = payload.get("parts", [])
        body = ""

        for part in parts:
            if part.get("mimeType") == "text/plain":
                data = part["body"].get("data")
                if data:
                    import base64
                    body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                    break

        email_payload = {
            "subject": subject,
            "body": body,
            "metadata": {
                "structured": [0.0] * 17  # Placeholder values
            }
        }

        response = requests.post(BACKEND_URL, json=email_payload)
        result = response.json()

        print("----------------------")
        print(f"📨 Subject: {subject}")
        print(f"🔍 Phishing: {result['phishing']}")
        print(f"🤖 AI-Generated: {result['ai_generated']}")
        print("----------------------\n")

if __name__ == "__main__":
    fetch_and_classify()
