import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

def analyze_email(email):
    prompt = f"""
You are an email assistant. Analyze this email and return ONLY a JSON object.

Email Details:
From: {email['sender']}
Subject: {email['subject']}
Body: {email['body']}

Return ONLY this JSON format, nothing else:
{{
    "summary": "one sentence summary here",
    "sentiment": "positive or neutral or negative",
    "priority": "high or medium or low",
    "category": "work or personal or spam or newsletter",
    "suggested_reply": "a professional 2-3 sentence reply here"
}}
"""
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        },
        json={
            "model": "google/gemma-4-26b-a4b-it:free",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    response_data = response.json()
    result = response_data['choices'][0]['message']['content'].strip()
    result = result.replace('```json', '').replace('```', '').strip()
    return json.loads(result)