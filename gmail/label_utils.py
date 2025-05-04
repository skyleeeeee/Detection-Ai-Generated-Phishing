from googleapiclient.errors import HttpError

def get_or_create_label(service, label_name):
    try:
        labels = service.users().labels().list(userId='me').execute().get('labels', [])
        for label in labels:
            if label['name'] == label_name:
                return label['id']

        label_obj = {
            "name": label_name,
            "labelListVisibility": "labelShow",
            "messageListVisibility": "show"
        }
        label = service.users().labels().create(userId='me', body=label_obj).execute()
        return label['id']
    except HttpError as error:
        print(f"An error occurred while creating label: {error}")
        return None
