from .person import Person

class Patient(Person):
    def __init__(self, name, age, phone):
        super().__init__(name)
        self.age = age
        self.phone = phone

    def save_to_db(self, cursor, conn):
        query = "INSERT INTO doctors (name, age, phone) VALUES (%s, %s,%s)"
        values = (self.name, self.age, self.phone)
        cursor.execute(query, values)
        conn.commit()

    def delete_from_db(self, cursor, conn, id):
        cursor.execute(f"delete from doctors where id = '{id}'") 
        conn.commit
