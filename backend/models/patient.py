from backend.models.person import Person

class Patient(Person):
    def __init__(self, name, age, gender, phone, email):
        super().__init__(name, age, gender, phone, email)

    def save_to_db(self, cursor, conn):
        values = (self.name, self.age, self.gender, self.phone, self.email)
        query = "INSERT INTO patients(name, age, gender, phone, email) VALUES(?, ?, ?, ?, ?)"
        cursor.execute(query, values)
        conn.commit()
        self.id = cursor.lastrowid
    
    @staticmethod
    def fetch_all_patients(cursor):
        query = "SELECT * FROM patients"
        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def search_patients(cursor, search_term):
        query = "SELECT * FROM patients WHERE name LIKE ? OR id LIKE ?"
        cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))
        return cursor.fetchall()
    
    @staticmethod
    def delete_from_db(cursor, conn, id):
        query = "SELECT * FROM patients WHERE id = ?"
        cursor.execute(query, (id,))
        found = cursor.fetchone()
        if found != None:
            query = "DELETE FROM patients WHERE id = ?"
            cursor.execute(query, (id,))
            conn.commit()
            print(f"Patient with ID: {id} was deleted.")
        else:
            print(f"Patient ID is not found.")

    def update_info(self, cursor, conn, id):
        query = "UPDATE patients SET name = ?, age = ?, gender = ?, phone = ?, email = ? WHERE id = ?"
        values = (self.name, self.age, self.gender, self.phone, self.email, id)
        cursor.execute(query, values)
        conn.commit()
