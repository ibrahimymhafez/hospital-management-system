import customtkinter as ctk
from ui.login_view import LoginView
from ui.signup_view import SignUpView
from ui.appointments_view import AppointmentsView
from ui.doctors_view import DoctorsView
from ui.patients_view import PatientsView
from ui.users_view import users_view
from ui.sidebar import Sidebar

class HospitalApp(ctk.CTk):  
    def __init__(self):
        super().__init__()

        self.title("Hospital Management System") 
        self.geometry("1200x700")

    
        # Configure grid for sidebar and main content
        self.grid_columnconfigure(0, weight=0) # Sidebar column (fixed width)
        self.grid_columnconfigure(1, weight=1) # Content column (expandable)
        self.grid_rowconfigure(0, weight=1)

        # Initialize Sidebar (hidden initially)
        self.sidebar = Sidebar(self, self)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_remove() # Hide initially

        # Container for views
        self.container = ctk.CTkFrame(self)         
        self.container.grid(row=0, column=1, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.__current_user = None

        self.frames = {}
        
        for F in (LoginView, SignUpView, AppointmentsView, DoctorsView, PatientsView, users_view):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginView")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        
        # Toggle Sidebar Visibility based on view
        if page_name in ["LoginView", "SignUpView"]:
            self.sidebar.grid_remove()
            self.container.grid(row=0, column=0, columnspan=2, sticky="nsew") # Expand container
            self.resizable(False, False)
        else:
            self.sidebar.grid(row=0, column=0, sticky="nsew")
            self.container.grid(row=0, column=1, columnspan=1, sticky="nsew") # Reset container
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
