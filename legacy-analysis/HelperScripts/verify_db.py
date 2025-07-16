import sqlite3

# Connect to database
conn = sqlite3.connect('queryX.db')
cursor = conn.cursor()

# Show table structure
print("=== DATABASE STRUCTURE ===")
cursor.execute("PRAGMA table_info(work_orders)")
print("Table: work_orders")
for row in cursor.fetchall():
    print(f"  {row[1]} - {row[2]} {'(Primary Key)' if row[5] else ''}")

# Show statistics
print("\n=== DATABASE STATISTICS ===")
cursor.execute("SELECT COUNT(*) FROM work_orders")
total = cursor.fetchone()[0]
print(f"Total records: {total}")

cursor.execute("SELECT COUNT(DISTINCT kpl) FROM work_orders")
unique_kpl = cursor.fetchone()[0]
print(f"Unique work orders (KPL): {unique_kpl}")

# Date range
cursor.execute("SELECT MIN(datum_isporuke), MAX(datum_isporuke) FROM work_orders WHERE datum_isporuke IS NOT NULL")
date_range = cursor.fetchone()
print(f"Delivery date range: {date_range[0]} to {date_range[1]}")

cursor.execute("SELECT MIN(datum_sastavljanja), MAX(datum_sastavljanja) FROM work_orders WHERE datum_sastavljanja IS NOT NULL")
assembly_range = cursor.fetchone()
print(f"Assembly date range: {assembly_range[0]} to {assembly_range[1]}")

# Work centers
print("\n=== WORK CENTERS ===")
cursor.execute("SELECT wc, wcname, COUNT(*) as count FROM work_orders GROUP BY wc, wcname ORDER BY count DESC")
for row in cursor.fetchall():
    print(f"{row[0]} - {row[1]}: {row[2]} operations")

# Sample urgent orders
print("\n=== SAMPLE URGENT ORDERS (HITNO > 0) ===")
cursor.execute("SELECT kpl, naziv, norma, datum_isporuke, hitno FROM work_orders WHERE hitno > 0 LIMIT 5")
for row in cursor.fetchall():
    print(f"KPL: {row[0]}, NAZIV: {row[1][:40]}..., NORMA: {row[2]}h, ISPORUKA: {row[3]}, HITNO: {row[4]}")

# Sample by delivery date
print("\n=== SAMPLE ORDERS BY DELIVERY DATE ===")
cursor.execute("SELECT kpl, naziv, norma, datum_isporuke FROM work_orders WHERE datum_isporuke IS NOT NULL ORDER BY datum_isporuke LIMIT 5")
for row in cursor.fetchall():
    print(f"KPL: {row[0]}, NAZIV: {row[1][:40]}..., NORMA: {row[2]}h, ISPORUKA: {row[3]}")

conn.close()
print("\n=== DATABASE VERIFICATION COMPLETE ===")