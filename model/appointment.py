

class Appointment:
    def __init__(self, patient, doctor, day):
        self.patient = patient
        self.doctor = doctor
        self.day = day



    def save_to_db(self, cursor, conn):
        query = "insert into appointments(patient_id, doctor_id, day)"
        values = (self.patient, self.doctor, self.day )
        cursor.execute(query, values)
        conn.commit

        

        