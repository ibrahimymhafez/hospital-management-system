import database.connectDB as connectDB
from models.doctor import Doctor
def main():
    connect = connectDB.connect()
    cursor = connect.cursor()
    doctor = Doctor("lol", "surgery", department_id=1)
    doctor.save_to_db(cursor, connect)
    # doctor.delete_from_db(cursor, connect, 73)
    

    
if __name__ == "__main__":
    main()