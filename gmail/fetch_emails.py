import requests
import base64
from gmail_auth import get_gmail_service
from label_utils import get_or_create_label
from config import SHOW_AI_GENERATED

BACKEND_URL = "http://localhost:8000/predict-email"

def fetch_and_classify():
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])

    for msg in messages:
        msg_id = msg['id']
        msg_data = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        payload = msg_data.get("payload", {})
        headers = payload.get("headers", [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
        
        # Extract plain text body
        body = ""
        parts = payload.get("parts", [])
        for part in parts:
            if part.get("mimeType") == "text/plain":
                data = part["body"].get("data")
                if data:
                    body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                    break

        email_payload = {
            "subject": subject,
            "body": body,
            "metadata": {
                "structured": [0.0] * 17  # Placeholder metadata
            }
        }

        response = requests.post(BACKEND_URL, json=email_payload)
        result = response.json()  # ✅ Make sure this is inside the loop

        # Apply labels based on prediction
        if result['phishing']:
            label_id = get_or_create_label(service, '🚨 Phishing')
            service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={"addLabelIds": [label_id]}
            ).execute()
            print(f"✅ Applied '🚨 Phishing' to: {subject}")

        elif SHOW_AI_GENERATED and result['ai_generated']:
            label_id = get_or_create_label(service, '🤖 AI-Generated')
            service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={"addLabelIds": [label_id]}
            ).execute()
            print(f"🤖 Marked AI-Generated (Developer Mode): {subject}")

if __name__ == "__main__":
    fetch_and_classify()
