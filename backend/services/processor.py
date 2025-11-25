from typing import List
from services.store import store
from services.llm_engine import process_email_with_prompt
from models import Email

async def process_inbox():
    """
    Iterates through all emails in the store and processes them if they haven't been processed.
    """
    emails = store.get_all_emails()
    prompts = store.get_all_prompts()
    
    categorize_prompt = next((p for p in prompts if p.id == "categorize"), None)
    action_prompt = next((p for p in prompts if p.id == "action_items"), None)
    
    if not categorize_prompt or not action_prompt:
        print("Error: Default prompts not found.")
        return

    for email in emails:
        # Skip if already processed (logic can be improved to force re-process)
        if email.category and email.action_items:
            continue
            
        try:
            print(f"Processing email: {email.id}")
            
            # Categorize
            category = await process_email_with_prompt(email.body, categorize_prompt.template, output_json=False)
            if category:
                email.category = category.strip()
                
            # Extract Action Items
            action_items = await process_email_with_prompt(email.body, action_prompt.template, output_json=True)
            if action_items:
                if isinstance(action_items, list):
                    email.action_items = action_items
                else:
                    # Handle case where LLM returns a single object instead of list
                    email.action_items = [action_items]
            
            store.update_email(email)
            print(f"Finished processing {email.id}")
        except Exception as e:
            print(f"Error processing email {email.id}: {e}")

async def process_single_email(email_id: str):
    """Process a single email by ID."""
    email = store.get_email(email_id)
    if not email:
        return
        
    prompts = store.get_all_prompts()
    categorize_prompt = next((p for p in prompts if p.id == "categorize"), None)
    action_prompt = next((p for p in prompts if p.id == "action_items"), None)
    
    if categorize_prompt:
        category = await process_email_with_prompt(email.body, categorize_prompt.template, output_json=False)
        if category:
            email.category = category.strip()

    if action_prompt:
        action_items = await process_email_with_prompt(email.body, action_prompt.template, output_json=True)
        if action_items:
             if isinstance(action_items, list):
                email.action_items = action_items
             else:
                email.action_items = [action_items]

    store.update_email(email)
