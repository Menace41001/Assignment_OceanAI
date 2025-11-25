import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from typing import Dict, Any, List
import json

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("Warning: GOOGLE_API_KEY not found in environment variables.")

# Initialize Gemini Model
# User requested gemini-2.5-flash. 
# Note: If this model version is not available via API yet, this might fail at runtime.
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GOOGLE_API_KEY, temperature=0)

async def process_email_with_prompt(email_content: str, prompt_template: str, output_json: bool = False) -> Any:
    """
    Process an email using a specific prompt template.
    """
    prompt = ChatPromptTemplate.from_template(prompt_template + "\n\nEmail Content:\n{email_content}")
    
    if output_json:
        chain = prompt | llm | JsonOutputParser()
    else:
        chain = prompt | llm | StrOutputParser()
    
    try:
        result = await chain.ainvoke({"email_content": email_content})
        return result
    except Exception as e:
        print(f"Error processing email: {e}")
        return None

async def chat_with_email(email_content: str, user_query: str) -> str:
    """
    Chat with a specific email.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful email assistant. Answer the user's question based on the following email content."),
        ("user", "Email Content:\n{email_content}\n\nQuestion: {user_query}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        return await chain.ainvoke({"email_content": email_content, "user_query": user_query})
    except Exception as e:
        return f"Error: {str(e)}"

async def generate_draft_reply(email_content: str, instructions: str = None) -> str:
    """
    Generate a draft reply for an email.
    """
    if not instructions:
        instructions = "Draft a polite and professional reply to this email. Keep it concise."
        
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful email assistant. Your goal is to draft email replies."),
        ("user", "Email Content:\n{email_content}\n\nInstructions: {instructions}\n\nDraft Reply:")
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        return await chain.ainvoke({"email_content": email_content, "instructions": instructions})
    except Exception as e:
        return f"Error generating draft: {str(e)}"
