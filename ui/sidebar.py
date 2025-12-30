import customtkinter as ctk
from .styles import HEADER_FONT, BODY_FONT
class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, width=200, corner_radius=0)
        self.controller = controller
        self.dashboard = parent  # Store reference to DashboardScreen
        self.pack(side="left", fill="y")
        self.pack_propagate(False) # Enforce width

        logo_label = ctk.CTkLabel(self, text="🏥 HMS", font=HEADER_FONT)
        logo_label.pack(pady=30)

        # self.create_nav_btn("Dashboard", "DashboardHome") 
        self.create_nav_btn("Patients", "PatientsView")
        self.create_nav_btn("Doctors", "DoctorsView")
        self.create_nav_btn("Appointments", "AppointmentsView")
        self.create_nav_btn("Users", "users_view")
        # self.create_nav_btn("Billing", "BillingView")
        
        ctk.CTkFrame(self, fg_color="transparent").pack(fill="both", expand=True)

        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self, values=["System", "Light", "Dark"],
                                                               command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.pack(padx=20, pady=10)
        self.appearance_mode_optionemenu.set("System")

        logout_btn = ctk.CTkButton(self, text="Logout",
                                    font=BODY_FONT, 
                                    fg_color="transparent",
                                    border_width=2,
                                    text_color=("gray10", "gray90"),
                                    hover_color=("gray70", "gray30"),
                                    command=lambda: self.controller.show_frame("LoginView"))

        logout_btn.pack(fill="x", pady=20, padx=20)

    def create_nav_btn(self, text, view_name):
        btn = ctk.CTkButton(self, text=text,
                            font=BODY_FONT, 
                            fg_color="transparent", 
                            text_color=("gray10", "gray90"),
                            hover_color=("gray70", "gray30"), 
                            anchor="w", 
                            command=lambda: self.check_frame(view_name)
                            )

        btn.pack(fill="x", pady=2, padx=10)

    def check_frame(self, view_name):
        self.controller.show_frame(view_name)
        if view_name == "users_view":
            users_view = self.controller.frames[view_name]
            users_view.get_all_users()
            users_view.count_all_users()
            users_view.count_secretary_users()
            users_view.count_admin_users()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
