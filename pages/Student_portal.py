from ui import apply_ui
apply_ui()

import streamlit as st
from database import get_student_attendance, get_attendance_percentage, get_all_students, get_total_classes


def render():
    st.markdown("""
    <div style='margin-bottom:1.5rem;'>
        <h2 style='font-family: Space Grotesk, sans-serif; font-size:1.8rem;
                   font-weight:700; color:#f1f5f9; margin:0;'>
               Student Portal
        </h2>
        <p style='color:#64748b; margin:4px 0 0 0; font-size:0.9rem;'>
            Look up your attendance record and track your progress.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Lookup ─────────────────────────
    col1, col2 = st.columns([2, 1])
    with col1:
        roll_input = st.text_input(
            "Enter your Roll Number",
            placeholder="e.g. CS2023001",
            label_visibility="visible"
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)

        # ✅ UPDATED
        search = st.button("🔍 Search", width="stretch")

    if not roll_input:
        st.markdown("<br>", unsafe_allow_html=True)
        students = get_all_students()
        total_cls = get_total_classes()

        if students and total_cls > 0:
            st.markdown("### Class Overview")
            for s in students:
                pct = get_attendance_percentage(s[2])
                color = "#10b981" if pct >= 75 else "#f59e0b" if pct >= 60 else "#ef4444"
                bar_w = int(pct)

                st.markdown(f"""
                <div style='background:#111827; padding:12px; border-radius:10px; margin-bottom:8px;'>
                    <b>{s[1]}</b> ({s[2]})<br>
                    <div style='background:#1e293b; height:8px; border-radius:5px; margin-top:5px;'>
                        <div style='width:{bar_w}%; background:{color}; height:8px; border-radius:5px;'></div>
                    </div>
                    <small style='color:{color}'>{pct:.1f}%</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Enter a roll number above to view attendance details.")
        return

    # ── Individual Student ─────────────
    roll_no = roll_input.strip().upper()
    records = get_student_attendance(roll_no)
    pct     = get_attendance_percentage(roll_no)

    if not records and pct == 0.0:
        students = get_all_students()
        exists = any(s[2] == roll_no for s in students)
        if not exists:
            st.error(f"No student found with roll number {roll_no}")
            return

    color = "#10b981" if pct >= 75 else "#f59e0b" if pct >= 60 else "#ef4444"

    st.markdown(f"### {roll_no} — {pct:.1f}%")

    st.progress(min(pct / 100, 1.0))

    # ── History ─────────────
    if records:
        st.dataframe(records, width="stretch")  # ✅ UPDATED
    else:
        st.info("No attendance records found.")


render()