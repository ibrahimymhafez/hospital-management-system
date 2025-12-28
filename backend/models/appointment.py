import sqlite3

class Appointment:
    def __init__(self, patient_id, doctor_id, day, status="First Visit", payment="Cash"):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.day = day
        self.status = status
        self.payment = payment

    @staticmethod
    def check_patient_exists(cursor, patient_id):
        cursor.execute("SELECT id FROM patients WHERE id = ?", (patient_id,))
        result = cursor.fetchone()
        return result is not None

    def save_to_db(self, cursor, conn):
        if not Appointment.check_patient_exists(cursor, self.patient_id):
            print(f"Error: Patient with ID {self.patient_id} does not exist.")
            return

        query = """
        INSERT INTO appointments(patient_id, doctor_id, day, Status, Payment)
        VALUES (?, ?, ?, ?, ?)
        """
        values = (self.patient_id, self.doctor_id, self.day, self.status, self.payment)
        
        try:
            cursor.execute(query, values)
            conn.commit()
            print("Appointment saved successfully!")
        except Exception as e:
            print(f"Error saving appointment: {e}")

    @staticmethod
    def delete_appointment(cursor, conn, appointment_id):
        query = "DELETE FROM appointments WHERE id = ?"
        try:
            cursor.execute(query, (appointment_id,))
            if cursor.rowcount > 0:
                conn.commit()
                print(f"Appointment {appointment_id} deleted successfully.")
            else:
                print("Appointment not found.")
        except Exception as e:
            print(f"Error deleting appointment: {e}")

    @staticmethod
    def get_doctor_queue(cursor, doctor_id):
        query = """
        SELECT a.id, p.name, a.day, a.Status, a.Payment 
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        WHERE a.doctor_id = ?
        ORDER BY a.id ASC
        """
        try:
            cursor.execute(query, (doctor_id,))
            rows = cursor.fetchall()
            
            print(f"\n--- Queue for Doctor ID {doctor_id} ---")
            if not rows:
                print("No appointments found for this doctor.")
            else:
                for row in rows:
                    print(f"Appt ID: {row[0]} | Patient: {row[1]} | Day: {row[2]} | Status: {row[3]} | Pay: {row[4]}")
            return rows
        except Exception as e:
            print(f"Error fetching queue: {e}")
            return []

