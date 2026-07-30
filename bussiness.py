import sqlite3

def get_conn():
    conn = sqlite3.connect("business.db")
    conn.row_factory = sqlite3.Row  # dictionary.like row formatting 
    return conn

def init_db():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        basic_departments = [
            ("Human Resources", "HR"),
            ("Accounting", "ACC"),
            ("sales", "SAL"),
            ("Information Technology", "IT"),
            ("Operations", "OPS")
        ]

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                department_id INTEGER PRIMARY KEY AUTOINCREMENT,
                department_name TEXT NOT NULL,
                department_code TEXT UNIQuE NOT NULL
            )    
        """)

        cursor.executemany("""
            INSERT OR IGNORE INTO departments (department_name, department_code)
            VALUES (?, ?)
        """, basic_departments)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employee (
                employee_id INT PRIMARY KEY,
                fname TEXT NOT NULL,
                lname TEXT NOT NULL,
                email TEXT NOT NULL,
                hire_date DATE NOT NULL,
                status TEXT DEFAULT 'Active',
                department_id INT,
                FOREIGN KEY (department_id) REFERENCES departments(deparment_id)
            )    
        """)

        conn.commit()

def show_departments():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM departments")
        # return cursor.fetchall()
        rows = cursor.fetchall()
        print("\n --- DEPARTMENTS LIST --- ")
        for row in rows:
            print(f'ID: {row['department_id']} | Código: {row['department_code']} | Nombre: {row['department_name']}')

# --- CLI handlers ---
def main():
    init_db()
    show_departments()

if __name__ == "__main__":
    main()