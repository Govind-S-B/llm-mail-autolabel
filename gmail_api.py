import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import base64
from bs4 import BeautifulSoup

# Set Edge as default browser
# import webbrowser
# url = "https://www.google.com"
# edge_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
# webbrowser.register("edge", None, webbrowser.BackgroundBrowser(edge_path))

# Set up the Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def get_body(parts):
    data = ""
    if 'parts' in parts:
        for part in parts['parts']:
            # if 'data' in part['body']:
            #     data += part['body']['data']
            data += get_body(part)

        return data
    else:
        return parts['body']['data']


def get_gmail_service():
    # Check if token file exists
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    # If credentials are not valid or missing, run the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the Gmail API service
    service = build('gmail', 'v1', credentials=creds)
    return service


# Function to list labels with their IDs
def list_labels(service):
    """
    Retrieves the list of user defined labels from a Gmail account.

    Args:
        service (object): The Gmail service object.

    Returns:
        dict: A dictionary containing the labels as keys and their respective IDs as values.
    """
    results = service.users().labels().list(userId='me').execute()
    label_dict = results.get('labels', [])

    # Default labels to exclude
    default_lables = [
        'CHAT',
        'SENT',
        'INBOX',
        'IMPORTANT',
        'TRASH',
        'DRAFT',
        'SPAM',
        'CATEGORY_FORUMS',
        'CATEGORY_UPDATES',
        'CATEGORY_PERSONAL',
        'CATEGORY_PROMOTIONS',
        'CATEGORY_SOCIAL',
        'STARRED',
        'UNREAD'
    ]

    labels = {}
    if not label_dict:
        print('No labels found.')
    else:
        for label in label_dict:
            if label['name'] not in default_lables:
                labels[label['name']] = label['id']
    return labels


# Fetch emails
def fetch_emails(service, max_results=10):
    """
    Fetches a specified number of emails using the given service.

    Parameters:
        service (obj): The service object used to fetch emails.
        max_results (int, optional): The maximum number of emails to fetch. Defaults to 10.

    Returns:
        list: A list of dictionaries representing the fetched emails.
    """

    results = service.users().messages().list(
        userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])
    message_ids = [message['id'] for message in messages]
    return message_ids


def fetch_email_content(service, message_id):
    """
    Fetches the content of a specific email message.

    Parameters:
        service (obj): The service object used to fetch the email content.
        message_id (str): The ID of the message to fetch the content for.

    Returns:
        dict: A dictionary containing the email content (subject, sender, body).
    """

    message = service.users().messages().get(userId='me', id=message_id).execute()
    # Get value of 'payload' from dictionary 'message'
    payload = message['payload']
    headers = payload['headers']
    # print(headers)
    # print(payload)

    # Look for Subject and Sender Email in the headers
    for d in headers:
        if d['name'] == 'Subject':
            subject = d['value']
        if d['name'] == 'From':
            sender = d['value']

    # The Body of the message is in Encrypted format. So, we have to decode it.
    # Get the data and decode it with base 64 decoder.
    data = get_body(payload.get('parts')[0])

    # data = ""
    # if 'parts' in parts:
    #     for part in parts['parts']:
    #         if 'data' in part['body']:
    #             data += part['body']['data']
    # else:
    #     data = parts['body']['data']

    # print(data)
    data = data.replace("-", "+").replace("_", "/")
    decoded_data = base64.b64decode(data)

    # Now, the data obtained is in lxml. So, we will parse it with BeautifulSoup library
    soup = BeautifulSoup(decoded_data, "lxml")
    body = soup.body()

    response = {
        "sender": sender,
        "subject": subject,
        "body": body
    }
    return response


def add_label(service, message_id, label):
    """
    Adds the specified label to the given message.

    Parameters:
        service (obj): The service object used to add the label.
        # labels (dict): The dictionary of available label names and their corresponding IDs.
        message_id (str): The ID of the message to add the label to.
        label (str): The name of the label to add.
    """

    labels = list_labels(service)
    label_id_to_apply = labels[label]

    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={'addLabelIds': [label_id_to_apply]}
    ).execute()
    print(f"Label '{label}' applied to the email successfully.\n")


def create_label(service, label_name):
    """
    Creates a new label with the specified name.

    Parameters:
        service (obj): The service object used to create the label.
        label_name (str): The name of the label to create.

    Returns:
        str: The ID of the created label.
    """

    created_label = service.users().labels().create(
        userId='me',
        body={'name': label_name}
    ).execute()

    label_id = created_label['id']
    print(f"Label '{label_name}' created with ID: {label_id}\n")
    return label_id


if __name__ == "__main__":
    # Get credentials and create Gmail API client
    service = get_gmail_service()

    # Fetch all the labels in the user's account
    labels = list_labels(service)
    if not labels:
        print("\nNo user defined labels found.")
    else:
        print("Label\t\t\tLabel ID")
        print('-'*40)
        for label, label_id in labels.items():
            print(f"{label}\t\t\t{label_id}")

    # Fetch and list the latest, specified number of emails
    max_results = input("\nEnter the number of emails to fetch: ")
    messages = fetch_emails(service, max_results=max_results)
    if not messages:
        print("\nNo emails found.")
    else:
        print(f"\n{'-'*15}Emails{'-'*15}")
        for message in messages:
            # Fetch and display the content of the first email
            print(f"Message ID - {message['id']}")
            try:
                message_content = fetch_email_content(service, message['id'])
                print(
                    f"From - {message_content['sender']} \nSubject - {message_content['subject']} \n")
            except Exception as e:
                print(f"Error fetching email content: {e}\n")

    while True:
        message_id = input("\nEnter the message ID to apply label: ")
        label = input("Enter the label to be added: ")
        # Add the specified label to the given message
        add_label(service, message_id, label)
