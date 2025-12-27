import backend.database.connectDB as connectDB
from backend.models.doctor import Doctor
from backend.models.user import User
from backend.controllers.auth import Auth


import customtkinter as ctk
from UI.login_view import LoginView
# from UI. import DashboardScreen

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
    
class HospitalApp(ctk.CTk):  #this creates the main window
    def __init__(self):
        super().__init__()

        self.title("Hospital Management System") #title of the main window
        self.geometry("1100x700")

        self.container = ctk.CTkFrame(self)         
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        # this creates both the log in screen and the dashboard, the login screen opens first and switches to the dashboard after entering creditials
        for F in (LoginView, DashboardScreen):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginScreen")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
    
if __name__ == "__main__":
    main()
  
    HospitalApp = HospitalApp()
    HospitalApp.mainloop()
