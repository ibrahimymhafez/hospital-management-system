from person import Person

class Patient(Person):
    def __init__(self, name, age, gender, phone, disease):
        super().__init__(name, age, gender, phone)
        self.disease = disease
    
    @staticmethod
    def assign_doctor(cursor, conn, patient_id, doctor_id):
        query = "SELECT * FROM patients WHERE patient_id = ?"
        cursor.execute(query, (patient_id,))
        patient = cursor.fetchone()

        query = "SELECT * FROM doctors WHERE doctor_id = ?"
        cursor.execute(query, (doctor_id,))
        doctor = cursor.fetchone()

        if patient and doctor:
            query = "UPDATE patients SET assigned_doctor_id = ? WHERE patient_id = ?"
            values = (doctor_id, patient_id)
            cursor.execute(query, values)
            conn.commit()
            print(f"Doctor with ID: {doctor_id} is assigned to patient with ID: {patient_id} successfully")
        else:
            print("Doctor or Patient does not exits")
            
    def save_to_db(self, cursor, conn):
        values = (self.name, self.age, self.gender, self.phone, self.disease)
        query = "INSERT INTO patients(name, age, gender, phone, disease) VALUES(?, ?, ?, ?, ?)"
        cursor.execute(query, values)
        conn.commit()
        self.patient_id = cursor.lastrowid
    
    @staticmethod
    def delete_from_db(cursor, conn, patient_id):
        query = "SELECT * FROM patients WHERE patient_id = ?"
        cursor.execute(query, (patient_id,))
        found = cursor.fetchone()
        if found != None:
            query = "DELETE FROM patients WHERE patient_id = ?"
            cursor.execute(query, (patient_id,))
            conn.commit()
            print(f"Patient with ID: {patient_id} was deleted.")
        else:
            print(f"Patient ID is not found.")

    def update_info(self, cursor, conn, patient_id):
        query = "UPDATE patients SET name = ?, age = ?, gender = ?, phone = ?, disease = ? WHERE patient_id = ?"
        values = (self.name, self.age, self.gender, self.phone, self.disease, patient_id)
        cursor.execute(query, values)
        conn.commit()
