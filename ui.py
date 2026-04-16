import streamlit as st

def apply_ui():
    st.markdown("""
    <style>

    /* Clean base */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0f172a;
        color: #e2e8f0;
    }

    /* Headings */
    h1, h2, h3 {
        color: #60a5fa;
        font-weight: 600;
    }

    /* 🔥 BIGGER SIDEBAR */
    section[data-testid="stSidebar"] {
        background: #020617;
        border-right: 1px solid #1e293b;
        width: 320px !important;
        min-width: 320px !important;
        position: relative;
    }

    /* Sidebar text bigger */
    section[data-testid="stSidebar"] * {
        font-size: 18px !important;
    }

    /* Sidebar spacing */
    section[data-testid="stSidebar"] li {
        margin-bottom: 14px !important;
    }

    /* Sidebar item style */
    section[data-testid="stSidebar"] a {
        padding: 10px !important;
        border-radius: 8px;
        display: block;
    }

    /* Hover */
    section[data-testid="stSidebar"] a:hover {
        background-color: #1e293b;
    }

    /* Active page highlight */
    section[data-testid="stSidebar"] [aria-current="page"] {
        background-color: #2563eb !important;
        color: white !important;
        border-radius: 8px;
    }

    /* 🔥 FIX SIDEBAR ARROW POSITION */
    section[data-testid="stSidebar"] button {
        position: absolute !important;
        right: 10px !important;
        top: 10px !important;
    }

    /* 👉 OPTIONAL: Hide arrow completely (uncomment if needed) */
    /*
    button[kind="header"] {
        display: none !important;
    }
    */

    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        font-size: 16px;
        padding: 8px 16px;
    }

    /* Cards */
    .card {
        background: #020617;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #1e293b;
        margin-bottom: 10px;
    }

    /* Buttons */
    .stButton button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        padding: 10px;
        border: none;
    }

    .stButton button:hover {
        background-color: #1d4ed8;
    }

    /* Inputs */
    .stTextInput, .stSelectbox, .stFileUploader {
        border-radius: 8px;
    }

    </style>
    """, unsafe_allow_html=True)