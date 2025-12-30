import customtkinter as ctk
import PIL
from backend.models.user import User
from backend.controllers.auth import Auth

class SignUpView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ctk.set_appearance_mode("light")

        bg_color = "#C3E9ED"
        self.configure(fg_color=bg_color)
        self.grid_rowconfigure(0 , weight=1)
        self.grid_columnconfigure(0 , weight=1)
        
        frame = ctk.CTkFrame(self , fg_color="white" , width=1100 , height=600 )
        frame.grid(row=0, column=0)
        frame.grid_propagate(False)


        frame.grid_rowconfigure(0 , weight=1)
        frame.grid_columnconfigure(0 , weight=1)
        frame.grid_columnconfigure(1 , weight=1)
        image_frame = ctk.CTkFrame(frame , fg_color="#2DEBFF", corner_radius=40)
        image_frame.grid(row=0 , column=0 , sticky="nsew")
        image_frame.grid_propagate(False)
        image_frame.grid_rowconfigure(0 , weight=1)
        image_frame.grid_columnconfigure(0 , weight=1)

        hospital_image = PIL.Image.open("assets/images/hospital_image.png")
        hospital_image = ctk.CTkImage(hospital_image, size=(600,600))
        
        image_label = ctk.CTkLabel(image_frame , image=hospital_image , text="")
        image_label.grid(row=0 , column=0,sticky="nsew")

        hospital_logo = PIL.Image.open("assets/images/hos_logo.png")
        hospital_logo_image = ctk.CTkImage(hospital_logo, size=(100,100))

        form_frame = ctk.CTkFrame(frame , fg_color="white")
        form_frame.grid(row=0 , column=1 , sticky="nsew")
        form_frame.grid_propagate(False)

        form_frame.grid_rowconfigure(0 , weight=1)
        form_frame.grid_rowconfigure(1 , weight=0)

        form_frame.grid_rowconfigure(2 , weight=1)
        form_frame.grid_rowconfigure(3 , weight=2)
        form_frame.grid_rowconfigure(4 , weight=0)
        form_frame.grid_rowconfigure(5 , weight=2)
        form_frame.grid_rowconfigure(6 , weight=2)
        form_frame.grid_rowconfigure(7 , weight=2)
        form_frame.grid_rowconfigure(8 , weight=0)
        form_frame.grid_rowconfigure(9 , weight=0)

        form_frame.grid_columnconfigure(0 , weight=1)


        label_form_image = ctk.CTkLabel(form_frame , image=hospital_logo_image , text="")
        label_form_image.grid(row=0 , column=0)
        label_form = ctk.CTkLabel(form_frame , text="HMS" , font=("Aptos", 20 , "bold") , text_color="#00A9B0")
        label_form.grid(row=1 , column=0 , padx=20,sticky="n" )

        label_welcome = ctk.CTkLabel(form_frame , text="Welcome To HMS" , font=("Aptos", 32 , "bold") , text_color="#00A9B0")
        label_welcome.grid(row=2 , column=0 , sticky="w", padx=20)
        self.username_entry = ctk.CTkEntry(form_frame , corner_radius=40 , border_width=0, font=("Aptos", 17) , placeholder_text="Username",bg_color="transparent")
        self.username_entry.grid(row=3 , column=0 , sticky="nsew" , padx= 20 , pady=20)

        self.password_entry = ctk.CTkEntry(form_frame , show="*", corner_radius=40 , border_width=0, font=("Aptos", 17) , placeholder_text="Password",bg_color="transparent")
        self.password_entry.grid(row=5 , column=0 , sticky="nsew" , padx= 20 )

        self.confirm_password_entry = ctk.CTkEntry(form_frame , show="*", corner_radius=40 , border_width=0, font=("Aptos", 17) , placeholder_text="Confirm Password",bg_color="transparent")
        self.confirm_password_entry.grid(row=6 , column=0 , sticky="nsew" , padx= 20 , pady=20)

        sign_up_button = ctk.CTkButton(form_frame , text="Create Account" , font=("Aptos", 15 , "bold") , text_color="white" , fg_color="#00A9B0", command=self.handle_signup)
        sign_up_button.grid(row=7 , column=0 , sticky="nsew" , padx= 20 , pady=20)

        have_account_frame = ctk.CTkFrame(form_frame , fg_color="transparent")
        have_account_frame.grid(row=8 , column=0 , sticky="nsew" , padx= 20)

        have_account_frame.grid_rowconfigure(0 , weight=0)
        have_account_frame.grid_columnconfigure(0 , weight=1)
        have_account_frame.grid_rowconfigure(1 , weight=0)

        have_account_label = ctk.CTkLabel(have_account_frame , text="Already have an account?" , font=("Aptos", 15) , text_color="#00A9B0")
        have_account_label.grid(row=0 , column=0 , sticky="ew")

        login_button = ctk.CTkButton(have_account_frame , text="Login" , font=("Aptos", 15 , "bold") , text_color="black" , fg_color="transparent",hover_color="white", command=lambda: self.controller.show_frame("LoginView"))
        login_button.grid(row=1 , column=0 )

        self.error_label = ctk.CTkLabel(form_frame , text="", text_color="red")
        self.error_label.grid(row=9 , column=0 , sticky="nsew" , padx= 20 , pady=20)


    def handle_signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        if password != confirm_password:
            self.error_label.configure(text="Passwords do not match")
            return

        auth = Auth()
        result , message = auth.signUp(username, password)
        
        if result:
            self.error_label.configure(text=message)
            self.controller.show_frame("LoginView")
        else:
            self.error_label.configure(text=message)


