from .person import Person



class Doctor(Person):
    def __init__(self, id, name, specialization, department):
        super().__init__(id, name)

        self.specialization = specialization
        self.department = department


    def save_to_db(self, cursor, conn):
        query = "INSERT INTO doctors (id, name, specialization, department) VALUES (%s, %s, %s, %s,%s)"
        values = (self.id, self.name, self.specialization, self.department)
        cursor.execute(query, values)
        conn.commit()