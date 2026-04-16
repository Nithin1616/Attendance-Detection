import streamlit as st
import numpy as np
from PIL import Image
from attendance import add_student
from database import get_all_students
from face_engine import register_face

st.set_page_config(page_title="Registration")

st.title("📝 Student Registration")

students = get_all_students()

if students:
    import pandas as pd
    df = pd.DataFrame(students, columns=["ID","Name","Roll","Email"])
    st.dataframe(df)

st.markdown("---")

name = st.text_input("Name")
roll = st.text_input("Roll")
email = st.text_input("Email")
img = st.file_uploader("Upload Face")

if st.button("Add Student"):
    if name and roll:
        res = add_student(name, roll, email)

        if res["success"]:
            if img:
                img_arr = np.array(Image.open(img))
                register_face(roll, img_arr)

            st.success("Student added")
        else:
            st.error(res["error"])
    else:
        st.warning("Enter name and roll")
