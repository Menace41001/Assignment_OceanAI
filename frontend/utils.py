import requests

API_BASE_URL = "http://localhost:8000"

def get_emails():
    try:
        response = requests.get(f"{API_BASE_URL}/emails")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def get_prompts():
    try:
        response = requests.get(f"{API_BASE_URL}/prompts")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def update_prompt(prompt_id, data):
    try:
        response = requests.put(f"{API_BASE_URL}/prompts/{prompt_id}", json=data)
        return response.status_code == 200
    except:
        return False

def trigger_process():
    try:
        requests.post(f"{API_BASE_URL}/process")
        return True
    except:
        return False

def chat_with_email(email_id, query):
    try:
        response = requests.post(f"{API_BASE_URL}/chat", json={"email_id": email_id, "query": query})
        if response.status_code == 200:
            return response.json().get("response")
        return "Error communicating with agent."
    except:
        return "Error communicating with agent."
