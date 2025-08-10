import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
from config import GMAIL_TOKEN_PATH, GMAIL_CREDENTIALS_PATH
from logs import logger

def safe_ascii(text):
    return text.encode('ascii', errors='replace').decode('ascii')

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    if os.path.exists(GMAIL_TOKEN_PATH):
        with open(GMAIL_TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                GMAIL_CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(GMAIL_TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def get_today_emails(service):
    today = datetime.datetime.now().strftime('%Y/%m/%d')
    # query = f'after:{today}'

    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1, hours=2)).strftime('%Y/%m/%d')
    query = f'after:{yesterday}'

    # query = f'after:{today} label:inbox'
    print(f"[TRACE] Gmail query: {query}")
    logger.info("[TRACE] Gmail query: %s", query)
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    logger.info("[TRACE] Found %d messages for query: %s", len(messages), query)
    emails = []
    for msg in messages:
        logger.info("[TRACE] Fetching message ID: %s", msg['id'])
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        headers = msg_data['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        from_email = next((h['value'] for h in headers if h['name'] == 'From'), '')
        snippet = msg_data.get('snippet', '')
        logger.info("[TRACE] Email subject: %s, from: %s", safe_ascii(subject), safe_ascii(from_email))
        body = get_body(msg_data)
        # logger.info("[TRACE] Email body: %s...", safe_ascii(body[:100]))
        emails.append({
            'subject': subject,
            'from': from_email,
            'snippet': snippet,
            'body': body
        })
    logger.info("[TRACE] Returning %d emails", len(emails))
    return emails

def get_body(msg_data):
    try:
        parts = msg_data['payload'].get('parts', [])
        logger.info("[TRACE] get_body: found %d parts", len(parts))
        for part in parts:
            logger.info("[TRACE] get_body: part mimeType: %s", part['mimeType'])
            if part['mimeType'] == 'text/plain':
                import base64
                decoded = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                logger.info("[TRACE] get_body: decoded text/plain body (first 100 chars): %s", safe_ascii(decoded[:100]))
                return decoded
        logger.info("[TRACE] get_body: no text/plain part found, returning snippet")
        return msg_data['snippet']
    except Exception as e:
        logger.error("[TRACE] get_body: exception: %s, returning snippet", e)

        return msg_data['snippet'] 
