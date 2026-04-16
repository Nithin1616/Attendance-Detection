from ui import apply_ui
apply_ui()
import streamlit as st
import numpy as np
from PIL import Image
from datetime import date
from database import mark_attendance, get_today_attendance, get_all_students

# 🔥 MATCH SAME UI STYLE AS HOME
st.markdown("""
<style>

/* Sidebar bigger text */
section[data-testid="stSidebar"] * {
    font-size: 18px !important;
}

/* Tabs styling */
.stTabs [data-baseweb="tab"] {
    font-size: 18px;
    padding: 10px 20px;
}

/* Card style */
.card {
    background: #111827;
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


def render():

    # 🔥 HEADER (same style as home)
    st.markdown("""
    <div style='margin-bottom:20px;'>
        <h1 style='font-size:2.5rem; color:#63b3ed;'> Attendance Detection</h1>
        <p style='color:#94a3b8;'>Mark attendance using AI face recognition or manual entry.</p>
    </div>
    """, unsafe_allow_html=True)

    # 🔥 DATE CARD
    today = str(date.today())
    st.markdown(f"""
    <div class="card">
        📅 <b>Today:</b> {today}
    </div>
    """, unsafe_allow_html=True)

    # 🔥 TABS
    tab_face, tab_manual, tab_today = st.tabs([
        " Face Recognition", "✏️ Manual Entry", "📋 Today's Log"
    ])

    # ================= FACE =================
    with tab_face:

        st.markdown("""
        <div class="card">
            <h4> Upload or Capture Photo</h4>
            <p style='color:#94a3b8;'>Upload image or use camera for automatic recognition.</p>
        </div>
        """, unsafe_allow_html=True)

        img_source = st.radio(
            "Image source", ["Upload Photo", "Camera"],
            horizontal=True, label_visibility="collapsed"
        )

        captured_img = None

        if img_source == "Upload Photo":
            uploaded = st.file_uploader("Upload", type=["jpg","jpeg","png"])
            if uploaded:
                captured_img = np.array(Image.open(uploaded).convert("RGB"))
                st.image(captured_img, width=250)

        else:
            camera_img = st.camera_input("Camera")
            if camera_img:
                captured_img = np.array(Image.open(camera_img).convert("RGB"))

        if captured_img is not None:
            if st.button(" Recognize & Mark Attendance", use_container_width=True):

                with st.spinner("Processing..."):
                    from face_engine import recognize_face
                    result = recognize_face(captured_img)

                if result.get("recognized"):
                    roll = result["roll_no"]
                    conf = result["confidence"]

                    res = mark_attendance(roll, method="face", confidence=conf)

                    if res["success"]:
                        st.success(f"✅ Attendance marked for {roll}")
                    else:
                        st.warning(res["error"])

                else:
                    st.error("❌ Face not recognized")

    # ================= MANUAL =================
    with tab_manual:

        students = get_all_students()

        if not students:
            st.info("No students found")
        else:
            with st.form("manual"):
                options = {f"{s[1]} ({s[2]})": s[2] for s in students}

                selected = st.selectbox("Select Student", list(options.keys()))
                submitted = st.form_submit_button("Mark Attendance")

            if submitted:
                roll = options[selected]
                res = mark_attendance(roll, method="manual")

                if res["success"]:
                    st.success("Attendance marked ✅")
                else:
                    st.warning(res["error"])

    # ================= LOG =================
    with tab_today:

        records = get_today_attendance()

        if records:
            for r in records:
                st.markdown(f"""
                <div class="card">
                    <b>{r[0]}</b> ({r[1]})<br>
                    ⏰ {r[2]} | ⚙️ {r[3]} | 🎯 {round(r[4]*100,1) if r[4] else '--'}%
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No attendance today")


render()