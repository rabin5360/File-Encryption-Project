import mysql.connector

def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",  # replace with your MySQL password
        database="file_encryption_db"
    )
    return conn

def log_action(filename, action, status):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO encryption_logs (filename, action, status) VALUES (%s, %s, %s)"
    cursor.execute(query, (filename, action, status))
    conn.commit()
    conn.close()
    print(f"[DB] Log saved: {filename} -> {action} -> {status}")

def view_logs():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM encryption_logs")
    rows = cursor.fetchall()
    conn.close()

    print("\n========== ENCRYPTION LOGS ==========")
    print(f"{'ID':<5} {'Filename':<25} {'Action':<15} {'Status':<10} {'Date'}")
    print("-" * 70)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<25} {row[2]:<15} {row[3]:<10} {row[4]}")
    print("=" * 70)