import customtkinter as ctk
import PIL
from backend.models.user import User
from backend.controllers.auth import Auth


class LoginView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ctk.set_appearance_mode("light")

        controller.title("Login Window")

        self.bg_color = "#C3E9ED"
        self.configure(fg_color=self.bg_color)
        self.grid_rowconfigure(0 , weight=1)
        self.grid_columnconfigure(0 , weight=1)
        
        self.frame = ctk.CTkFrame(self , fg_color="white" , width=1100 , height=600 )
        self.frame.grid(row=0, column=0)
        self.frame.grid_propagate(False)


        self.frame.grid_rowconfigure(0 , weight=1)
        self.frame.grid_columnconfigure(0 , weight=1)
        self.frame.grid_columnconfigure(1 , weight=1)
        self.image_frame = ctk.CTkFrame(self.frame , fg_color="#2DEBFF", corner_radius=40)
        self.image_frame.grid(row=0 , column=0 , sticky="nsew")
        self.image_frame.grid_propagate(False)
        self.image_frame.grid_rowconfigure(0 , weight=1)
        self.image_frame.grid_columnconfigure(0 , weight=1)

        self.hospital_image = PIL.Image.open("assets/images/hospital_image.png")
        self.hospital_image = ctk.CTkImage(self.hospital_image, size=(600,600))
        
        self.image_label = ctk.CTkLabel(self.image_frame , image=self.hospital_image , text="")
        self.image_label.grid(row=0 , column=0,sticky="nsew")

        self.hospital_logo = PIL.Image.open("assets/images/hos_logo.png")
        self.hospital_logo_image = ctk.CTkImage(self.hospital_logo, size=(100,100))

        self.form_frame = ctk.CTkFrame(self.frame , fg_color="white")
        self.form_frame.grid(row=0 , column=1 , sticky="nsew")
        self.form_frame.grid_propagate(False)

        self.form_frame.grid_rowconfigure(0 , weight=1)
        self.form_frame.grid_rowconfigure(1 , weight=0)

        self.form_frame.grid_rowconfigure(2 , weight=1)
        self.form_frame.grid_rowconfigure(3 , weight=1)
        self.form_frame.grid_rowconfigure(4 , weight=0)
        self.form_frame.grid_rowconfigure(5 , weight=1)
        self.form_frame.grid_rowconfigure(6 , weight=1)
        self.form_frame.grid_rowconfigure(7 , weight=0)
        self.form_frame.grid_rowconfigure(8 , weight=0)

        self.form_frame.grid_columnconfigure(0 , weight=1)


        self.label_form_image = ctk.CTkLabel(self.form_frame , image=self.hospital_logo_image , text="")
        self.label_form_image.grid(row=0 , column=0)
        self.label_form = ctk.CTkLabel(self.form_frame , text="HMS" , font=("Aptos", 20 , "bold") , text_color="#00A9B0")
        self.label_form.grid(row=1 , column=0 , sticky="n" )

        self.label_welcome = ctk.CTkLabel(self.form_frame , text="Welcome Back" , font=("Aptos", 32 , "bold") , text_color="#00A9B0")
        self.label_welcome.grid(row=2 , column=0 , sticky="w", padx=20)
        self.username_entry = ctk.CTkEntry(self.form_frame , corner_radius=40 , border_width=0, font=("Aptos", 17) , placeholder_text="Username",bg_color="transparent")
        self.username_entry.grid(row=3 , column=0 , sticky="nsew" , padx= 20 , pady=20)

        self.password_entry = ctk.CTkEntry(self.form_frame , show="*", corner_radius=40 , border_width=0, font=("Aptos", 17) , placeholder_text="Password",bg_color="transparent")
        self.password_entry.grid(row=5 , column=0 , sticky="nsew" , padx= 20 , pady=20)

        self.login_button = ctk.CTkButton(self.form_frame , text="Login" , font=("Aptos", 15) , text_color="white" , fg_color="#00A9B0", command=self.handle_login)
        self.login_button.grid(row=6 , column=0 , sticky="nsew" , padx= 20 , pady=20)

        self.have_account_frame = ctk.CTkFrame(self.form_frame , fg_color="transparent")
        self.have_account_frame.grid(row=7 , column=0 , sticky="nsew" , padx= 20)

        self.have_account_frame.grid_rowconfigure(0 , weight=0)
        self.have_account_frame.grid_columnconfigure(0 , weight=1)
        self.have_account_frame.grid_rowconfigure(1 , weight=0)

        self.have_account_label = ctk.CTkLabel(self.have_account_frame , text="Don't have an account?" , font=("Aptos", 15) , text_color="#00A9B0")
        self.have_account_label.grid(row=0 , column=0 , sticky="ew")

        self.signup_button = ctk.CTkButton(self.have_account_frame , text="Create Account" , font=("Aptos", 15 , "bold") , text_color="black" , fg_color="transparent",hover_color="white", command=lambda: self.controller.show_frame("SignUpView"))
        self.signup_button.grid(row=1 , column=0 )

        self.error_label = ctk.CTkLabel(self.form_frame , text="", text_color="red")
        self.error_label.grid(row=8 , column=0 , sticky="nsew" , padx= 20 , pady=20)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username and not password:
            self.error_label.configure(text="Please enter valid credentials")
            return

        auth = Auth()
        result , user_data = auth.signIn(username, password)
        
        if result:
            self.controller.set_current_user(user_data)
            self.controller.show_frame("AppointmentsView")
            print(user_data)
        else:
            self.error_label.configure(text=user_data)

