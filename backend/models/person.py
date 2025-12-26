class Person:
    def __init__(self, name, age, gender, phone, email):
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone
        self.email = email
        
    def save_to_db(self, cursor, conn):
        pass 

    def delete_from_db(cursor, conn, person_id):
        pass

    def update_info(self, cursor, conn, person_id):
        pass
