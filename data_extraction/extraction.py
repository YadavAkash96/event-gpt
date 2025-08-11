import requests
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("EVENTBRITE_TOKEN")

def fetch_events(token, location="Berlin"):
    url = "https://www.eventbriteapi.com/v3/events/search/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "location.address": location,
        # minimal params for now
    }
    response = requests.get(url, headers=headers, params=params)
    print(f"Status code: {response.status_code}")
    print(response.text)  # will help debug errors
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    events_data = fetch_events(TOKEN, "Berlin")
    print(f"Fetched {len(events_data.get('events', []))} events")
