from ui import apply_ui
apply_ui()

import streamlit as st
import numpy as np
from PIL import Image
from database import add_student, get_all_students, delete_student
from face_engine import register_face, delete_face, face_registered


def render():
    st.markdown("""
    <div style='margin-bottom:1.5rem;'>
        <h2 style='font-family: Space Grotesk, sans-serif; font-size:1.8rem;
                   font-weight:700; color:#f1f5f9; margin:0;'>
                 Student Registration
        </h2>
        <p style='color:#64748b; margin:4px 0 0 0; font-size:0.9rem;'>
            Add new students and register their face for automatic attendance.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_add, tab_list = st.tabs(["➕  Add Student", "📜  All Students"])

    # ── ADD STUDENT ─────────────────────────────────────────
    with tab_add:
        st.markdown("<br>", unsafe_allow_html=True)

        with st.form("add_student_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            name    = c1.text_input("Full Name")
            roll_no = c2.text_input("Roll Number")
            email   = c1.text_input("Email Address")
            phone   = c2.text_input("Phone Number (optional)")

            upload = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])

            # ✅ Updated
            submitted = st.form_submit_button("Register Student", width="stretch")

        if submitted:
            if not name or not roll_no or not email:
                st.error("Fill all required fields")
            else:
                result = add_student(name, roll_no.upper(), email, phone)

                if result["success"]:
                    if upload:
                        img = np.array(Image.open(upload).convert("RGB"))
                        face_result = register_face(roll_no.upper(), img)

                        if face_result["success"]:
                            st.success("Student registered with face ✅")
                        else:
                            st.warning("Student added but face failed")
                    else:
                        st.success("Student registered (no face)")
                else:
                    st.error(result["error"])

    # ── STUDENT LIST ─────────────────────────────────────────
    with tab_list:
        students = get_all_students()

        if not students:
            st.info("No students yet")
        else:
            for s in students:
                sid, name, roll, email, phone = s

                col1, col2, col3 = st.columns([3,1,1])
                col1.write(f"{name} ({roll})")

                if face_registered(roll):
                    col2.write("👁 Face")
                else:
                    col2.write("No Face")

                # ✅ Updated
                if col3.button("Delete", key=roll, width="content"):
                    delete_student(roll)
                    delete_face(roll)
                    st.rerun()

            st.markdown("---")

            # UPDATE FACE
            st.subheader("Update Face")

            upd_roll = st.text_input("Roll No")
            upd_photo = st.file_uploader("New Photo", type=["jpg","jpeg","png"])

            # ✅ Updated
            if st.button("Update Face", width="stretch"):
                if upd_roll and upd_photo:
                    img = np.array(Image.open(upd_photo).convert("RGB"))
                    res = register_face(upd_roll.upper(), img)

                    if res["success"]:
                        st.success("Face updated ✅")
                    else:
                        st.error(res["error"])
                else:
                    st.warning("Provide roll no and photo")


# IMPORTANT: call function
render()
