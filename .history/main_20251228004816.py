import backend.database.connectDB as connectDB
from backend.models.doctor import Doctor
from backend.models.user import User
from backend.controllers.auth import Auth
import customtkinter as ctk
from UI.doctors_view import DoctorsView
from UI.patients_view import PatientsView
# from UI.login_screen import LoginScreen
# from UI.dashboard_screen import DashboardScreen

    
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
        
        for F in (DoctorsView, PatientsView):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("PatientsView")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
    
  
    # HospitalApp = HospitalApp()
    # HospitalApp.mainloop()

def main():
    Doctor =  DoctorsView()
    Doctor.mainloop()
if __name__ == "__main__":
    main()