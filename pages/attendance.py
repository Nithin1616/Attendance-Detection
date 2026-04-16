import sqlite3
from datetime import date, datetime

DB_PATH = "attendance.db"

def get_conn():
return sqlite3.connect(DB_PATH, check_same_thread=False)

# ------------------ MARK ATTENDANCE ------------------

def mark_attendance(roll_no, method="face", confidence=None):
conn = get_conn()
c = conn.cursor()

```
# Get student ID
c.execute("SELECT id FROM students WHERE roll_no=?", (roll_no,))
row = c.fetchone()

if not row:
    conn.close()
    return {"success": False, "error": "Student not found"}

student_id = row[0]
today = str(date.today())
now = datetime.now().strftime("%H:%M:%S")

# ✅ FIX: check only THIS student for TODAY
c.execute("""
    SELECT id FROM attendance
    WHERE student_id=? AND date=?
""", (student_id, today))

if c.fetchone():
    conn.close()
    return {"success": False, "error": "Already marked"}

# ✅ INSERT attendance (no subject_id now)
c.execute("""
    INSERT INTO attendance
    (student_id, date, time, method, status, confidence)
    VALUES (?, ?, ?, ?, ?, ?)
""", (student_id, today, now, method, "present", confidence))

conn.commit()
conn.close()

return {"success": True, "time": now}
```

# ------------------ TODAY ATTENDANCE ------------------

def get_today_attendance():
conn = get_conn()
c = conn.cursor()
today = str(date.today())

```
c.execute("""
    SELECT s.name, s.roll_no, a.time, a.method, a.confidence
    FROM attendance a
    JOIN students s ON a.student_id = s.id
    WHERE a.date=?
""", (today,))

rows = c.fetchall()
conn.close()
return rows
```

# ------------------ GET ALL STUDENTS ------------------

def get_all_students():
conn = get_conn()
c = conn.cursor()

```
c.execute("SELECT id, name, roll_no, email FROM students")
rows = c.fetchall()

conn.close()
return rows
```
