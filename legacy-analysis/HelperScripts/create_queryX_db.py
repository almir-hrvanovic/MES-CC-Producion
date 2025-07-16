import pandas as pd
import sqlite3
from datetime import datetime, timedelta

# Read Excel file
print("Reading Excel file...")
df = pd.read_excel('RawData/query.xlsx')

# Convert Excel date numbers to proper dates
def excel_date_to_datetime(excel_date):
    if pd.isna(excel_date):
        return None
    # Excel dates are days since 1900-01-01 (with leap year bug)
    base_date = datetime(1899, 12, 30)  # Excel's epoch
    return base_date + timedelta(days=int(excel_date))

# Convert date columns
df['datum_isporuke'] = df['Isporuka'].apply(excel_date_to_datetime)
df['datum_sastavljanja'] = df['Datum SAS'].apply(excel_date_to_datetime)

# Create SQLite database
print("Creating SQLite database...")
conn = sqlite3.connect('queryX.db')

# Create work_orders table
create_table_sql = """
CREATE TABLE work_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kpl INTEGER NOT NULL,
    kplq INTEGER,
    rn INTEGER NOT NULL,
    naziv TEXT NOT NULL,
    norma REAL,
    quantity INTEGER,
    zq INTEGER,
    cq INTEGER,
    wc TEXT,
    wcname TEXT,
    mto TEXT,
    datum_isporuke DATE,
    datum_sastavljanja DATE,
    norma_j REAL,
    item TEXT,
    promjena TEXT,
    hitno INTEGER,
    suma_h REAL,
    zavrsetak_masinske DATE,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

conn.execute(create_table_sql)

# Prepare data for insertion
insert_data = []
for _, row in df.iterrows():
    insert_data.append((
        int(row['KPL']) if pd.notna(row['KPL']) else None,
        int(row['KPLQ']) if pd.notna(row['KPLQ']) else None,
        int(row['RN']) if pd.notna(row['RN']) else None,
        str(row['NAZIV']) if pd.notna(row['NAZIV']) else '',
        float(row['Norma']) if pd.notna(row['Norma']) else None,
        int(row['Q']) if pd.notna(row['Q']) else None,
        int(row['ZQ']) if pd.notna(row['ZQ']) else None,
        int(row['CQ']) if pd.notna(row['CQ']) else None,
        str(row['WC']) if pd.notna(row['WC']) else None,
        str(row['WCNAME']) if pd.notna(row['WCNAME']) else None,
        str(row['MTO']) if pd.notna(row['MTO']) else None,
        row['datum_isporuke'].strftime('%Y-%m-%d') if row['datum_isporuke'] else None,
        row['datum_sastavljanja'].strftime('%Y-%m-%d') if row['datum_sastavljanja'] else None,
        float(row['NORMA/J']) if pd.notna(row['NORMA/J']) else None,
        str(row['Item']) if pd.notna(row['Item']) else None,
        str(row['PROMJENA']) if pd.notna(row['PROMJENA']) else None,
        int(row['HITNO']) if pd.notna(row['HITNO']) else None,
        float(row['SUMA H']) if pd.notna(row['SUMA H']) else None,
        excel_date_to_datetime(row['ZAVRŠETAK MAŠINSKE']).strftime('%Y-%m-%d') if pd.notna(row['ZAVRŠETAK MAŠINSKE']) else None
    ))

# Insert data
insert_sql = """
INSERT INTO work_orders (
    kpl, kplq, rn, naziv, norma, quantity, zq, cq, wc, wcname, mto,
    datum_isporuke, datum_sastavljanja, norma_j, item, promjena, hitno,
    suma_h, zavrsetak_masinske
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

print(f"Inserting {len(insert_data)} records...")
conn.executemany(insert_sql, insert_data)

# Create indexes for better performance
print("Creating indexes...")
conn.execute("CREATE INDEX idx_kpl ON work_orders(kpl);")
conn.execute("CREATE INDEX idx_rn ON work_orders(rn);")
conn.execute("CREATE INDEX idx_wc ON work_orders(wc);")
conn.execute("CREATE INDEX idx_datum_isporuke ON work_orders(datum_isporuke);")
conn.execute("CREATE INDEX idx_datum_sastavljanja ON work_orders(datum_sastavljanja);")
conn.execute("CREATE INDEX idx_status ON work_orders(status);")

# Commit and close
conn.commit()

# Show some statistics
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM work_orders")
total_records = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(DISTINCT kpl) FROM work_orders")
unique_kpl = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(DISTINCT wc) FROM work_orders")
unique_wc = cursor.fetchone()[0]

print(f"\nDatabase created successfully!")
print(f"Total records: {total_records}")
print(f"Unique KPL (work orders): {unique_kpl}")
print(f"Unique work centers: {unique_wc}")

# Show sample data
print("\nSample records:")
cursor.execute("SELECT kpl, rn, naziv, norma, wc, datum_isporuke FROM work_orders LIMIT 5")
for row in cursor.fetchall():
    print(f"KPL: {row[0]}, RN: {row[1]}, NAZIV: {row[2][:30]}..., NORMA: {row[3]}, WC: {row[4]}, ISPORUKA: {row[5]}")

conn.close()
print("\nDatabase 'queryX.db' created successfully!")