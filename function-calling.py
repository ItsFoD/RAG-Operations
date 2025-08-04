import os
import json
from datetime import datetime, timedelta
from openai import AzureOpenAI
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from keys import endpoint, deployment, subscription_key

# --- Azure OpenAI Setup ---
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
)

# --- Google Calendar Setup ---
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret_485292368779-6s9015gm70f22k5dslcgeos1mlkodfbb.apps.googleusercontent.com.json',
            SCOPES
        )
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

# --- Freeform chat response ---
def get_response(prompt):
    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# --- Classify prompt ---
def classify_prompt(prompt):
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    classification_prompt = f"""
Today is {today} and tomorrow is {tomorrow}.

Classify the user's intent from this message: "{prompt}"

Respond in JSON format with:
- "action": one of ["chat", "get_date", "create_event"]
- If action is "get_date", include "label": "today" or "tomorrow", and "date": "YYYY-MM-DD"
- If action is "create_event", include: summary, description, start_time (YYYY-MM-DDTHH:MM:SS), end_time, and timezone set to "Africa/Cairo"
- Do NOT include attendee_email
- Otherwise, respond with: {{ "action": "chat" }}
"""

    result = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "system", "content": classification_prompt}],
        temperature=0,
        max_tokens=500
    )
    return result.choices[0].message.content.strip()

# --- Create event ---
def create_event_from_json(data, service):
    event = {
        'summary': data['summary'],
        'description': data['description'],
        'start': {'dateTime': data['start_time'], 'timeZone': data['timezone']},
        'end': {'dateTime': data['end_time'], 'timeZone': data['timezone']}
    }
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print("✅ Event created:", created_event.get('htmlLink'))

# --- Main loop ---
def main():
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break

        try:
            classification = classify_prompt(user_input)
            data = json.loads(classification)
            action = data.get("action")

            if action == "get_date":
                print(f"📅 Assistant: The {data['label']}'s date is: {data['date']}")

            elif action == "create_event":
                service = authenticate_google_calendar()
                create_event_from_json(data, service)

            else:
                # General chat
                chat_response = get_response(user_input)
                print("🤖 Assistant:", chat_response)

        except json.JSONDecodeError:
            print("❌ Could not parse classification response:")
            print(classification)

if __name__ == '__main__':
    main()
