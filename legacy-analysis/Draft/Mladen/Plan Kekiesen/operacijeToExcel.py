#!/usr/bin/env python3
import os
import sqlite3
import pandas as pd

def export_table(conn, table_name, filename, output_dir):
    """
    Reads the given table from the SQLite connection and writes it
    to an Excel file named filename (inside output_dir).
    """
    df = pd.read_sql_query(f'SELECT * FROM "{table_name}"', conn)
    out_path = os.path.join(output_dir, filename)
    with pd.ExcelWriter(out_path, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name=table_name)
    print(f"✓ {table_name} → {out_path}")

def main():
    # Project root and paths
    root      = os.getcwd()
    db_path   = os.path.join(root, "db", "report.db")
    report_dir = os.path.join(root, "Report")
    os.makedirs(report_dir, exist_ok=True)

    # Open DB and export
    conn = sqlite3.connect(db_path)
    try:
        export_table(conn, "Operacije",   "tb_Operacije.xlsx", report_dir)
        export_table(conn, "report",      "tb_Report.xlsx",    report_dir)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
