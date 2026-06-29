from gmail_client import get_gmail_service, fetch_emails
from email_parser import parse_email
from ai_agent import analyze_email

print("🔌 Connecting to Gmail...")
service = get_gmail_service()
print("✅ Connected!\n")

print("📧 Fetching emails...")
raw_emails = fetch_emails(service, max_results=3)
print(f"✅ Got {len(raw_emails)} emails!\n")

for i, raw in enumerate(raw_emails):
    print(f"{'='*50}")
    print(f"📩 EMAIL {i+1}")
    
    email = parse_email(raw)
    print(f"From    : {email['sender']}")
    print(f"Subject : {email['subject']}")
    
    print(f"🤖 Analyzing with Gemini AI...")
    analysis = analyze_email(email)
    
    print(f"📌 Priority  : {analysis['priority'].upper()}")
    print(f"😊 Sentiment : {analysis['sentiment']}")
    print(f"📂 Category  : {analysis['category']}")
    print(f"📝 Summary   : {analysis['summary']}")
    print(f"💬 Reply     : {analysis['suggested_reply']}")
    print()