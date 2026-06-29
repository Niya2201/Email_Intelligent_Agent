from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    creds = None

    # Try Streamlit Cloud secrets first
    try:
        import streamlit as st
        token = st.secrets.get("GOOGLE_TOKEN", None)
        creds_json = st.secrets.get("GOOGLE_CREDENTIALS", None)
        
        if token:
            with open('token.json', 'w') as f:
                f.write(token)
        if creds_json:
            with open('credentials.json', 'w') as f:
                f.write(creds_json)
    except Exception:
        pass  # Local mode — use files directly

    # Local mode
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def fetch_emails(service, max_results=5):
    results = service.users().messages().list(
        userId='me', maxResults=max_results, labelIds=['INBOX']
    ).execute()
    messages = results.get('messages', [])
    emails = []
    for msg in messages:
        detail = service.users().messages().get(
            userId='me', id=msg['id'], format='full'
        ).execute()
        emails.append(detail)
    return emails