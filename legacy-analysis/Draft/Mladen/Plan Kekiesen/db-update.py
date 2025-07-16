#!/usr/bin/env python3
import os
import sqlite3
import pandas as pd
from datetime import date, time, datetime
import numpy as np

def infer_sql_type(pd_dtype):
    """Map pandas dtype to SQLite type."""
    if pd.api.types.is_integer_dtype(pd_dtype):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(pd_dtype):
        return "REAL"
    else:
        return "TEXT"

def serialize_value(v):
    """Convert unsupported types to something sqlite3 can handle."""
    if isinstance(v, (pd.Timestamp, datetime)):
        return v.isoformat(sep=' ')
    if isinstance(v, date):
        return v.isoformat()
    if isinstance(v, time):
        return v.isoformat()
    if isinstance(v, np.generic):
        # numpy types (e.g. np.int64, np.float64)
        return v.item()
    # leave ints, floats, strings, None as-is
    return v

def main():
    # Paths
    root       = os.path.abspath(os.path.dirname(__file__))
    excel_path = os.path.join(root, "Report", "report.xlsx")
    db_dir     = os.path.join(root, "db")
    os.makedirs(db_dir, exist_ok=True)
    db_path    = os.path.join(db_dir, "report.db")

    # 1) Load the first sheet into a DataFrame
    df = pd.read_excel(excel_path, engine="openpyxl")

    # 2) Open (or create) the SQLite database
    conn = sqlite3.connect(db_path)
    cur  = conn.cursor()

    # 3) Build the CREATE TABLE statement
    cols = ['"id" INTEGER PRIMARY KEY AUTOINCREMENT']
    for col, dtype in df.dtypes.items():
        sql_type = infer_sql_type(dtype)
        # escape column names with quotes
        cols.append(f'"{col}" {sql_type}')
    create_sql = f"""
    CREATE TABLE IF NOT EXISTS report (
      {',\n      '.join(cols)}
    );
    """
    cur.execute(create_sql)

    # 4) Prepare insertion
    data_cols   = list(df.columns)
    placeholders = ", ".join("?" for _ in data_cols)
    insert_sql   = f"""
      INSERT INTO report ({', '.join(f'"{c}"' for c in data_cols)})
      VALUES ({placeholders});
    """

    # 5) Serialize rows and insert
    rows = []
    for row in df.itertuples(index=False, name=None):
        serialized = tuple(serialize_value(v) for v in row)
        rows.append(serialized)
    cur.executemany(insert_sql, rows)

    # 6) Finalize
    conn.commit()
    conn.close()

    print(f"✓ Database written to {db_path}, table 'report' now has {len(rows)} rows.")

if __name__ == "__main__":
    main()
