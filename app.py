import streamlit as st
from _init_db import init_db
init_db()

st.set_page_config(
    page_title="Attendance Detection System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔥 CLEAN UI + SIDEBAR FIX
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0f172a;
    color: #e2e8f0;
}

/* Title */
h1 {
    color: #60a5fa;
    text-align: center;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 1.1rem;
    margin-bottom: 30px;
}

/* Box */
.box {
    background: #020617;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
}

/* 🔥 SIDEBAR IMPROVED */
section[data-testid="stSidebar"] {
    background: #020617;
    border-right: 1px solid #1e293b;
    width: 280px !important;
    min-width: 280px !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    font-size: 16px !important;
}

/* Sidebar items */
section[data-testid="stSidebar"] a {
    padding: 8px 12px !important;
    border-radius: 6px;
    margin-bottom: 6px;
}

/* Hover */
section[data-testid="stSidebar"] a:hover {
    background-color: #1e293b;
}

/* Active page */
section[data-testid="stSidebar"] [aria-current="page"] {
    background-color: #2563eb !important;
    color: white !important;
    border-radius: 6px;
}

/* Remove collapse arrow */
button[kind="header"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# 🔥 TITLE
st.markdown("<h1>🎓 Attendance Tracker</h1>", unsafe_allow_html=True)

st.markdown(
    "<div class='subtitle'>Smart Attendance System using Face Recognition</div>",
    unsafe_allow_html=True
)

# 🔥 SECTION 1
st.markdown("""
<div class='box'>
<b>🟢 System Status:</b> Online<br><br>
<b>🤖 AI Model:</b> Llama 3.3 70B<br><br>
<b>👁️ Recognition:</b> Facenet512<br><br>
<b>🗄️ Database:</b> SQLite
</div>
""", unsafe_allow_html=True)

# 🔥 SECTION 2
st.markdown("""
<div class='box'>
💡 <b>Getting Started</b><br><br>
Go to <b>Admin Dashboard</b> → Add Students → Register Face → Start marking attendance.
</div>
""", unsafe_allow_html=True)