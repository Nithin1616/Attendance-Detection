from ui import apply_ui
apply_ui()
import streamlit as st
import numpy as np
from PIL import Image
from datetime import date
from database import mark_attendance, get_today_attendance
from face_engine import recognize_face

st.set_page_config(page_title="Attendance")

st.title("📷 Attendance Marking")
st.write(f"Date: {date.today()}")

img = st.camera_input("Capture Face")

if img:
    image = np.array(Image.open(img).convert("RGB"))

    if st.button("Mark Attendance"):
        result = recognize_face(image)

        if result.get("recognized"):
            roll = result["roll_no"]
            res = mark_attendance(roll)

            if res["success"]:
                st.success(f"Marked for {roll}")
            else:
                st.warning(res["error"])
        else:
            st.error("Face not recognized")

st.markdown("---")

records = get_today_attendance()

if records:
    for r in records:
        st.write(f"{r[0]} ({r[1]}) - {r[2]}")
else:
    st.info("No attendance yet")
