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
        try:
            print(f"Processing email: {email.id}")
            
            # Categorize
            category = await process_email_with_prompt(
                email.body, 
                categorize_prompt.template, 
                output_json=False,
                system_template=categorize_prompt.system_template
            )
            if category:
                # Sanitize: extract only the category word
                category = category.strip()
                
                # Define valid categories
                valid_categories = ["Important", "To-Do", "Newsletter", "Spam"]
                
                # Try to find a valid category in the response
                found_category = None
                category_lower = category.lower()
                
                for valid_cat in valid_categories:
                    if valid_cat.lower() in category_lower:
                        found_category = valid_cat
                        break
                
                if found_category:
                    email.category = found_category
                else:
                    # Fallback: try to extract from common patterns
                    for prefix in ["Category:", "category:", "The category is", "This email is", "classified as", "categorized as"]:
                        if prefix.lower() in category_lower:
                            # Extract text after the prefix
                            parts = category.split(prefix, 1)
                            if len(parts) > 1:
                                remainder = parts[1].strip()
                                # Check if remainder starts with a valid category
                                for valid_cat in valid_categories:
                                    if remainder.lower().startswith(valid_cat.lower()):
                                        found_category = valid_cat
                                        break
                                if found_category:
                                    break
                    
                    if found_category:
                        email.category = found_category
                    else:
                        # Last resort: take first word and capitalize
                        first_word = category.split()[0] if category.split() else category
                        first_word = first_word.strip('"\'.,!?:')
                        email.category = first_word.capitalize()
                
            # Extract Action Items
            action_items = await process_email_with_prompt(
                email.body, 
                action_prompt.template, 
                output_json=True,
                system_template=action_prompt.system_template
            )
            if action_items:
                if isinstance(action_items, list):
                    email.action_items = action_items
                else:
                    # Handle case where LLM returns a single object instead of list
                    email.action_items = [action_items]
            
            store.update_email(email)
            print(f"Finished processing {email.id}: category={email.category}")
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
        category = await process_email_with_prompt(
            email.body, 
            categorize_prompt.template, 
            output_json=False,
            system_template=categorize_prompt.system_template
        )
        if category:
            # Sanitize: extract only the category word
            category = category.strip()
            
            # Define valid categories
            valid_categories = ["Important", "To-Do", "Newsletter", "Spam"]
            
            # Try to find a valid category in the response
            found_category = None
            category_lower = category.lower()
            
            for valid_cat in valid_categories:
                if valid_cat.lower() in category_lower:
                    found_category = valid_cat
                    break
            
            if found_category:
                email.category = found_category
            else:
                # Fallback: try to extract from common patterns
                for prefix in ["Category:", "category:", "The category is", "This email is", "classified as", "categorized as"]:
                    if prefix.lower() in category_lower:
                        parts = category.split(prefix, 1)
                        if len(parts) > 1:
                            remainder = parts[1].strip()
                            for valid_cat in valid_categories:
                                if remainder.lower().startswith(valid_cat.lower()):
                                    found_category = valid_cat
                                    break
                            if found_category:
                                break
                
                if found_category:
                    email.category = found_category
                else:
                    first_word = category.split()[0] if category.split() else category
                    first_word = first_word.strip('"\'.,!?:')
                    email.category = first_word.capitalize()

    if action_prompt:
        action_items = await process_email_with_prompt(
            email.body, 
            action_prompt.template, 
            output_json=True,
            system_template=action_prompt.system_template
        )
        if action_items:
             if isinstance(action_items, list):
                email.action_items = action_items
             else:
                email.action_items = [action_items]

    store.update_email(email)
