import gmail_api as gmail
import ai_utils as ai
import json
import csv

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
    max_results = data.get('max_results', 15)

    return user_info, label_mapping, max_results

def write_to_csv(data, file_path='logs.csv'):
    # Write data to CSV file
    with open(file_path, mode='a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(data)

def clear_logs(file_path='logs.csv'):
    # Clear contents of CSV file
    with open(file_path, mode='w', newline='') as csv_file:
        pass


if __name__ == "__main__":
    service = gmail.get_gmail_service()

    user_info, label_mapping, max_results = extract_user_info()
    messages = gmail.fetch_emails(service, max_results)

    clear_logs()
    for index, message_id in enumerate(messages):
        print(f"{index+1}. Message ID - {message_id}")

        try:
            response = gmail.fetch_email_content(service, message_id)
            # print(f"Response: {response}\n")
            mail_subject = response['subject']
            print(f"Email subject - {mail_subject}\n")
            mail_body = response['body']
            # print(f"Email content - {mail_body}\n")
        except Exception as e:
            print(f"Error fetching email content: {e}\n")
            data_to_write = ('FAILED', message_id, '-', f"Error fetching email content: {e}")
            write_to_csv(data_to_write)
            continue

        try:
            label, reason = ai.mail_processor(user_info, label_mapping, mail_body, llm_online=True, api_key=api_key)
            print(f"label - {label}")
            print(f"reason - {reason}\n")
        except Exception as e:
            print(f"Error processing email: {e}\n")
            data_to_write = ('FAILED', mail_subject, '-', f"Error processing email: {e}")
            write_to_csv(data_to_write)
            continue

        try:
            gmail.add_label(service, message_id, label)
        except KeyError as e:
            gmail.create_label(service, label)
            gmail.add_label(service, message_id, label)

        # Write to CSV
        data_to_write = ('SUCCESS', mail_subject, label, reason)
        write_to_csv(data_to_write)