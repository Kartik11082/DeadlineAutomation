import datetime as dt
import os
import re

from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

app = Flask(__name__)
CORS(app)

# Allow HTTP for local development (do not use in production)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Google Calendar setup
SCOPES = ["https://www.googleapis.com/auth/calendar"]
TOKEN_FILE = "token.json"
CREDS_FILE = "credentials.json"


def get_calendar_service():
    """Return an authenticated Google Calendar service with logging."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if creds and creds.expired and creds.refresh_token:
        print("⚡ Refreshing expired token...")
        creds.refresh(Request())

    if not creds or not creds.valid:
        raise Exception("No valid credentials. Please visit /authorize first.")

    print("✅ Using valid credentials for Google Calendar API.")
    return build("calendar", "v3", credentials=creds)


@app.route("/authorize")
def authorize():
    """Start OAuth flow."""
    flow = Flow.from_client_secrets_file(
        CREDS_FILE,
        scopes=SCOPES,
        redirect_uri="http://localhost:5000/oauth2callback",
    )
    auth_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    print(f"🔗 Redirecting user to Google OAuth: {auth_url}")
    return redirect(auth_url)


@app.route("/oauth2callback")
def oauth2callback():
    """Handle OAuth callback and save token.json."""
    flow = Flow.from_client_secrets_file(
        CREDS_FILE,
        scopes=SCOPES,
        redirect_uri="http://localhost:5000/oauth2callback",
    )
    flow.fetch_token(authorization_response=request.url)

    creds = flow.credentials
    with open(TOKEN_FILE, "w") as token_file:
        token_file.write(creds.to_json())

    print("✅ Authentication complete. Token saved to token.json.")
    return "✅ Authentication complete! You can close this tab and use the extension."


@app.route("/receive-html", methods=["POST"])
# def receive_html():
#     """Receive HTML, parse deadlines, and add them to Google Calendar with detailed logging."""
#     data = request.get_json()
#     html = data.get("html", "")
#     url = data.get("url", "")
#     print(f"📩 Received HTML from URL: {url[:100]}...")  # print first 100 chars

#     # Regex: mm/dd/yyyy : event
#     pattern = r"(\d{1,2}/\d{1,2}/\d{4})\s*:\s*([^<\n]+)"
#     matches = re.findall(pattern, html)

#     print(f"🔎 Found {len(matches)} event(s) in HTML.")
#     results = []

#     # if events:
#     #     last_event = events[-1]   # get the last event
#     #     add_event_to_calendar(last_event)

#     for date, event in matches:
#         clean_event = event.strip()
#         results.append({"date": date, "event": clean_event})
#         add_to_calendar(date, clean_event)

#     print(f"✅ Added {len(results)} event(s) to Google Calendar.")
#     return jsonify({"status": "added", "count": len(results), "results": results})

import datetime as dt
import os
import re

from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

app = Flask(__name__)
CORS(app)

# Allow HTTP for local development (do not use in production)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Google Calendar setup
SCOPES = ["https://www.googleapis.com/auth/calendar"]
TOKEN_FILE = "token.json"
CREDS_FILE = "credentials.json"


def get_calendar_service():
    """Return an authenticated Google Calendar service with logging."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if creds and creds.expired and creds.refresh_token:
        print("⚡ Refreshing expired token...")
        creds.refresh(Request())

    if not creds or not creds.valid:
        raise Exception("No valid credentials. Please visit /authorize first.")

    print("✅ Using valid credentials for Google Calendar API.")
    return build("calendar", "v3", credentials=creds)


@app.route("/authorize")
def authorize():
    """Start OAuth flow."""
    flow = Flow.from_client_secrets_file(
        CREDS_FILE,
        scopes=SCOPES,
        redirect_uri="http://localhost:5000/oauth2callback",
    )
    auth_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    print(f"🔗 Redirecting user to Google OAuth: {auth_url}")
    return redirect(auth_url)


@app.route("/oauth2callback")
def oauth2callback():
    """Handle OAuth callback and save token.json."""
    flow = Flow.from_client_secrets_file(
        CREDS_FILE,
        scopes=SCOPES,
        redirect_uri="http://localhost:5000/oauth2callback",
    )
    flow.fetch_token(authorization_response=request.url)

    creds = flow.credentials
    with open(TOKEN_FILE, "w") as token_file:
        token_file.write(creds.to_json())

    print("✅ Authentication complete. Token saved to token.json.")
    return "✅ Authentication complete! You can close this tab and use the extension."


@app.route("/receive-html", methods=["POST"])
def receive_html():
    """Receive HTML, parse deadlines, and add them to Google Calendar with detailed logging."""
    data = request.get_json()
    html = data.get("html", "")
    url = data.get("url", "")
    print(f"📩 Received HTML from URL: {url[:100]}...")  # print first 100 chars

    # Regex: mm/dd/yyyy : event
    pattern = r"(\d{1,2}/\d{1,2}/\d{4})\s*:\s*([^<\n]+)"
    matches = re.findall(pattern, html)

    print(f"🔎 Found {len(matches)} event(s) in HTML.")
    results = []

    # if events:
    #     last_event = events[-1]   # get the last event
    #     add_event_to_calendar(last_event)

    for date, event in matches:
        clean_event = event.strip()
        results.append({"date": date, "event": clean_event})
        add_to_calendar(date, clean_event)

    print(f"✅ Added {len(results)} event(s) to Google Calendar.")
    return jsonify({"status": "added", "count": len(results), "results": results})


def add_to_calendar(date_str, summary):
    """Insert event into Google Calendar with visible prefix, description, color, and detailed logs."""
    service = get_calendar_service()

    # Parse date
    try:
        month, day, year = map(int, date_str.split("/"))
        event_date = dt.date(year, month, day)
        if event_date < dt.date.today():
            print(f"⏭ Skipping past date: {event_date} ({summary})")
            return

        start_date = dt.date(year, month, day)
    except Exception as e:
        print(f"❌ Failed to parse date '{date_str}': {e}")
        return

    event_body = {
        "summary": f"[Auto CS 6344 DR] {summary}",
        "description": "Added automatically via DeadlineAutomation script",
        "start": {"date": start_date.isoformat()},
        "end": {"date": start_date.isoformat()},
        "colorId": "9",  # distinguishable color
    }

    try:
        created_event = (
            service.events().insert(calendarId="primary", body=event_body).execute()
        )
        print(f"✅ Event created: {created_event.get('summary')} on {date_str}")
        print(f"🔗 Link: {created_event.get('htmlLink')}")
    except Exception as e:
        print(f"❌ Failed to create event '{summary}' on {date_str}: {e}")


if __name__ == "__main__":
    app.run(port=5000, debug=True)


def add_to_calendar(date_str, summary):
    """Insert event into Google Calendar with visible prefix, description, color, and detailed logs."""
    service = get_calendar_service()

    # Parse date
    try:
        month, day, year = map(int, date_str.split("/"))
        event_date = dt.date(year, month, day)
        if event_date < dt.date.today():
            print(f"⏭ Skipping past date: {event_date} ({summary})")
            return

        start_date = dt.date(year, month, day)
    except Exception as e:
        print(f"❌ Failed to parse date '{date_str}': {e}")
        return

    event_body = {
        "summary": f"[Auto CS 6344 DR] {summary}",
        "description": "Added automatically via DeadlineAutomation script",
        "start": {"date": start_date.isoformat()},
        "end": {"date": start_date.isoformat()},
        "colorId": "9",  # distinguishable color
    }

    try:
        created_event = (
            service.events().insert(calendarId="primary", body=event_body).execute()
        )
        print(f"✅ Event created: {created_event.get('summary')} on {date_str}")
        print(f"🔗 Link: {created_event.get('htmlLink')}")
    except Exception as e:
        print(f"❌ Failed to create event '{summary}' on {date_str}: {e}")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
