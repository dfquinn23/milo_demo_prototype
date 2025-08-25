# app_streamlit.py

import os
import requests
import streamlit as st

st.set_page_config(page_title="Milo Demo", page_icon="🤖", layout="wide")

st.title("Milo Demo — Round-Trip Stub")
st.caption("Streamlit → FastAPI → (stub agents) → Streamlit")

# Configure backend URL (default is your local FastAPI server)
DEFAULT_BACKEND = "http://localhost:8000"
backend_url = os.getenv("BACKEND_URL", DEFAULT_BACKEND)

with st.sidebar:
    st.subheader("Settings")
    backend_url = st.text_input(
        "Backend URL", value=backend_url, help="FastAPI base URL")
    session_id = st.text_input("Session ID (optional)")
    st.markdown("""
    **How it works**
    1. Type a prompt
    2. Click **Run**
    3. Streamlit calls FastAPI `/generate`
    4. FastAPI runs a stubbed crew and returns a response
    """)

prompt = st.text_area(
    "Enter your prompt",
    height=160,
    placeholder="e.g., Draft an RFP answer about our cybersecurity controls…",
)

col_run, col_clear = st.columns([1, 1])

if col_run.button("Run", type="primary"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Contacting backend…"):
            try:
                resp = requests.post(
                    f"{backend_url}/generate",
                    json={"prompt": prompt, "session_id": session_id or None},
                    timeout=60,
                )
                resp.raise_for_status()
                data = resp.json()
                st.success("Response received")

                st.subheader("Answer")
                st.write(data.get("answer", ""))

                with st.expander("Details"):
                    st.json({
                        "model": data.get("model"),
                        "latency_ms": data.get("latency_ms"),
                        "review_flags": data.get("review_flags", []),
                        "citations": data.get("citations", []),
                    })
            except requests.RequestException as e:
                st.error(f"Request failed: {e}")

if col_clear.button("Clear"):
    st.experimental_rerun()
