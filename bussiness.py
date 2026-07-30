import sqlite3

def get_conn():
    conn = sqlite3.connect("business.db")
    conn.row_factory = sqlite3.Row  # dictionary.like row formatting 
    return conn

def init_db():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.exceute("PRAGMA foreign_keys = ON")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                department_id INTEGER PRIMARY KEY AUTOINCREMENT,
                department_name TEXT NOT NULL,
                department_code TEXT NOT NULL
            )    
        """)

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

        conn.commi()


# --- CLI handlers ---
def main():
    init_db()

if __name__ == "__main__":
    main()