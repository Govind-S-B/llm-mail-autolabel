import gmail_api as gmail
import ai_utils as ai
import json

# Load API key from .env file
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("PALM_API_KEY")

def extract_user_info(json_file_path='user_info.json'):
    # Read data from JSON file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Extract information
    user_info = data.get('user_info', '')
    label_mapping = data.get('label_mapping', {})
    mail_body = data.get('mail_body', '')

    return user_info, label_mapping, mail_body

if __name__ == "__main__":
    service = gmail.get_gmail_service()

    user_info, label_mapping, mail_body = extract_user_info()

    max_results = int(input("Enter the number of emails to fetch: "))
    messages = gmail.fetch_emails(service, max_results)
    print(messages)

    # label, reason = ai.mail_processor(user_info, label_mapping, mail_body, llm_online=True, api_key=api_key)
    # print(label, reason)