import base64

def parse_email(msg):
    headers = msg['payload']['headers']
    
    subject = next((h['value'] for h in headers 
                   if h['name'] == 'Subject'), 'No Subject')
    sender = next((h['value'] for h in headers 
                  if h['name'] == 'From'), 'Unknown')
    
    body = ""
    payload = msg['payload']
    
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data', '')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
    elif 'body' in payload:
        data = payload['body'].get('data', '')
        if data:
            body = base64.urlsafe_b64decode(data).decode('utf-8')
    
    return {
        "subject": subject,
        "sender": sender,
        "body": body[:500]
    }