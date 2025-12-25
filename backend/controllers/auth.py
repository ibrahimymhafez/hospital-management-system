import bcrypt
from backend.models.user import User
class Auth:
    def __init__(self):
        self.__curr_user = None

    def signUp(self, username, password):
        try:
            hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user = User(username, hashedPassword)
            user1 = user.get_user_by_username(username)
            if user1:
                raise Exception("User already exists.")
            else:
                user.save_to_db()
        except Exception as e:
            print(f"Unexpected error: {e}")


    def signIn(self, username, password):
        try:
            user = User(username, password)
            user1 = user.get_user_by_username(username)
            if user1:
                if bcrypt.checkpw(password.encode('utf-8'), user1[2]):
                    self.curr_user = user
                    print("Login successful.")
                else:
                    raise Exception("Incorrect password.")
            else:
                raise Exception("User not found.")
        except Exception as e:
            print(f"Unexpected error ----> : {e}")