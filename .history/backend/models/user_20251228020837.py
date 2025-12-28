from backend.models.person import Person
import backend.database.connectDB as connectDB
class User(Person):
    def __init__(self, username, password,):
        super().__init__(username,age="",gender="",phone="",email="")
        self.username = username
        self.__password = password

        


    def set_password(self, password):
        self.__password = password
    def get_password(self):
        return self.__password


    @staticmethod
    def create_table():
        conn = connectDB.connect()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password BLOB NOT NULL,
            role TEXT NOT NULL 
            CHECK (role IN ('admin', 'secretary')) 
            DEFAULT 'secretary',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.commit()
        print("User table created successfully.")


    def save_to_db(self):
        conn = connectDB.connect()
        cursor = conn.cursor()
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        values = (self.username, self.get_password())
        cursor.execute(query, values)
        conn.commit()
        print(f"User {self.username} saved to database successfully.")


    @staticmethod
    def get_user_by_username(username):
        conn = connectDB.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        return cursor.fetchone()

    @staticmethod
    def update_user_info(self,new_user, new_password):
        conn = connectDB.connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET username = ?, password = ? WHERE id = ?",
            (new_username, new_password, user_id)
        )
        conn.commit()
        print(f"User with id {user_id} updated successfully.")
