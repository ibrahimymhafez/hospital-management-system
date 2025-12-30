import backend.database.connectDB as connectDB
from backend.models.doctor import Doctor
from backend.models.user import User
from backend.controllers.auth import Auth


import customtkinter as ctk
from UI.login_view import LoginView
from UI.dummy_dashboard import DashboardScreen
from UI.signup_view import SignUpView
from UI.appointments_view import AppointmentsView
    
class HospitalApp(ctk.CTk):  
    def __init__(self):
        super().__init__()

        self.title("Hospital Management System") 
        self.geometry("1100x700")

        self.container = ctk.CTkFrame(self)         
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.__current_user = None

        self.frames = {}
        
        for F in (LoginView, DashboardScreen, SignUpView, AppointmentsView):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginView")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if page_name == "SignUpView" or page_name == "LoginView":
            self.resizable(False, False)
        else:
            self.resizable(True, True)
        frame.tkraise()

    def set_current_user(self, user):
        self.__current_user = user
    
    def get_current_user(self):
        return self.__current_user
    
def main():
    hospital_app = HospitalApp()
    hospital_app.mainloop()

if __name__ == "__main__":
    main()
  
