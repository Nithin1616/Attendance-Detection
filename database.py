from datetime import date, datetime
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "attendance.db")


def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


# ─────────────────── STUDENTS ───────────────────

def add_student(name: str, roll_no: str, email: str, phone: str = ""):
    conn = get_conn()
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO students (name, roll_no, email, phone) VALUES (?, ?, ?, ?)",
            (name, roll_no, email, phone)
        )
        conn.commit()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        conn.close()


def get_all_students():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, name, roll_no, email, phone FROM students ORDER BY name")
    rows = c.fetchall()
    conn.close()
    return rows


def delete_student(roll_no: str):
    conn = get_conn()
    c = conn.cursor()
    try:
        c.execute("SELECT id FROM students WHERE roll_no=?", (roll_no,))
        row = c.fetchone()
        if not row:
            return {"success": False, "error": "Student not found"}
        student_id = row[0]
        c.execute("DELETE FROM attendance WHERE student_id=?", (student_id,))
        c.execute("DELETE FROM students WHERE roll_no=?", (roll_no,))
        conn.commit()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        conn.close()


# ─────────────────── CLASSES (sessions) ───────────────────

def mark_class_conducted(session_date: str = None):
    """Record that a class was held on a given date."""
    conn = get_conn()
    c = conn.cursor()
    if not session_date:
        session_date = str(date.today())
    c.execute("SELECT id FROM classes WHERE date=?", (session_date,))
    if not c.fetchone():
        c.execute("INSERT INTO classes (date) VALUES (?)", (session_date,))
        conn.commit()
    conn.close()


def get_total_classes():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM classes")
    count = c.fetchone()[0]
    conn.close()
    return count


# ─────────────────── ATTENDANCE ───────────────────

def mark_attendance(roll_no: str, method: str = "face", confidence: float = None, session_date: str = None):
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT id FROM students WHERE roll_no=?", (roll_no,))
    row = c.fetchone()
    if not row:
        conn.close()
        return {"success": False, "error": "Student not found"}

    student_id = row[0]
    today = session_date or str(date.today())
    now = datetime.now().strftime("%H:%M:%S")

   # mark_class_conducted(today)

    c.execute(
        "SELECT id FROM attendance WHERE student_id=? AND date=?",
        (student_id, today)
    )
    if c.fetchone():
        conn.close()
        return {"success": False, "error": "Already marked today"}

    c.execute("""
        INSERT INTO attendance (student_id, date, time, method, status, confidence)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (student_id, today, now, method, "present", confidence))

    conn.commit()
    conn.close()
    return {"success": True, "time": now}


def get_today_attendance():
    conn = get_conn()
    c = conn.cursor()
    today = str(date.today())
    c.execute("""
        SELECT s.name, s.roll_no, a.time, a.method, a.confidence
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        WHERE a.date=? AND a.status='present'
        ORDER BY a.time
    """, (today,))
    rows = c.fetchall()
    conn.close()
    return rows


def get_student_attendance(roll_no: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT s.name, a.date, a.time, a.method, a.status, a.confidence
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        WHERE s.roll_no=?
        ORDER BY a.date DESC
    """, (roll_no,))
    rows = c.fetchall()
    conn.close()
    return rows


def get_attendance_percentage(roll_no: str) -> float:
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT id FROM students WHERE roll_no=?", (roll_no,))
    row = c.fetchone()
    if not row:
        conn.close()
        return 0.0

    student_id = row[0]

    c.execute(
        "SELECT COUNT(*) FROM attendance WHERE student_id=? AND status='present'",
        (student_id,)
    )
    present = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM classes")
    total = c.fetchone()[0]

    conn.close()
    if total == 0:
        return 0.0
    return round((present / total) * 100, 2)


def get_all_attendance_summary():
    """Return attendance percentage for every student."""
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM classes")
    total_classes = c.fetchone()[0]

    c.execute("""
        SELECT s.id, s.name, s.roll_no, s.email, s.phone,
               COUNT(a.id) AS present_count
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id AND a.status='present'
        GROUP BY s.id
        ORDER BY s.name
    """)
    rows = c.fetchall()
    conn.close()

    result = []
    for r in rows:
        pct = round((r[5] / total_classes) * 100, 2) if total_classes > 0 else 0.0
        result.append({
            "id": r[0], "name": r[1], "roll_no": r[2],
            "email": r[3], "phone": r[4],
            "present": r[5], "total": total_classes, "percentage": pct
        })
    return result
