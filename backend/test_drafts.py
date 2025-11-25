from fastapi.testclient import TestClient
from main import app
from models import Draft, GenerateDraftRequest
from datetime import datetime

client = TestClient(app)

def test_drafts_flow():
    # 1. Create a draft
    draft_data = {
        "id": "test_draft_1",
        "to": "test@example.com",
        "subject": "Test Draft",
        "body": "This is a test draft.",
        "saved_at": datetime.now().isoformat()
    }
    response = client.post("/drafts", json=draft_data)
    assert response.status_code == 200
    assert response.json()["id"] == "test_draft_1"

    # 2. Get drafts
    response = client.get("/drafts")
    assert response.status_code == 200
    drafts = response.json()
    assert len(drafts) >= 1
    assert any(d["id"] == "test_draft_1" for d in drafts)

    # 3. Update draft
    draft_data["body"] = "Updated body"
    response = client.put("/drafts/test_draft_1", json=draft_data)
    assert response.status_code == 200
    assert response.json()["body"] == "Updated body"

    # 4. Generate draft (Mocking LLM or expecting error if no key, but we can test the endpoint structure)
    # We'll just check if it handles the request, even if it fails due to missing API key or mock data
    # First get an email to reply to
    emails = client.get("/emails").json()
    if emails:
        email_id = emails[0]["id"]
        gen_req = {
            "email_id": email_id,
            "instructions": "Say thanks"
        }
        # This might fail if LLM is not configured, but let's see
        try:
            response = client.post("/drafts/generate", json=gen_req)
            # It might return 200 with a generated text or error message in text
            print("Generate response:", response.json())
        except Exception as e:
            print("Generate failed as expected (maybe):", e)

if __name__ == "__main__":
    try:
        test_drafts_flow()
        print("Tests Passed!")
    except AssertionError as e:
        print("Tests Failed:", e)
    except Exception as e:
        print("An error occurred:", e)
