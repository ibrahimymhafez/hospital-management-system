import sqlite3

def create_schema():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK (role IN ('admin', 'secretary')) DEFAULT 'secretary',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        gender TEXT,
        email TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT,
        department_id INTEGER,
        day TEXT,
        age INTEGER,
        gender TEXT,
        phone TEXT,
        email TEXT,
        FOREIGN KEY(department_id) REFERENCES departments(id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        phone TEXT,
        gender TEXT,
        email TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        day TEXT NOT NULL CHECK(day IN ('Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday')),
        Status TEXT,
        Payment TEXT,
        FOREIGN KEY(doctor_id) REFERENCES doctors(id),
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    );
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_schema()