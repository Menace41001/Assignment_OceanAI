from typing import List, Dict
from models import Email, PromptConfig, Draft

class Store:
    def __init__(self):
        self.emails: Dict[str, Email] = {}
        self.prompts: Dict[str, PromptConfig] = {}
        self.drafts: Dict[str, Draft] = {}

        # Initialize default prompts
        self._init_default_prompts()

    def _init_default_prompts(self):
        defaults = [
            PromptConfig(
                id="categorize",
                name="Categorization",
                template="Categorize the following email into one of these categories: Important, Newsletter, Spam, To-Do. To-Do emails must include a direct request requiring user action. Return only the category name.",
                description="Determines the category of an email."
            ),
            PromptConfig(
                id="action_items",
                name="Action Item Extraction",
                template="Extract tasks from the email. Return a JSON list of objects with 'task' and 'deadline' fields. If no tasks, return an empty list.",
                description="Extracts actionable tasks from email content."
            ),
            PromptConfig(
                id="auto_reply",
                name="Auto-Reply Draft",
                template="Draft a polite and professional reply to this email. If it is a meeting request, ask for an agenda. Keep it concise.",
                description="Generates a draft reply."
            )
        ]
        for p in defaults:
            self.prompts[p.id] = p

    def add_email(self, email: Email):
        self.emails[email.id] = email

    def get_all_emails(self) -> List[Email]:
        return list(self.emails.values())

    def get_email(self, email_id: str) -> Email:
        return self.emails.get(email_id)

    def update_email(self, email: Email):
        self.emails[email.id] = email

    def get_prompt(self, prompt_id: str) -> PromptConfig:
        return self.prompts.get(prompt_id)
    
    def update_prompt(self, prompt: PromptConfig):
        self.prompts[prompt.id] = prompt

    def get_all_prompts(self) -> List[PromptConfig]:
        return list(self.prompts.values())

    def save_draft(self, draft: Draft):
        self.drafts[draft.id] = draft

    def get_all_drafts(self) -> List[Draft]:
        return list(self.drafts.values())

# Global store instance
store = Store()
