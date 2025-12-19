from .person import Person

class Doctor(Person):
    def __init__(self, name, specialization, department):
        super().__init__(name)
        self.specialization = specialization
        self.department = department


    def save_to_db(self, cursor, conn):
        query = "INSERT INTO doctors (name, specialization, department) VALUES (%s, %s, %s, %s,%s)"
        values = (self.id, self.name, self.specialization, self.department)
        cursor.execute(query, values)
        conn.commit()

    def delete_from_db(self, cursor, conn, id):
        cursor.execute(f"delete from doctors where id = '{id}'") 
        conn.commit()
