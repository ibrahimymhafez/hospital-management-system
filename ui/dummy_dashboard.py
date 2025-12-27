import customtkinter as ctk
import PIL
from backend.models.user import User
from backend.controllers.auth import Auth


class DashboardScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        controller.title("Dashboard")
        controller.geometry("1200x700")
        self.frame = ctk.CTkFrame(self , fg_color="white" , width=1100 , height=600 )
        self.frame.pack(fill="both" , expand=True)
        self.frame.pack_propagate(False)
        self.label = ctk.CTkLabel(self.frame , text="Dashboard" , font=("Aptos" , 20 , "bold"))
        self.label.pack(pady=20)
        self.label.pack_propagate(False)