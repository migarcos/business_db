import sqlite3
from datetime import date

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
            ("Darth", "Vader", "dvader@buss.com", "2026-01-02", 3500.00, "OPS"),
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
                employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
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

        cursor.execute("SELECT COUNT(*) FROM employee")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("""
                INSERT INTO employee (fname, lname, email, hire_date, salary, department_id)
                VALUES (?, ?, ?, ?, ?, (SELECT department_id FROM departments WHERE department_code = ?) )
            """, init_empl,)

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

def show_all_empl():
    with get_conn() as conn:
            cursor = conn.cursor()
            # cursor.execute("SELECT * FROM employee")
            cursor.execute("""SELECT
                        e.employee_id, e.fname, e.lname, e.email, e.hire_date, e.salary, d.department_code 
                        FROM employee e
                        JOIN departments d ON e.department_id = d.department_id
                        ORDER BY d.department_code ASC
            """)

            rows = cursor.fetchall()
            print("\n --- EMPLOYEES LIST --- ")
            print(f"\n{'ID':<5} {'Name':<10} {'Last':<12} {'Email':<20} {'Hire Date':<12} {'Salary':>10} {'Dept':>6}")
            print("-" * 82)
            for row in rows:
                # emp_id = row['employee_id'] if row['employee_id'] is not None else 0
                # print(f"{emp_id:<5} {row['fname']:<10} {row['lname']:<12} {row['email']:<20} {row['hire_date']:<12} {row['salary']:>10.2f} {row['department_code']:>6}")
                print(f"{row['employee_id']:<5} {row['fname']:<10} {row['lname']:<12} {row['email']:<20} {row['hire_date']:<12} {row['salary']:>10.2f} {row['department_code']:>6}")

#  - - - -  CRUD  - - - -  
def create_emp(data):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO employee (fname, lname, email, hire_date, salary, department_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data["fname"], data["lname"], data["email"], data["hire_date"], data["salary"], data["department_id"]
            ),
        )
        conn.commit()
        print("\n A new employee was created successfully!")

# --- CLI handlers ---
def emp_creation():
    
    fields = [
        ("fname", "First Name"),
        ("lname", "Last Name"),
        ("email", "Email Address"),
        ("salary", "Salary"),
    ]

    employee_data = {}

    print("\n---- Create a new employee ----")
    print("* This fields are required:")

    for field_key, field_label in fields:
        while True:
            value = input(f'{field_label}: ').strip()

            if not value:
                print(f' ERROR! {field_label} cannot be blank. Write a valid value.')
                continue

            if field_key == "salary":
                try:
                    value = float(value)
                    if value < 800:
                        print(' ERROR! Salary must be greater than 799. Try again')
                        continue
                except ValueError:
                    print('ERROR! Invalid number format for Salary. Try again')
                    continue

            employee_data[field_key] = value
            break

    hire_date_str = date.today().isoformat()
    employee_data["hire_date"] = hire_date_str
    print('Hire Date use, as default value, the actual date.')

    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT department_id, department_code, department_name FROM departments")
        departments = cursor.fetchall()

        print('\nAvailable departments: ')
        for dept in departments:
            print(f"[{dept['department_code']:<4}] - [{dept['department_name']}] ")

        while True:
            dept_code = (
                input('\nEnter a valid department Code: ').strip().upper()
            )

            cursor.execute('SELECT department_id FROM departments WHERE department_code = ?',
                        (dept_code,),
            )
            dept_result = cursor.fetchone()

            if dept_result:
                employee_data['department_id'] = dept_result['department_id']
                break
            else:
                print('ERROR! Invalid department code. Choose from the list above')

    create_emp(employee_data)

def emp_del():
    print("starting")

def main():
    init_db()
    # show_departments()     show_init_empl()
    try: 
        while True:
            print("\n ===   MAIN MENU   === ")
            print("1. Add Employee")
            print("2. List All Employee")
            print("3. Find Employee by Name")
            print("4. Update Employee")
            print("5. Delete Employee")
            print("6. Exit ")
            usr_opt = input("\nSelect an option: ").strip()

            match usr_opt:
                case "1": 
                    emp_creation()
                case "2":
                    show_all_empl()
                case "5":
                    emp_del()
                case "6": 
                    print("\nExiting application. Goodbye!")
                    break
                case _:
                    print("\nInvalid choice. Please select from the list")

    except (KeyboardInterrupt, EOFError):
        print("\nGame Over, Try afain")

if __name__ == "__main__":
    main()