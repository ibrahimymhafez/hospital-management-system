import sqlite3
import bcrypt
def create_new_schema():
    # Connect to the database (it will be created if it doesn't exist)
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    
    print("--- Creating Database Schema for the New System ---")

    # 1. Departments Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );
    ''')

    # 2. Users Table (For Login: Admin / Secretary)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password BLOB NOT NULL,
        role TEXT NOT NULL CHECK (role IN ('admin', 'secretary')) DEFAULT 'secretary',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        gender TEXT,
        email TEXT
    );
    ''')

    # 3. Doctors Table
    # Matches the 'Doctor' class attributes: name, age, gender, phone, email, specialization, department_id
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        phone TEXT,
        email TEXT,
        specialization TEXT,
        department_id INTEGER,
        FOREIGN KEY(department_id) REFERENCES departments(id)
    );
    ''')

    # 4. Patients Table
    # Matches the 'Person'/'Patient' class attributes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        phone TEXT,
        email TEXT
    );
    ''')

    # 5. Appointments Table (The New Structure)
    # Includes 'appointment_date' for the timestamp logic we created
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        day TEXT,                  -- Stores the day name (e.g., "Monday")
        appointment_date TEXT,     -- Stores the full timestamp (e.g., "2025-10-30 10:30:00")
        Status TEXT DEFAULT 'First Visit',
        Payment TEXT DEFAULT 'Cash',
        FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE,
        FOREIGN KEY(doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
    );
    ''')

    # Optional: Insert default admin user if not exists
    try:
        hashed_password = bcrypt.hashpw("admin1234@".encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', ? , 'admin')", (hashed_password,))
        print("Default admin user created.")
    except sqlite3.IntegrityError:
        pass # Admin already exists

    conn.commit()
    conn.close()
    print("Database 'hospital.db' is ready with the NEW schema.")

if __name__ == "__main__":
    create_new_schema()
