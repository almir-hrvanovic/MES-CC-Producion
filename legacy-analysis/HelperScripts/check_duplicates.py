import sqlite3

conn = sqlite3.connect('queryX.db')
cursor = conn.cursor()

# Find duplicate KPL+RN combinations
print("=== DUPLICATE KPL+RN COMBINATIONS ===")
cursor.execute("""
SELECT kpl, rn, COUNT(*) as count 
FROM work_orders 
GROUP BY kpl, rn 
HAVING COUNT(*) > 1 
ORDER BY count DESC 
LIMIT 10
""")

duplicates = cursor.fetchall()
print(f"Found {len(duplicates)} different KPL+RN combinations with duplicates")

for row in duplicates:
    print(f"KPL: {row[0]}, RN: {row[1]}, Count: {row[2]}")

# Show details of first duplicate
if duplicates:
    first_dup = duplicates[0]
    print(f"\n=== DETAILS FOR KPL: {first_dup[0]}, RN: {first_dup[1]} ===")
    cursor.execute("""
    SELECT id, kpl, rn, naziv, wc, wcname, quantity, norma 
    FROM work_orders 
    WHERE kpl = ? AND rn = ?
    """, (first_dup[0], first_dup[1]))
    
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, KPL: {row[1]}, RN: {row[2]}, NAZIV: {row[3][:30]}..., WC: {row[4]}, QTY: {row[5]}, NORMA: {row[6]}")

conn.close()