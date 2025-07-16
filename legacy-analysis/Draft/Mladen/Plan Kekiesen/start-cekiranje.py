#!/usr/bin/env python3
import os
import sqlite3
import uuid
from datetime import datetime

DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "db", "report.db")

def get_pending_row(cur, rn):
    """
    Fetch the first row for RN=rn where STATUS is NULL or empty,
    ordered by START ascending.
    Returns (RN, KPL, START, WC) or None.
    """
    query = """
    SELECT RN, KPL, START, WC
      FROM report
     WHERE RN = ?
       AND (STATUS IS NULL OR STATUS = '')
     ORDER BY START ASC
     LIMIT 1
    """
    cur.execute(query, (rn,))
    return cur.fetchone()

def ensure_operacije_table(cur):
    # Create table if missing, with all necessary columns
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Operacije (
      id             INTEGER PRIMARY KEY AUTOINCREMENT,
      "ID-OP"        TEXT UNIQUE,
      WC             TEXT,
      RN             TEXT,
      "Start-Time"   TEXT,
      "Start-Date"   TEXT,
      "Stop-Time"    TEXT,
      "Stop-Date"    TEXT,
      STATUS         TEXT
    );
    """)
    # Add any columns that might be missing
    cur.execute('PRAGMA table_info(Operacije);')
    existing = {row[1] for row in cur.fetchall()}
    for col_def in [
        ('"ID-OP"',      'TEXT UNIQUE'),
        ('WC',           'TEXT'),
        ('RN',           'TEXT'),
        ('"Start-Time"', 'TEXT'),
        ('"Start-Date"', 'TEXT'),
        ('"Stop-Time"',  'TEXT'),
        ('"Stop-Date"',  'TEXT'),
        ('STATUS',       'TEXT'),
    ]:
        col_name = col_def[0].strip('"')
        if col_name not in existing:
            cur.execute(f'ALTER TABLE Operacije ADD COLUMN {col_def[0]} {col_def[1]};')

def prompt_yes_no(prompt):
    while True:
        resp = input(prompt).strip().upper()
        if resp in ("DA", "NE"):
            return resp == "DA"
        print("Molim unesite DA ili NE.")

def main():
    if not os.path.isfile(DB_PATH):
        print(f"ERROR: database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    try:
        while True:
            rn_input = input("Unesi nalog za pocetak operacije: ").strip()
            if not rn_input.isdigit():
                print("Molim unesite numerički nalog.")
                continue

            row = get_pending_row(cur, rn_input)
            if not row:
                print(f"Nalog {rn_input} nije pronađen ili je STATUS popunjen.")
                continue

            rn, kpl, start_ts, wc = row
            print(f"\nPronađeno:\n  RN:     {rn}\n  KPL:    {kpl}\n  START:  {start_ts}\n")

            if not prompt_yes_no("Da li zelite zapoceti operaciju? (DA/NE) "):
                continue  # back to RN prompt

            # Prepare Operacije table & data
            ensure_operacije_table(cur)

            now_utc    = datetime.utcnow()
            start_time = now_utc.time().isoformat()
            start_date = now_utc.date().isoformat()
            status_txt = "Izvodi se"
            id_op      = str(uuid.uuid4())

            # Insert new operation; Stop-Time and Stop-Date will remain NULL
            cur.execute(
                'INSERT INTO Operacije ("ID-OP", WC, RN, "Start-Time", "Start-Date", STATUS) '
                'VALUES (?, ?, ?, ?, ?, ?)',
                (id_op, wc, rn, start_time, start_date, status_txt)
            )
            conn.commit()

            print(
                f"\n✓ Operacija za RN={rn} započeta.\n"
                f"  ID-OP:       {id_op}\n"
                f"  WC:          {wc}\n"
                f"  Start-Date:  {start_date}\n"
                f"  Start-Time:  {start_time}\n"
                f"  STATUS:      {status_txt}\n"
                f"  Stop-Date:   (NULL)\n"
                f"  Stop-Time:   (NULL)\n"
            )
            break

    finally:
        conn.close()

if __name__ == "__main__":
    main()
