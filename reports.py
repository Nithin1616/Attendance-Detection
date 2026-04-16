
import pandas as pd
import sqlite3
import os
from datetime import date
from dotenv import load_dotenv
load_dotenv()

DB_PATH = os.getenv("DB_PATH", "attendance.db")


def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def daily_report(report_date: str = None):
    if not report_date:
        report_date = str(date.today())
    conn = get_conn()
    df = pd.read_sql_query("""
        SELECT s.name AS Student, s.roll_no AS RollNo,
               a.time AS Time, a.method AS Method,
               a.status AS Status,
               ROUND(a.confidence * 100, 1) AS Confidence_Pct
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        WHERE a.date = ?
        ORDER BY s.name
    """, conn, params=(report_date,))
    conn.close()
    return df


def monthly_report(year: int, month: int):
    conn = get_conn()
    df = pd.read_sql_query("""
        SELECT s.name AS Student, s.roll_no AS RollNo,
               COUNT(*) AS DaysPresent
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        WHERE strftime('%Y', a.date) = ?
          AND strftime('%m', a.date) = ?
          AND a.status = 'present'
        GROUP BY s.roll_no
        ORDER BY s.name
    """, conn, params=(str(year), str(month).zfill(2)))
    conn.close()
    return df


def defaulter_report(threshold: int = 75):
    conn = get_conn()
    total_classes_row = conn.execute("SELECT COUNT(*) FROM classes").fetchone()
    total_classes = total_classes_row[0] if total_classes_row else 0

    if total_classes == 0:
        conn.close()
        return pd.DataFrame(columns=["Student", "RollNo", "Email", "Present", "Total", "Percentage"])

    df = pd.read_sql_query("""
        SELECT s.name AS Student, s.roll_no AS RollNo, s.email AS Email,
               COUNT(a.id) AS Present
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id AND a.status='present'
        GROUP BY s.id
    """, conn)
    conn.close()

    df["Total"] = total_classes
    df["Percentage"] = (df["Present"] / total_classes * 100).round(2)
    df = df[df["Percentage"] < threshold].sort_values("Percentage")
    return df


def overall_summary():
    conn = get_conn()
    total_classes_row = conn.execute("SELECT COUNT(*) FROM classes").fetchone()
    total_classes = total_classes_row[0] if total_classes_row else 0

    df = pd.read_sql_query("""
        SELECT s.name AS Student, s.roll_no AS RollNo,
               COUNT(a.id) AS Present
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id AND a.status='present'
        GROUP BY s.id
        ORDER BY s.name
    """, conn)
    conn.close()

    df["Total"] = total_classes
    df["Percentage"] = (df["Present"] / total_classes * 100).round(2) if total_classes > 0 else 0
    return df


def export_to_csv(df, filename: str) -> str:
    path = f"{filename}.csv"
    df.to_csv(path, index=False)
    return path