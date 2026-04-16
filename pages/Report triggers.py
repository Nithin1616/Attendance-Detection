from ui import apply_ui
apply_ui()

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from reports import daily_report, monthly_report, defaulter_report, overall_summary, export_to_csv
from alerts import run_alert_check, send_single_alert, get_alert_threshold, set_alert_threshold
from database import get_all_attendance_summary


def render():
    st.markdown("""
    <div style='margin-bottom:1.5rem;'>
        <h2 style='font-family: Space Grotesk, sans-serif; font-size:1.8rem;
                   font-weight:700; color:#f1f5f9; margin:0;'>
            📊 Reports &amp; Triggers
        </h2>
        <p style='color:#64748b; margin:4px 0 0 0; font-size:0.9rem;'>
            Generate reports, visualize data, and send low-attendance alerts to students.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_overview, tab_daily, tab_monthly, tab_defaulters, tab_alerts = st.tabs([
        "📈  Overview", "📅  Daily", "🗓️  Monthly", "⚠️  Defaulters", "🔔  Alert Triggers"
    ])

    # ── OVERVIEW ─────────────────────────────────────────
    with tab_overview:
        st.markdown("<br>", unsafe_allow_html=True)
        summary = get_all_attendance_summary()

        if not summary:
            st.info("No data available yet.")
            return

        df = pd.DataFrame(summary)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Students", len(df))
        m2.metric("Above 75%", int((df["percentage"] >= 75).sum()))
        m3.metric("Below 75%", int((df["percentage"] < 75).sum()))
        m4.metric("Class Average", f"{df['percentage'].mean():.1f}%")

        c1, c2 = st.columns(2)

        with c1:
            fig_pie = go.Figure(data=[go.Pie(
                labels=["Above 75%", "60–75%", "Below 60%"],
                values=[
                    (df["percentage"] >= 75).sum(),
                    ((df["percentage"] >= 60) & (df["percentage"] < 75)).sum(),
                    (df["percentage"] < 60).sum(),
                ],
                hole=0.5
            )])
            st.plotly_chart(fig_pie, width="stretch")  # ✅ updated

        with c2:
            fig_bar = px.bar(df, x="percentage", y="name", orientation="h")
            st.plotly_chart(fig_bar, width="stretch")  # ✅ updated

        st.dataframe(df, width="stretch")  # ✅ updated

        csv = df.to_csv(index=False).encode()
        st.download_button("Download CSV", csv, "report.csv")

    # ── DAILY ─────────────────────────────────────────
    with tab_daily:
        selected_date = st.date_input("Select Date", value=date.today())
        df_daily = daily_report(str(selected_date))

        if not df_daily.empty:
            st.dataframe(df_daily, width="stretch")  # ✅ updated
            csv = df_daily.to_csv(index=False).encode()
            st.download_button("Download Daily CSV", csv, "daily.csv")

    # ── MONTHLY ────────────────────────────────────────
    with tab_monthly:
        year = st.number_input("Year", value=date.today().year)
        month = st.number_input("Month", value=date.today().month)

        df_monthly = monthly_report(int(year), int(month))

        if not df_monthly.empty:
            st.dataframe(df_monthly, width="stretch")  # ✅ updated
            csv = df_monthly.to_csv(index=False).encode()
            st.download_button("Download Monthly CSV", csv, "monthly.csv")

    # ── DEFAULTERS ─────────────────────────────────────
    with tab_defaulters:
        threshold = st.slider("Threshold", 50, 90, 75)

        df_def = defaulter_report(threshold)

        if not df_def.empty:
            st.dataframe(df_def, width="stretch")  # ✅ updated
            csv = df_def.to_csv(index=False).encode()
            st.download_button("Download Defaulters CSV", csv, "defaulters.csv")

    # ── ALERTS ─────────────────────────────────────────
    with tab_alerts:

        if st.button("🚨 Run Alert Check", width="stretch"):  # ✅ updated
            alerts = run_alert_check()
            st.write(alerts)

        roll = st.text_input("Student Roll")

        if st.button("Send Alert", width="content"):  # ✅ updated
            if roll:
                result = send_single_alert(roll)
                st.write(result)


render()