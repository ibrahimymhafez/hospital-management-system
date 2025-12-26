from backend.models.person import Person


class Doctor(Person):
    def __init__(self, name, age, gender, phone, email, specialization, department_id):
        super().__init__(name, age, gender, phone, email)
        self.specialization = specialization
        self.department_id = department_id

    
    def save_to_db(self, cursor, conn):
        query = """INSERT INTO doctors 
                    (name, age, gender, phone, email, specialization, department_id) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)"""
        values = (self.name, self.age, self.gender, self.phone, self.email, self.specialization, self.department_id)
        cursor.execute(query, values)
        conn.commit()
        print(f"Doctor {self.name} at department {self.specialization} saved to database successfully.")


    @staticmethod
    def delete_from_db(cursor, conn, doctor_id):
        cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
        print(f"Doctor with id {doctor_id} deleted successfully.")
        conn.commit()
        
    def update_doc_info(self, cursor, conn, doctor_id):
        cursor.execute(
            "UPDATE doctors SET name = ?, age = ?, gender = ?, phone = ?, email = ?, specialization = ?, department_id = ? WHERE id = ?",
            (self.name, self.age, self.gender, self.phone, self.email, self.specialization, self.department_id, doctor_id)
        )
        conn.commit()

    #returns all the data from the doctors table for viewing
    @staticmethod
    def get_all(cursor):
        cursor.execute("SELECT id, name, age, gender, phone, email, specialization, department_id FROM doctors")
        rows = cursor.fetchall()
        return rows

    # returns the resurlt of a search
    @staticmethod
    def search(cursor, text):
        cursor.execute("SELECT * FROM doctors WHERE name LIKE ? OR specialization LIKE ?", (f"%{text}%", f"%{text}%"))
        return cursor.fetchall()