import bcrypt
from backend.models.user import User
class Auth:
    def __init__(self):
        self.__curr_user = None

    def signUp(self, username, password):
        try:
            hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user = User(username.lower(), hashedPassword)
            user1 = user.get_user_by_username(username.lower())
            if user1:
                raise Exception("User already exists.")
            
            if len(password) < 8:
                raise Exception("Password must be at least 8 characters long.")
            if password.isdigit():
                raise Exception("Password must contain at least one letter.")
            if password.isalpha():
                raise Exception("Password must contain at least one number.")
            if password.isalnum():
                raise Exception("Password must contain at least one special character.")
            if not any(char.isupper() for char in password):
                raise Exception("Password must contain at least one uppercase letter.")

            user.save_to_db()
            return True , "User created successfully."
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False , str(e)


    def signIn(self, username, password):
        try:
            user = User(username.lower(), password)
            user.create_table()
            user_data = user.get_user_by_username(username.lower())
            if not user_data:
                raise Exception("User not found.")
            if not bcrypt.checkpw(password.encode('utf-8'), user_data[2]):
                raise Exception("Incorrect password.")
            return True,user_data
        except Exception as e:
            print(f"Unexpected error ----> : {e}")
            return False , str(e)