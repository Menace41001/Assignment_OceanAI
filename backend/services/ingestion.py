import json
import os
from typing import List
from models import Email
from services.store import store
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "mock_inbox.json")

def load_mock_data():
    """Loads mock emails from JSON file into the store."""
    if not os.path.exists(DATA_PATH):
        print(f"Warning: Mock data file not found at {DATA_PATH}")
        return

    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    
    for item in data:
        # Convert timestamp string to datetime object
        try:
            item['timestamp'] = datetime.fromisoformat(item['timestamp'].replace('Z', '+00:00'))
        except ValueError:
            pass # Keep as is or handle error
            
        email = Email(**item)
        store.add_email(email)
    
    print(f"Loaded {len(data)} emails into store.")
