from langchain.tools import tool
from attendance import (
    mark_attendance, get_attendance_percentage,
    get_today_attendance, get_all_students, get_all_subjects
)
from alerts import run_alert_check
from reports import daily_report, defaulter_report
from datetime import date


@tool
def tool_mark_attendance(roll_no: str, subject_id: int) -> str:
    """Mark attendance for a student by roll number and subject ID."""
    result = mark_attendance(roll_no, subject_id, method="agent")
    if result["success"]:
        return f"Attendance marked for {roll_no} at {result['time']}"
    return f"Failed: {result['error']}"


@tool
def tool_get_percentage(roll_no: str) -> str:
    """Get overall attendance percentage for a student by roll number."""
    pct = get_attendance_percentage(roll_no)
    return f"{roll_no} has {pct}% overall attendance."


@tool
def tool_get_today(subject_id: int) -> str:
    """Get today's attendance list for a given subject ID."""
    rows = get_today_attendance(subject_id)
    if not rows:
        return "No attendance recorded today for this subject."
    lines = [f"{r[0]} ({r[1]}) at {r[2]} via {r[3]}" for r in rows]
    return f"Present today ({len(rows)} students):\n" + "\n".join(lines)


@tool
def tool_run_alerts() -> str:
    """Check and trigger alerts for all students below the attendance threshold."""
    alerts = run_alert_check()
    if not alerts:
        return "All students are above the attendance threshold. No alerts needed."
    lines = [f"{a['student']} ({a['roll_no']}) - {a['subject']}: {a['percentage']}%" for a in alerts]
    return f"{len(alerts)} students below threshold:\n" + "\n".join(lines)


@tool
def tool_defaulter_list() -> str:
    """Get the full list of defaulter students below 75% attendance."""
    df = defaulter_report(75)
    if df.empty:
        return "No defaulters found. All students are above 75%."
    return df.to_string(index=False)


@tool
def tool_list_students() -> str:
    """List all registered students."""
    students = get_all_students()
    if not students:
        return "No students registered yet."
    return "\n".join([f"{s[2]} - {s[1]} ({s[3] or 'no email'})" for s in students])


@tool
def tool_list_subjects() -> str:
    """List all subjects."""
    subjects = get_all_subjects()
    if not subjects:
        return "No subjects added yet."
    return "\n".join([f"ID {s[0]}: {s[1]} (Teacher: {s[2] or 'N/A'})" for s in subjects])


@tool
def tool_daily_report() -> str:
    """Get today's full attendance report."""
    df = daily_report(str(date.today()))
    if df.empty:
        return "No attendance recorded today."
    return df.to_string(index=False)