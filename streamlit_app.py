import streamlit as st
import json
from gmail_client import get_gmail_service, fetch_emails
from email_parser import parse_email
from ai_agent import analyze_email
from draft_reply import create_draft

st.set_page_config(
    page_title="Email Intelligence Agent",
    page_icon="📧",
    layout="wide"
)

st.title("📧 Email Intelligence Agent")
st.markdown("*AI-powered email analysis and smart reply generation*")
st.divider()

with st.sidebar:
    st.header("⚙️ Settings")
    num_emails = st.slider("Number of emails to fetch", 1, 10, 3)
    st.divider()
    st.markdown("**Built with:**")
    st.markdown("- 🔴 Gmail API")
    st.markdown("- 🤖 Gemma LLM")
    st.markdown("- 🔀 OpenRouter")
    st.markdown("- 🎈 Streamlit")

# ✅ Store emails in session state so page doesn't reset
if "emails_data" not in st.session_state:
    st.session_state.emails_data = []

if "service" not in st.session_state:
    st.session_state.service = None

if "draft_status" not in st.session_state:
    st.session_state.draft_status = {}

if st.button("🔄 Fetch & Analyze Emails", type="primary", use_container_width=True):
    with st.spinner("Connecting to Gmail..."):
        st.session_state.service = get_gmail_service()

    with st.spinner(f"Fetching {num_emails} emails..."):
        raw_emails = fetch_emails(st.session_state.service, max_results=num_emails)

    emails_data = []
    for i, raw in enumerate(raw_emails):
        email = parse_email(raw)
        with st.spinner(f"🤖 Analyzing email {i+1}..."):
            try:
                analysis = analyze_email(email)
                emails_data.append({"email": email, "analysis": analysis})
            except Exception as e:
                st.error(f"Failed to analyze email {i+1}: {e}")

    st.session_state.emails_data = emails_data
    st.session_state.draft_status = {}
    st.success(f"✅ Analyzed {len(emails_data)} emails!")

# ✅ Display emails from session state
if st.session_state.emails_data:
    st.divider()
    for i, item in enumerate(st.session_state.emails_data):
        email = item["email"]
        analysis = item["analysis"]

        priority_color = {
            "high": "🔴",
            "medium": "🟡",
            "low": "🟢"
        }.get(analysis['priority'].lower(), "⚪")

        with st.expander(
            f"{priority_color} {email['subject']} — {email['sender'][:40]}",
            expanded=(i == 0)
        ):
            col1, col2, col3 = st.columns(3)
            col1.metric("Priority", analysis['priority'].upper())
            col2.metric("Sentiment", analysis['sentiment'].capitalize())
            col3.metric("Category", analysis['category'].capitalize())

            st.markdown("**📝 AI Summary:**")
            st.info(analysis['summary'])

            st.markdown("**💬 Suggested Reply:**")
            reply_text = st.text_area(
                "Edit reply before saving:",
                value=analysis['suggested_reply'],
                height=120,
                key=f"reply_{i}"
            )

            if st.button(f"📨 Save as Draft in Gmail", key=f"draft_{i}"):
                try:
                    create_draft(
                        st.session_state.service,
                        email['sender'],
                        email['subject'],
                        reply_text
                    )
                    st.session_state.draft_status[i] = "success"
                except Exception as e:
                    st.session_state.draft_status[i] = f"error: {e}"

            # Show status without refreshing
            if i in st.session_state.draft_status:
                status = st.session_state.draft_status[i]
                if status == "success":
                    st.success("✅ Draft saved to Gmail!")
                else:
                    st.error(status)

        st.divider()