#!/usr/bin/env python3
import os
import sqlite3
import pandas as pd

def main():
    # --- Paths ---
    root        = os.getcwd()
    db_path     = os.path.join(root, "db", "report.db")
    excel_path  = os.path.join(root, "Report", "report.xlsx")

    # --- 1) Read existing Excel sheet ---
    df = pd.read_excel(excel_path, sheet_name="Report", engine="openpyxl")

    # --- 2) Fetch id→STATUS from DB.report ---
    conn = sqlite3.connect(db_path)
    status_df = pd.read_sql_query("SELECT id, STATUS FROM report", conn)
    conn.close()

    # --- 3) Merge statuses into DataFrame (only updating STATUS) ---
    #    We assume your DataFrame has a column 'id' matching report.id
    if "id" not in df.columns:
        raise KeyError("No 'id' column in report.xlsx to match on")

    df = df.merge(status_df, on="id", how="left", suffixes=("", "_db"))
    # If STATUS_db is not null, use it; otherwise keep original
    df["STATUS"] = df["STATUS_db"].combine_first(df["STATUS"])
    df.drop(columns=["STATUS_db"], inplace=True)

    # --- 4) Overwrite the Excel file ---
    with pd.ExcelWriter(excel_path, engine="openpyxl", mode="overwrite") as writer:
        df.to_excel(writer, index=False, sheet_name="Report")

    print(f"✓ report.xlsx updated (only STATUS column changed)")

if __name__ == "__main__":
    main()
