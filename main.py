import database.connectDB as connectDB
from models.doctor import Doctor
from models.user import User
from controllers.auth import Auth
def main():
    # doctor = Doctor("lol", "surgery", department_id=1)
    
    # doctor.save_to_db(cursor, connect)
    # doctor.delete_from_db(cursor, connect, 73)
    

    # user = User("Ahmed", "12345678")
    # auth.signUp("Ahmed", "12345678")
    user = User("Ahmed", "12345678")
    auth = Auth()
    # auth.signUp("Ahmed", "12345678")
    auth.signIn("Ahmed", "123456788")
    # user.create_table(cursor, connect)
    # user.update_user_info(cursor, connect, 1, "AhmedYoussef", "123456789898")
    
if __name__ == "__main__":
    main()