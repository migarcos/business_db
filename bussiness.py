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

        init_empl = [
            ("Aneth", "Wall", "awall@buss.com", "2023-01-15", 3500.00, "HR"),
            ("Kyle", "Bowser", "kbowser@buss.com", "2024-01-15", 4200.00, "ACC"),
            ("Te Ara", "Erueti", "terueti@buss.com", "2025-01-01", 3900.00, "ACC"),
            ("Garret", "Peterson", "gpeterson@buss.com", "2023-06-15", 2000.00, "SAL"),
            ("Percy", "Brandot", "pbrandot@buss.com", "2024-07-01", 2000.00, "SAL"),
            ("Salma", "Hayek", "shayek@buss.com", "2023-01-15", 3000.00, "SAL"),
            ("Angeline", "Jolie", "ajolie@buss.com", "2024-02-01", 2000.00, "SAL"),
            ("Sandra", "Bullock", "sbullock@buss.com", "2025-09-15", 2000.00, "SAL"),
            ("Kevin", "Space", "kspace@buss.com", "2023-11-15", 3500.00, "OPS"),
            ("Darth", "Vader", "dvader@buss.com", "2026-01-02", 3500.00, "OPS")
        ]

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                department_id INTEGER PRIMARY KEY AUTOINCREMENT,
                department_name TEXT NOT NULL,
                department_code TEXT UNIQUE NOT NULL
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
                salary DECIMAL(10, 2) NOT NULL CHECK (salary > 0),
                department_id INT,
                FOREIGN KEY (department_id) REFERENCES departments(department_id)
            )
        """)

        cursor.executemany("""
            INSERT OR IGNORE INTO employee (fname, lname, email, hire_date, salary, department_id)
            VALUES (?, ?, ?, ?, ?, (SELECT department_id FROM departments WHERE department_code = ?) )
        """, init_empl)

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
        print("\n")

def show_init_empl():
    with get_conn() as conn:
            cursor = conn.cursor()
            # cursor.execute("SELECT * FROM employee")
            cursor.execute("""SELECT
                        e.fname, e.lname, e.email, e.hire_date, e.salary, d.department_code 
                        FROM employee e
                        JOIN departments d ON e.department_id = d.department_id
                        ORDER BY d.department_code ASC
            """)

            rows = cursor.fetchall()
            print("\n --- EMPLOYEES LIST --- ")
            print(f"\n{'Name':<10} {'Last':<12} {'Email':<28} {'Hire Date':<12} {'Salary':>10} {'Dept':>6}")
            print("-" * 82)
            for row in rows:
                print(f'{row['fname']:<10} {row['lname']:<12} {row['email']:<28} {row['hire_date']:<12} {row['salary']:>10.2f} {row['department_code']:>6}')

# --- CLI handlers ---
def main():
    init_db()
    show_departments()
    show_init_empl()

if __name__ == "__main__":
    main()