import smtplib
import sqlite3
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()

from database import get_all_attendance_summary

DB_PATH = os.getenv("DB_PATH", "attendance.db")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def get_alert_threshold() -> int:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT threshold FROM alert_config WHERE id=1")
    row = c.fetchone()
    conn.close()
    return row[0] if row else 75


def set_alert_threshold(threshold: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE alert_config SET threshold=? WHERE id=1", (threshold,))
    conn.commit()
    conn.close()


def send_email_alert(to_email: str, student_name: str, percentage: float, threshold: int) -> dict:
    """Send a low-attendance warning email to a student."""
    if not SMTP_EMAIL or not SMTP_PASSWORD:
        print(f"[ALERT LOG - no SMTP] {student_name} | {percentage:.1f}% (threshold: {threshold}%)")
        return {"sent": False, "reason": "SMTP not configured"}

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"⚠️ Low Attendance Warning — {percentage:.1f}%"
        msg["From"] = SMTP_EMAIL
        msg["To"] = to_email

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background: #f4f6f8; padding: 30px;">
          <div style="max-width: 520px; margin: auto; background: white; border-radius: 12px;
                      box-shadow: 0 4px 20px rgba(0,0,0,0.08); overflow: hidden;">
            <div style="background: linear-gradient(135deg, #0f1f3d, #1a3a6b); padding: 30px; text-align: center;">
              <h1 style="color: white; margin: 0; font-size: 1.6rem;">🎓 AttendAI</h1>
              <p style="color: #93c5fd; margin: 6px 0 0 0; font-size: 0.9rem;">Attendance Alert System</p>
            </div>
            <div style="padding: 32px;">
              <p style="font-size: 1rem; color: #374151;">Dear <strong>{student_name}</strong>,</p>
              <p style="color: #374151;">Your current attendance has dropped below the required threshold:</p>
              <div style="background: #fff3cd; border-left: 4px solid #f59e0b; border-radius: 8px;
                          padding: 16px 20px; margin: 20px 0;">
                <p style="margin: 0; font-size: 1.5rem; font-weight: bold; color: #b45309;">
                  {percentage:.1f}% <span style="font-size: 0.9rem; color: #92400e;">/ {threshold}% required</span>
                </p>
              </div>
              <p style="color: #374151;">Please ensure you attend upcoming classes to improve your attendance record.
              Falling below <strong>{threshold}%</strong> may result in academic penalties.</p>
              <p style="color: #6b7280; font-size: 0.85rem; margin-top: 24px;">
                This is an automated alert from the AttendAI system. Please contact your administrator if you
                believe this is incorrect.
              </p>
            </div>
            <div style="background: #f9fafb; padding: 16px; text-align: center; border-top: 1px solid #e5e7eb;">
              <p style="color: #9ca3af; font-size: 0.8rem; margin: 0;">AttendAI — Automated Attendance System</p>
            </div>
          </div>
        </body>
        </html>
        """

        plain_body = (
            f"Dear {student_name},\n\n"
            f"Your attendance has fallen to {percentage:.1f}% which is below the {threshold}% requirement.\n"
            f"Please attend upcoming classes regularly.\n\n"
            f"— AttendAI System"
        )

        msg.attach(MIMEText(plain_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, to_email, msg.as_string())

        print(f"[EMAIL SENT] → {to_email} | {student_name} | {percentage:.1f}%")
        return {"sent": True}

    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return {"sent": False, "reason": str(e)}


def run_alert_check(custom_threshold: int = None) -> list:
    """
    Check all students and send alerts to those below the threshold.
    Returns a list of alert dicts for display in the UI.
    """
    threshold = custom_threshold or get_alert_threshold()
    summary = get_all_attendance_summary()
    triggered = []

    for student in summary:
        pct = student["percentage"]
        # Only alert if they have attended at least once (avoid alerting brand new students)
        if student["total"] > 0 and pct < threshold:
            triggered.append({
                "name": student["name"],
                "roll_no": student["roll_no"],
                "email": student["email"] or "",
                "percentage": pct,
                "threshold": threshold,
                "email_result": None,
            })
            if student["email"]:
                result = send_email_alert(
                    student["email"], student["name"], pct, threshold
                )
                triggered[-1]["email_result"] = result

    return triggered


def send_single_alert(roll_no: str) -> dict:
    """Send alert to a specific student manually."""
    from database import get_attendance_percentage, get_all_students
    threshold = get_alert_threshold()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, email FROM students WHERE roll_no=?", (roll_no,))
    row = c.fetchone()
    conn.close()

    if not row:
        return {"success": False, "error": "Student not found"}

    name, email = row
    from database import get_attendance_percentage
    pct = get_attendance_percentage(roll_no)

    if not email:
        return {"success": False, "error": "No email on record for this student"}

    result = send_email_alert(email, name, pct, threshold)
    return {"success": result["sent"], "percentage": pct, **result}