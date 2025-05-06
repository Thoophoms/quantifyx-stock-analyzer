import psycopg2

try:
    conn = psycopg2.connect("postgresql://thoophoms:@localhost:5432/quantifyx")
    print("✅ Connected to PostgreSQL!")
    conn.close()
except Exception as e:
    print("❌ Failed to connect:", e)