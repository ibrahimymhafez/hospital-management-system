import sqlite3
from datetime import datetime

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
            print("Please go to register the new patient")
            return

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = """
        INSERT INTO appointments(patient_id, doctor_id, day, appointment_date, Status, Payment)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        values = (self.patient_id, self.doctor_id, self.day, current_time, self.status, self.payment)
        
        try:
            cursor.execute(query, values)
            case_number = cursor.lastrowid
            conn.commit()
            
            print("--------------------------------------------------")
            print("Registration Successful!")
            print(f"Time: {current_time}")
            print(f"Your Case Number (Ticket) is: {case_number}")
            print("--------------------------------------------------")
            
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
        today_date = datetime.now().strftime('%Y-%m-%d')

        query = """
        SELECT a.id, p.name, a.appointment_date, a.Status, a.Payment 
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        WHERE a.doctor_id = ? AND date(a.appointment_date) = ?
        ORDER BY a.id ASC
        """
        try:
            cursor.execute(query, (doctor_id, today_date))
            rows = cursor.fetchall()
            
            print(f"\n--- Waiting List for Doctor ID {doctor_id} today ---")
            if not rows:
                print("No patients in queue yet.")
            else:
                for row in rows:
                    print(f"Ticket #{row[0]} | Patient: {row[1]} | Time: {row[2].split()[1]} | Status: {row[3]}")
            return rows
        except Exception as e:
            print(f"Error fetching queue: {e}")
            return []
