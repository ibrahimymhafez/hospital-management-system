from backend.models.person import Person
import backend.database.connectDB as connectDB
import bcrypt
class User(Person):
    def __init__(self, username, password,age="",gender="",phone="",email=""):
        super().__init__(username,age,gender,phone,email)
        self.__username = username
        self.__password = password


    def set_password(self, password):
        self.__password = password
    def get_password(self):
        return self.__password

    def set_username(self, username):
        self.__username = username
    def get_username(self):
        return self.__username



    def create_table(self):
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
        values = (self.get_username(), self.get_password())
        cursor.execute(query, values)
        conn.commit()
        print(f"User {self.get_username()} saved to database successfully.")

    @staticmethod
    def get_user_by_username(username):
        conn = connectDB.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        return cursor.fetchone()

    @staticmethod
    def update_user_info(user_id, new_username, new_password ,role):
        conn = connectDB.connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET username = ?, password = ?, role = ? WHERE id = ?",
            (new_username, new_password, role, user_id)
        )
        conn.commit()
        print(f"User with id {user_id} updated successfully.")

    @staticmethod
    def count_all_users():
        conn = connectDB.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        return cursor.fetchone()[0]
    
    @staticmethod
    def count_secretary_users():
        conn = connectDB.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'secretary'")
        return cursor.fetchone()[0]
    
    @staticmethod
    def count_admin_users():
        conn = connectDB.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
        return cursor.fetchone()[0]
    
    @staticmethod
    def get_all_users():
        conn = connectDB.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()

    @staticmethod
    def search_users(text):
        conn = connectDB.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username LIKE ?", (f"%{text}%",))
        return cursor.fetchall()

    @staticmethod
    def delete_user(user_id):
        conn = connectDB.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        print(f"User with id {user_id} deleted successfully.")