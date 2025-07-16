#!/usr/bin/env python3
import os
import re
from datetime import datetime
import pandas as pd

def main():
    # --- Paths (adjust if needed) ---
    root = os.path.abspath(os.path.dirname(__file__))
    input_path = os.path.join(root, "Plan", "Mladen.xlsm")
    output_dir = os.path.join(root, "Report")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "report.xlsx")

    # --- 1) Read sheet PRINT without headers ---
    df = pd.read_excel(input_path, sheet_name="PRINT", header=None, engine="openpyxl")

    # --- 2) Keep only first 22 columns (Column1…Column22) ---
    df = df.iloc[:, :22]

    # --- 3) Remove the top 3 rows, then promote the next row to header ---
    df = df.iloc[3:].reset_index(drop=True)
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)

    # --- 4) Convert START to datetime ---
    if "START" in df.columns:
        df["START"] = pd.to_datetime(df["START"], errors="coerce")

    # --- 5) Drop END TIME and KASNI if present ---
    for col in ["END TIME", "KASNI"]:
        if col in df.columns:
            df.drop(columns=col, inplace=True)

    # --- 6) Filter out rows where Isporuka == "PAUZA" ---
    if "Isporuka" in df.columns:
        df = df[df["Isporuka"] != "PAUZA"]

    # --- 7) Rename the auto-date column to "Datum PZ" ---
    date_cols = []
    pattern = re.compile(r"\d{1,2}/\d{1,2}/\d{4}")
    for col in df.columns:
        if isinstance(col, (datetime, pd.Timestamp)):
            date_cols.append(col)
        elif isinstance(col, str) and pattern.match(col):
            date_cols.append(col)
    if date_cols:
        df.rename(columns={date_cols[0]: "Datum PZ"}, inplace=True)

    # --- 8) Convert Datum PZ and Datum PS to datetime ---
    for c in ["Datum PZ", "Datum PS"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")

    # --- 9) Drop fully blank rows (treat empty strings as blank) ---
    df.replace("", pd.NA, inplace=True)
    df.dropna(how="all", inplace=True)
    df.reset_index(drop=True, inplace=True)

    # --- 10) Split START into date and time columns ---
    if "START" in df.columns:
        df["START - Datum"]   = df["START"].dt.date
        df["START - Vrijeme"] = df["START"].dt.time

    # --- 11) Remove Column22 if it survived as a literal name ---
    if "Column22" in df.columns:
        df.drop(columns="Column22", inplace=True)

    # --- 12) Save to Excel ---
    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Report")

    print(f"✓ Transformed data written to:\n   {output_path}")

if __name__ == "__main__":
    main()
