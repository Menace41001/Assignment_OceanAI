# Email Productivity Agent

## Overview
This project is an intelligent, prompt-driven Email Productivity Agent designed to streamline email management. It leverages Large Language Models (LLMs) to automatically categorize emails, extract actionable tasks, and generate context-aware draft replies. The system features a modern React-based frontend and a robust FastAPI backend.

## Key Features

### 1. Email Ingestion & Management
- **Mock Inbox**: Loads a diverse set of sample emails (Meeting requests, Newsletters, Spam, etc.) from a JSON source.
- **Inbox View**: Displays emails with sender, subject, timestamp, and status (read/unread).

### 2. Intelligent Processing (LLM-Powered)
- **Auto-Categorization**: Automatically tags emails as *Important*, *Newsletter*, *Spam*, or *To-Do* based on content.
- **Action Item Extraction**: Identifies and extracts specific tasks and deadlines from email bodies.
- **Background Processing**: Uses asynchronous background tasks to process the inbox without blocking the UI.

### 3. Email Agent Chat
- **RAG-like Interaction**: Chat with specific emails to ask questions like "Summarize this" or "What are the key dates?".
- **Context Awareness**: The agent understands the specific email context when answering.

### 4. Drafts Management (New!)
- **Create & Edit**: Full-featured editor to create new drafts or edit existing ones.
- **Draft Reply**: Instantly create a reply draft from any email in the inbox.
- **Save & Persist**: Drafts are saved to the backend store.

### 5. AI Draft Generation (New!)
- **AI Writer**: Generate professional email drafts by simply providing instructions (e.g., "Polite refusal", "Accept and ask for agenda").
- **Contextual**: The AI uses the original email content to generate relevant replies.

### 6. Prompt Configuration ("Brain")
- **Customizable Logic**: View and edit the system prompts used for categorization, extraction, and drafting.
- **Real-time Updates**: Changes to prompts take effect immediately for subsequent processing.

## Technical Implementation

### Backend (`backend/`)
- **Framework**: FastAPI (Python)
- **LLM Integration**: LangChain + Google Gemini (gemini-2.5-flash)
- **Concurrency**: Fully async/await architecture with `BackgroundTasks` for non-blocking operations.
- **Data Store**: In-memory storage (simulated database) with Pydantic models for validation.
- **API**: RESTful endpoints for emails, prompts, drafts, and chat.

### Frontend (`frontend/`)
- **Framework**: React + Vite
- **Styling**: TailwindCSS (v4) for a modern, responsive design.
- **Architecture**: Component-based (InboxView, DraftsView, BrainView).
- **State Management**: React Hooks (`useState`, `useEffect`) for real-time UI updates.

## Setup Instructions

### Prerequisites
- Node.js & npm
- Python 3.10+
- Google API Key (Set as `GOOGLE_API_KEY` environment variable in `backend/.env`)

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   uvicorn main:app --reload
   ```
   Server runs at `http://localhost:8000`.

### Frontend Setup
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
   UI runs at `http://localhost:5173`.

## Usage Guide
1. **Start**: Run both backend and frontend servers.
2. **Ingest**: The app loads mock data on startup.
3. **Process**: Click **"Process Inbox"** to run AI categorization. This runs in the background.
4. **Interact**: Click an email to view details. Use the **Chat** to ask questions.
5. **Draft**: Click **"Draft Reply"** to switch to the Drafts tab. Use the **AI Writer** to generate text, then edit and **Save**.
6. **Configure**: Go to **"Prompt Config"** to tweak the AI's behavior.
