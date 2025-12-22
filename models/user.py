from models.person import Person
import database.connectDB as connectDB
class User(Person):
    def __init__(self, username, password):
        super().__init__(username)
        self.username = username
        self._password = password
    def set_password(self, password):
        self._password = password
    def get_password(self):
        return self._password

    def create_table(self,cursor, conn):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL 
            CHECK (role IN ('admin', 'secretary')) 
            DEFAULT 'secretary',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.commit()
        print("User table created successfully.")


    def save_to_db(self, cursor, conn):
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        values = (self.username, self.get_password())
        cursor.execute(query, values)
        conn.commit()
        print(f"User {self.username} saved to database successfully.")


    def update_user_info(self, cursor, conn, user_id, new_username, new_password):
        cursor.execute(
            "UPDATE users SET username = ?, password = ? WHERE id = ?",
            (new_username, new_password, user_id)
        )
        conn.commit()
        print(f"User with id {user_id} updated successfully.")
