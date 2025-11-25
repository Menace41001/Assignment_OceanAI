import requests
import time

BASE_URL = "http://localhost:8000"

def check_health():
    try:
        print("Checking root...")
        res = requests.get(f"{BASE_URL}/")
        print(f"Root status: {res.status_code}, Response: {res.json()}")
        
        print("Checking emails...")
        res = requests.get(f"{BASE_URL}/emails")
        print(f"Emails status: {res.status_code}")
        emails = res.json()
        print(f"Email count: {len(emails)}")
        if len(emails) > 0:
            print(f"First email ID: {emails[0]['id']}")
        
        print("Triggering process...")
        start = time.time()
        res = requests.post(f"{BASE_URL}/process")
        duration = time.time() - start
        print(f"Process status: {res.status_code}, Duration: {duration:.2f}s")
        print(f"Process response: {res.json()}")
        
        # Check if it returns immediately (should be < 1s)
        if duration > 2.0:
            print("WARNING: Process took too long! Background task might not be working.")
        else:
            print("SUCCESS: Process returned immediately.")

        print("Waiting 5s for background processing...")
        time.sleep(5)
        
        print("Checking emails after process...")
        res = requests.get(f"{BASE_URL}/emails")
        emails = res.json()
        print(f"Email count: {len(emails)}")
        processed_count = sum(1 for e in emails if e.get('category'))
        print(f"Processed emails: {processed_count}")


    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_health()
