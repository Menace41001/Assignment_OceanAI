import streamlit as st
from utils import get_emails, get_prompts, update_prompt, trigger_process, chat_with_email
from datetime import datetime

# Page Config
st.set_page_config(layout="wide", page_title="Email Agent", page_icon="📧")

# Custom CSS for professional look
st.markdown("""
<style>
    /* Global Styles */
    .block-container { 
        padding-top: 2rem; 
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        transition: background-color 0.2s;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: #334155;
    }
    
    /* Email Card Styling */
    .email-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        cursor: pointer;
        transition: all 0.2s;
    }
    .email-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
    }
    .email-card.selected {
        border-left: 4px solid #3b82f6;
        background-color: #eff6ff;
    }
    
    /* Email Card Content */
    .email-sender {
        font-weight: 600;
        color: #111827;
        font-size: 0.95rem;
        margin-bottom: 4px;
    }
    .email-subject {
        font-weight: 500;
        color: #1f2937;
        font-size: 0.9rem;
        margin-bottom: 6px;
    }
    .email-preview {
        color: #6b7280;
        font-size: 0.85rem;
        margin-bottom: 8px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .email-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 8px;
    }
    .email-date {
        color: #9ca3af;
        font-size: 0.8rem;
    }
    
    /* Badge Styling */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-important { background-color: #ff6b35; color: white; }
    .badge-todo { background-color: #10b981; color: white; }
    .badge-newsletter { background-color: #8b5cf6; color: white; }
    .badge-spam { background-color: #ef4444; color: white; }
    .badge-default { background-color: #6b7280; color: white; }
    
    /* Detail View */
    .email-detail-header {
        background: white;
        padding: 24px;
        border-radius: 8px;
        margin-bottom: 16px;
        border: 1px solid #e5e7eb;
    }
    .email-detail-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 12px;
    }
    .email-detail-meta {
        color: #6b7280;
        font-size: 0.9rem;
    }
    .email-detail-body {
        background: white;
        padding: 24px;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        line-height: 1.6;
        color: #374151;
    }
    
    /* Action Items */
    .action-item {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 8px;
    }
    
    /* Buttons */
    .stButton button {
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Inbox header */
    .inbox-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 2px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "selected_email" not in st.session_state:
    st.session_state.selected_email = None
if "emails" not in st.session_state:
    st.session_state.emails = []
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# Sidebar
with st.sidebar:
    st.markdown("### 📧 Email Agent")
    st.markdown("**AI-Powered Productivity**")
    st.markdown("---")
    
    page = st.radio("", ["📥 Inbox", "🧠 Prompt Config", "📝 Drafts"], label_visibility="collapsed")
    
    st.markdown("---")
    
    if st.button("🔄 Process Inbox", use_container_width=True):
        with st.spinner("Processing emails..."):
            trigger_process()
            st.session_state.emails = get_emails()
            st.success("✓ Processed!")
            st.rerun()
    
    # Load emails if not loaded
    if not st.session_state.emails:
        st.session_state.emails = get_emails()
    
    st.markdown("---")
    st.markdown(f"**{len(st.session_state.emails)}** emails loaded")
    unread = sum(1 for e in st.session_state.emails if not e.get('read', False))
    st.markdown(f"**{unread}** unread")

# Main Content
if page == "📥 Inbox":
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="inbox-header"><h3 style="margin:0;">Inbox</h3></div>', unsafe_allow_html=True)
        
        for email in st.session_state.emails:
            # Determine badge
            category = email.get('category', '')
            badge_html = ""
            if category:
                badge_class = {
                    'Important': 'badge-important',
                    'To-Do': 'badge-todo',
                    'Newsletter': 'badge-newsletter',
                    'Spam': 'badge-spam'
                }.get(category, 'badge-default')
                badge_html = f'<span class="badge {badge_class}">{category}</span>'
            
            # Task count badge
            action_items = email.get('action_items')
            task_count = len(action_items) if action_items is not None else 0
            if task_count > 0:
                badge_html += f'<span class="badge badge-todo">{task_count} tasks</span>'
            
            # Format date
            try:
                dt = datetime.fromisoformat(str(email['timestamp']).replace('Z', '+00:00'))
                date_str = dt.strftime('%b %d')
            except:
                date_str = "Recent"
            
            # Email card
            is_selected = st.session_state.selected_email and st.session_state.selected_email['id'] == email['id']
            card_class = "email-card selected" if is_selected else "email-card"
            
            # Use button for click handling
            if st.button(
                f"{email['sender']}\n{email['subject']}", 
                key=f"email_{email['id']}",
                use_container_width=True,
                type="secondary" if not is_selected else "primary"
            ):
                st.session_state.selected_email = email
                st.session_state.chat_messages = []
                st.rerun()
            
            # Display badges and date below button
            if badge_html or date_str:
                cols = st.columns([3, 1])
                with cols[0]:
                    st.markdown(badge_html, unsafe_allow_html=True)
                with cols[1]:
                    st.markdown(f'<div class="email-date">{date_str}</div>', unsafe_allow_html=True)
            
            st.markdown("---")
    
    with col2:
        if st.session_state.selected_email:
            email = st.session_state.selected_email
            
            # Email Header
            st.markdown(f'<div class="email-detail-title">{email["subject"]}</div>', unsafe_allow_html=True)
            
            # Metadata
            col_meta1, col_meta2 = st.columns([3, 1])
            with col_meta1:
                st.markdown(f"**From:** {email['sender']}")
                try:
                    dt = datetime.fromisoformat(str(email['timestamp']).replace('Z', '+00:00'))
                    st.markdown(f"**Date:** {dt.strftime('%A, %B %d, %Y at %I:%M %p')}")
                except:
                    st.markdown(f"**Date:** {email['timestamp']}")
            
            with col_meta2:
                if email.get('category'):
                    category = email['category']
                    badge_class = {
                        'Important': 'badge-important',
                        'To-Do': 'badge-todo',
                        'Newsletter': 'badge-newsletter',
                        'Spam': 'badge-spam'
                    }.get(category, 'badge-default')
                    st.markdown(f'<span class="badge {badge_class}">{category}</span>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Email Body
            st.markdown(f'<div class="email-detail-body">{email["body"]}</div>', unsafe_allow_html=True)
            
            # Action Items
            if email.get('action_items') and len(email['action_items']) > 0:
                st.markdown("### ✅ Action Items")
                for item in email['action_items']:
                    task = item.get('task', 'No task description')
                    deadline = item.get('deadline', 'No deadline')
                    st.markdown(f"""
                    <div class="action-item">
                        <strong>Task:</strong> {task}<br>
                        <strong>Deadline:</strong> {deadline}
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # AI Assistant
            st.markdown("### 🤖 AI Assistant")
            
            # Display chat history
            for msg in st.session_state.chat_messages:
                if msg['role'] == 'user':
                    st.info(f"**You:** {msg['content']}")
                else:
                    st.success(f"**Agent:** {msg['content']}")
            
            # Chat input
            with st.form(key="chat_form", clear_on_submit=True):
                user_query = st.text_input("Ask about this email:", placeholder="Summarize this email, Draft a reply...")
                submit = st.form_submit_button("Send", use_container_width=True)
                
                if submit and user_query:
                    st.session_state.chat_messages.append({"role": "user", "content": user_query})
                    with st.spinner("Thinking..."):
                        response = chat_with_email(email['id'], user_query)
                        st.session_state.chat_messages.append({"role": "assistant", "content": response})
                    st.rerun()
        else:
            st.info("👈 Select an email from the inbox to view details")

elif page == "🧠 Prompt Config":
    st.title("🧠 Prompt Configuration")
    st.markdown("Configure how the AI agent processes your emails.")
    
    prompts = get_prompts()
    
    for prompt in prompts:
        with st.expander(f"**{prompt['name']}**", expanded=True):
            st.markdown(f"*{prompt['description']}*")
            new_template = st.text_area(
                "Template", 
                value=prompt['template'], 
                height=150, 
                key=f"prompt_{prompt['id']}"
            )
            if st.button("💾 Save Changes", key=f"save_{prompt['id']}"):
                if update_prompt(prompt['id'], {
                    "id": prompt['id'], 
                    "name": prompt['name'], 
                    "description": prompt['description'], 
                    "template": new_template
                }):
                    st.success("✓ Saved successfully!")
                else:
                    st.error("✗ Failed to save")

elif page == "📝 Drafts":
    st.title("📝 Email Drafts")
    st.info("Draft management feature coming soon...")
