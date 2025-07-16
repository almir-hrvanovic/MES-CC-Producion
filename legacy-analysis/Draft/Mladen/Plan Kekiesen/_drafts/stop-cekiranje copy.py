#!/usr/bin/env python3
import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "db", "report.db")

def ensure_operacije_table(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Operacije (
      id             INTEGER PRIMARY KEY,
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
    # Ensure Stop-Time and Stop-Date exist
    cur.execute('PRAGMA table_info(Operacije);')
    existing = {r[1] for r in cur.fetchall()}
    for col in ("Stop-Time", "Stop-Date"):
        if col not in existing:
            cur.execute(f'ALTER TABLE Operacije ADD COLUMN "{col}" TEXT;')

def list_active(cur):
    cur.execute("""
        SELECT id, "ID-OP", WC, RN, "Start-Date", "Start-Time"
          FROM Operacije
         WHERE STATUS = 'Izvodi se'
         ORDER BY "Start-Date", "Start-Time"
    """)
    return cur.fetchall()

def prompt_selection(count):
    while True:
        sel = input(f"Unesite broj (1–{count}) naloga/operacije koji želite obraditi: ").strip()
        if sel.isdigit():
            n = int(sel)
            if 1 <= n <= count:
                return n
        print(f"Nevažeća numeracija — unesite broj između 1 i {count}.")

def prompt_action():
    print("\nOdaberite akciju:")
    print(" 1. Završeno")
    print(" 2. Kraj smjene")
    print(" 3. Pauziraj operaciju")
    while True:
        c = input("Unesite 1, 2 ili 3: ").strip()
        if c in ("1","2","3"):
            return int(c)
        print("Molim unesite 1, 2 ili 3.")

def main():
    if not os.path.isfile(DB_PATH):
        print(f"ERROR: database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    ensure_operacije_table(cur)

    try:
        while True:
            active = list_active(cur)
            if not active:
                print("Nema više operacija u statusu ‘Izvodi se’. Izlazim.")
                break

            print("\nAktivne operacije (STATUS = 'Izvodi se'):")
            for idx, (pk, id_op, wc, rn, sd, st) in enumerate(active, start=1):
                print(f"{idx}. RN={rn} | WC={wc} | ID-OP={id_op} | Start={sd} {st}")

            sel = prompt_selection(len(active))
            pk, id_op, wc, rn, sd, st = active[sel-1]

            action = prompt_action()
            now = datetime.utcnow()
            stop_time = now.time().isoformat()
            stop_date = now.date().isoformat()

            if action == 1:
                status_txt = "Završeno"
                # update stop-time/date + status
                cur.execute("""
                  UPDATE Operacije
                     SET "Stop-Time" = ?, "Stop-Date" = ?, STATUS = ?
                   WHERE id = ?
                """, (stop_time, stop_date, status_txt, pk))
            elif action == 2:
                status_txt = "Kraj smjene"
                cur.execute("""
                  UPDATE Operacije
                     SET STATUS = ?
                   WHERE id = ?
                """, (status_txt, pk))
            else:
                status_txt = "Pauziraj operaciju"
                cur.execute("""
                  UPDATE Operacije
                     SET STATUS = ?
                   WHERE id = ?
                """, (status_txt, pk))

            # also update report.STATUS for the paired id
            cur.execute("""
              UPDATE report
                 SET STATUS = ?
               WHERE id = ?
                 AND (STATUS IS NULL OR STATUS = '')
            """, (status_txt, pk))

            conn.commit()
            print(f"\n✓ Operacija RN={rn} sada ima STATUS='{status_txt}'.")
            # loop back to list remaining

    finally:
        conn.close()

if __name__ == "__main__":
    main()
