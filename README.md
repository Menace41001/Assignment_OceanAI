# Email Productivity Agent

An AI-powered email management system that automatically categorizes emails, extracts action items, and helps you stay organized.

---

## � Setup Instructions

### Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))

### Step 1: Install Backend Dependencies

```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Step 2: Configure API Key

Create a file `backend/.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 3: Install Frontend Dependencies

```bash
cd frontend
npm install
```

---

## ▶️ How to Run

You need **two terminal windows** running simultaneously:

### Terminal 1: Start Backend

```bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
uvicorn main:app --reload
```

✅ Backend will run at: **http://localhost:8000**

### Terminal 2: Start Frontend

```bash
cd frontend
npm run dev
```

✅ Frontend will run at: **http://localhost:5173**

Open your browser and go to **http://localhost:5173**

---

## � How to Load Mock Inbox

The mock inbox loads **automatically** when you start the backend.

### View/Edit Mock Data

The sample emails are in: `backend/data/mock_inbox.json`

To customize:
1. Edit `mock_inbox.json` with your own sample emails
2. Restart the backend
3. Click **"Process Inbox"** in the UI

### Reset Data

To start fresh:
1. Delete `backend/persistence.json`
2. Restart the backend
3. Mock data will reload automatically

---

## ⚙️ How to Configure Prompts

### Method 1: Using the UI (Recommended)

1. Go to the **"Prompt Config"** tab in the web interface
2. Click on any prompt to edit it
3. Make your changes
4. Changes save automatically when you click outside the text box

**Available Prompts:**
- **Categorization**: Controls how emails are sorted (Important, To-Do, Newsletter, Spam)
- **Action Item Extraction**: Defines how tasks and deadlines are identified

### Method 2: Edit Code Directly

Edit default prompts in: `backend/services/store.py`

Look for the `DEFAULT_PROMPTS` list (around line 20).

**Note:** Changes in code only apply to new installations. Existing data uses saved prompts from `persistence.json`.

---

## 📖 Usage Examples

### Example 1: Process Emails

1. Open the app at http://localhost:5173
2. Click **"Process Inbox"** button
3. Watch emails get categorized in real-time (updates every 2 seconds)
4. See color-coded badges: 🟢 To-Do, 🟣 Newsletter, 🔴 Spam, 🟠 Important

### Example 2: Chat with Inbox

**Ask questions about all emails:**
1. Don't select any email
2. Type in the chat box: "Show me urgent emails"
3. Or try: "What are my deadlines?"

**Ask about a specific email:**
1. Click on an email to select it
2. Type: "Summarize this email"
3. Or: "What action items are in this?"

### Example 3: Generate Draft Reply

1. Click on any email
2. Click **"Draft Reply"** button
3. In the Drafts tab, click **"Generate with AI"**
4. Add instructions like: "Polite decline" or "Accept and ask for agenda"
5. Click **"Generate"**
6. Edit the generated draft
7. Click **"Save Draft"**

### Example 4: Customize Categorization

1. Go to **"Prompt Config"** tab
2. Edit the "Categorization" prompt
3. Example change: Add a new category or change the rules
4. Click outside to save
5. Go back to Inbox and click **"Process Inbox"** to re-categorize

---

## � Troubleshooting

**"Backend won't start"**
- Check if `OPENAI_API_KEY` is set in `backend/.env`
- Make sure virtual environment is activated
- Verify port 8000 is not in use

**"Frontend can't connect to backend"**
- Ensure backend is running on http://localhost:8000
- Check browser console for errors
- Try restarting both servers

**"Emails not processing"**
- Verify OpenAI API key is valid
- Check you have API credits at https://platform.openai.com/usage
- Look at backend terminal for error messages

**"Changes to prompts not working"**
- Make sure you clicked outside the text box to save
- Try refreshing the page
- Click "Process Inbox" again to re-process with new prompts

---

## 📁 Project Structure

```
Assignment_OceanAI/
├── backend/
│   ├── main.py              # API server
│   ├── models.py            # Data models
│   ├── services/
│   │   ├── store.py         # Data storage
│   │   ├── processor.py     # Email processing
│   │   ├── llm_engine.py    # OpenAI integration
│   │   └── ingestion.py     # Mock data loader
│   ├── data/
│   │   └── mock_inbox.json  # Sample emails
│   └── persistence.json     # Saved data (auto-generated)
│
└── frontend/
    └── src/
        ├── App.jsx          # Main UI
        └── api.js           # Backend client
```

---

## 🎯 Key Features

- ✅ Automatic email categorization (Important, To-Do, Newsletter, Spam)
- ✅ Action item extraction with deadlines
- ✅ AI-powered chat for inbox queries
- ✅ Draft generation and management
- ✅ Customizable AI prompts
- ✅ Data persistence across restarts
- ✅ Real-time processing updates

---

## � Notes

- Uses OpenAI GPT-4o model
- All data stored in `backend/persistence.json`
- Mock data reloads automatically on first startup
- CORS enabled for development (localhost only)
