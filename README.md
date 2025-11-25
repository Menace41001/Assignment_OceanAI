# Email Productivity Agent

## Overview
An intelligent, prompt-driven Email Productivity Agent capable of processing an inbox, categorizing emails, extracting action items, and generating draft replies using LLMs.

## Project Structure
- `backend/`: FastAPI application handling email processing, storage, and LLM integration.
- `frontend/`: React + Vite application providing the user interface.

## Setup Instructions

### Prerequisites
- Node.js & npm
- Python 3.10+
- OpenAI API Key (Set as `OPENAI_API_KEY` environment variable)

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

### Frontend Setup (React/Vite)
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   The UI will be available at `http://localhost:5173` (or similar port).

## Usage
1. **Load Inbox**: The mock inbox is loaded automatically by the backend.
2. **Process Inbox**: Click "Process Inbox" in the sidebar to categorize emails and extract actions.
3. **View Emails**: Select an email from the list to view details and AI insights.
4. **Chat**: Use the "AI Assistant" section in the email detail view to ask questions or draft replies.
5. **Configure Prompts**: Go to "Prompt Brain" to edit the agent's instructions.

## Mock Data
The mock inbox is located at `backend/data/mock_inbox.json`. You can edit this file to test different scenarios.
