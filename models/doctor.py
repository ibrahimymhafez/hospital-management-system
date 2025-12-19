from .person import Person


class Doctor(Person):
    def __init__(self, name, specialization, department_id):
        super().__init__(name)
        self.specialization = specialization
        self.department_id = department_id


    def save_to_db(self, cursor, conn):
        query = "INSERT INTO doctors (name, specialization, department_id) VALUES (?, ?, ?)"
        values = (self.name, self.specialization, self.department_id)
        cursor.execute(query, values)
        conn.commit()
        print(f"Doctor {self.name} at department {self.specialization} saved to database successfully.")

    def delete_from_db(self, cursor, conn, doctor_id):
        cursor.execute(
            "DELETE FROM doctors WHERE id = ?",
            (doctor_id,)
        )
        print(f"Doctor with id {doctor_id} deleted successfully.")
        conn.commit()
    def update_doc_info(self, cursor, conn, doctor_id):
        cursor.execute(
            "UPDATE doctors SET name = ?, specialization = ?, department_id = ? WHERE id = ?",
            (self.name, self.specialization, self.department_id, doctor_id)
        )
        conn.commit()
