from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from models import Email, PromptConfig, Draft, GenerateDraftRequest
from services.store import store
from services.ingestion import load_mock_data
from services.processor import process_inbox, process_single_email
from services.llm_engine import chat_with_email, generate_draft_reply
from models import ChatRequest

app = FastAPI(title="Email Productivity Agent API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    load_mock_data()

@app.get("/")
def read_root():
    return {"message": "Email Productivity Agent API is running"}

@app.get("/emails", response_model=List[Email])
def get_emails():
    return store.get_all_emails()

@app.get("/emails/{email_id}", response_model=Email)
def get_email(email_id: str):
    email = store.get_email(email_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email

@app.get("/prompts", response_model=List[PromptConfig])
def get_prompts():
    return store.get_all_prompts()

@app.put("/prompts/{prompt_id}")
def update_prompt(prompt_id: str, prompt: PromptConfig):
    if prompt_id != prompt.id:
        raise HTTPException(status_code=400, detail="Prompt ID mismatch")
    store.update_prompt(prompt)
    return {"message": "Prompt updated"}

@app.post("/ingest")
async def trigger_ingest():
    # In a real app, this might trigger fetching from an IMAP server
    # Here we just reload mock data or reset
    load_mock_data()
    return {"message": "Ingestion triggered"}

@app.post("/process")
async def trigger_process(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_inbox)
    return {"message": "Inbox processing started in background"}

@app.post("/process/{email_id}")
async def trigger_process_email(email_id: str):
    await process_single_email(email_id)
    return {"message": f"Processing started for {email_id}"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if request.email_id:
        email = store.get_email(request.email_id)
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        response = await chat_with_email(email.body, request.query)
        return {"response": response}
    else:
        # Chat with whole inbox (future scope or simple implementation)
        return {"response": "Global inbox chat not implemented yet. Please select an email."}

@app.get("/drafts", response_model=List[Draft])
def get_drafts():
    return store.get_all_drafts()

@app.post("/drafts", response_model=Draft)
def create_draft(draft: Draft):
    store.save_draft(draft)
    return draft

@app.put("/drafts/{draft_id}", response_model=Draft)
def update_draft(draft_id: str, draft: Draft):
    if draft_id != draft.id:
        raise HTTPException(status_code=400, detail="Draft ID mismatch")
    store.save_draft(draft)
    return draft

@app.post("/drafts/generate")
async def generate_draft(request: GenerateDraftRequest):
    email = store.get_email(request.email_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    draft_body = await generate_draft_reply(email.body, request.instructions)
    return {"draft_body": draft_body}
