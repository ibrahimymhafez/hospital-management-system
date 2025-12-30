import customtkinter as ctk
from ui.sidebar import Sidebar
from ui.patients_view import PatientsView
from ui.doctors_view import DoctorsView
# from ui.appointments_view import AppointmentsView
# from ui.billing_view import BillingView

class DashboardScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        # Dashboard Layout: Sidebar (Left) + Content (Right)
        # Sidebar
        self.sidebar = Sidebar(self, controller)
        
        # Content Area - Using transparent frame to just hold content
        self.content_area = ctk.CTkFrame(self, fg_color="transparent")
        self.content_area.pack(side="right", fill="both", expand=True)
        
        # Store views cache
        self.views = {}
        self.current_view = None
        
        self.show_welcome()

    def show_welcome(self):
        self.clear_content()
        self.current_view = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.current_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(self.current_view, text="Welcome to the Dashboard", font=("Roboto Medium", 24)).pack(pady=40)
        
        ctk.CTkLabel(self.current_view, text="Select an option from the sidebar to get started.", 
                 font=("Roboto", 14)).pack()

    def show_view(self, view_class_name):
        self.clear_content()
        
        # Map class names to classes
        view_mapping = {
            "PatientsView": PatientsView,
            "DoctorsView": DoctorsView
            # "AppointmentsView": AppointmentsView,
            # "BillingView": BillingView
        }
        
        ViewClass = view_mapping.get(view_class_name)
        
        if ViewClass:
            # Pass content_area as parent
            self.current_view = ViewClass(self.content_area)
            self.current_view.pack(fill="both", expand=True, padx=20, pady=20)
        else:
            # Fallback
            self.current_view = ctk.CTkFrame(self.content_area)
            self.current_view.pack(fill="both", expand=True, padx=20, pady=20)
            ctk.CTkLabel(self.current_view, text=f"{view_class_name} is under construction.", 
                     font=("Roboto", 18)).pack(pady=20)

    def clear_content(self):
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None
