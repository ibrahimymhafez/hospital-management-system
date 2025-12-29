import customtkinter as ctk
import PIL
from tkinter import ttk, messagebox
from backend.models.user import User
import bcrypt
from backend.controllers.auth import Auth
class users_view(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)
        
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=10, fill="both", expand=True)

        top_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        top_frame.pack(fill="x", pady=25)

        label = ctk.CTkLabel(top_frame,text="Users Management",font=("Roboto Medium", 16))
        label.pack(side="left", padx=10)

        buttons_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        buttons_frame.pack(side="right", padx=10)
        add_button = ctk.CTkButton(buttons_frame, text="Add User", fg_color="green",command=self.add_user)
        add_button.pack(side="left", padx=5)
        update_button = ctk.CTkButton(buttons_frame, text="Update User",command=self.update_user)
        update_button.pack(side="left", padx=5)
        delete_button = ctk.CTkButton(buttons_frame, text="Delete User", fg_color="red",command=self.delete_user)
        delete_button.pack(side="left", padx=5)

        bottom_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        bottom_frame.pack(fill="both", expand=True)

        analyze_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        analyze_frame.pack(fill="x", pady=10)
        analyze_frame.grid_columnconfigure(0, weight=1)
        analyze_frame.grid_columnconfigure(1, weight=1)
        analyze_frame.grid_columnconfigure(2, weight=1)

        count_all_users_frame = ctk.CTkFrame(analyze_frame, fg_color="#BEDBFF")
        count_all_users_frame.grid(row=0, column=0, sticky="nsew", padx=20)
        count_all_users_frame.grid_columnconfigure(0, weight=1)
        count_all_users_frame.grid_columnconfigure(1, weight=1)
        count_all_users_frame.grid_rowconfigure(0, weight=1)
        count_all_users_frame.grid_rowconfigure(1, weight=1)
        count_all_users_image = PIL.Image.open("assets/images/users.png")
        count_all_users_image = ctk.CTkImage(count_all_users_image, size=(100,100))
        count_all_users_label_image = ctk.CTkLabel(count_all_users_frame,text="",image=count_all_users_image)
        count_all_users_label_image.grid(row=0, column=0, rowspan=2, sticky="w", padx=10,pady=10)
        count_all_users_label = ctk.CTkLabel(count_all_users_frame,text="All Users",font=("Roboto Medium", 24),text_color="#1E3A8A")
        count_all_users_label.grid(row=0, column=1, sticky="ew", pady=(10, 0),padx = 10)
        self.count_all_users_count = ctk.CTkLabel(count_all_users_frame,text= User.count_all_users(),font=("Roboto Medium", 24),text_color="#1E3A8A")
        self.count_all_users_count.grid(row=1, column=1, sticky="ew", pady=(0, 10))



        count_secretary_users_frame = ctk.CTkFrame(analyze_frame, fg_color="#E6FDED")
        count_secretary_users_frame.grid_columnconfigure(0, weight=1)
        count_secretary_users_frame.grid_columnconfigure(1, weight=1)
        count_secretary_users_frame.grid(row=0, column=1, sticky="nsew", padx=20)
        count_secretary_users_image = PIL.Image.open("assets/images/user.png")
        count_secretary_users_image = ctk.CTkImage(count_secretary_users_image, size=(100,100))
        count_secretary_users_label_image = ctk.CTkLabel(count_secretary_users_frame,text="",image=count_secretary_users_image)
        count_secretary_users_label_image.grid(row=0, column=0, rowspan=2, sticky="w", padx=10,pady=10)
        count_secretary_users_label = ctk.CTkLabel(count_secretary_users_frame,text="Secretary Users",font=("Roboto Medium", 24),text_color="#14532D")
        count_secretary_users_label.grid(row=0, column=1, sticky="ew", pady=(10, 0),padx=10)
        self.count_secretary_users_count = ctk.CTkLabel(count_secretary_users_frame,text= User.count_secretary_users(),font=("Roboto Medium", 24),text_color="#14532D")
        self.count_secretary_users_count.grid(row=1, column=1, sticky="ew", pady=(0, 10),padx=10)


        count_admin_users_frame = ctk.CTkFrame(analyze_frame, fg_color="red")
        count_admin_users_frame.grid_columnconfigure(0, weight=1)
        count_admin_users_frame.grid_columnconfigure(1, weight=1)
        count_admin_users_frame.grid_rowconfigure(0, weight=1)
        count_admin_users_frame.grid_rowconfigure(1, weight=1)
        count_admin_users_frame.grid(row=0, column=2, sticky="nsew", padx=20)
        count_admin_users_image = PIL.Image.open("assets/images/admin.png")
        count_admin_users_image = ctk.CTkImage(count_admin_users_image, size=(100,100))
        count_admin_users_label_image = ctk.CTkLabel(count_admin_users_frame,text="",image=count_admin_users_image)
        count_admin_users_label_image.grid(row=0, column=0, rowspan=2, sticky="w", padx=10,pady=10)
        count_admin_users_label = ctk.CTkLabel(count_admin_users_frame,text="Admin Users",font=("Roboto Medium", 24),text_color="white")
        count_admin_users_label.grid(row=0, column=1, sticky="ew", pady=(10, 0),padx=10)
        self.count_admin_users_count = ctk.CTkLabel(count_admin_users_frame,text= User.count_admin_users(),font=("Roboto Medium", 24),text_color="white")
        self.count_admin_users_count.grid(row=1, column=1, sticky="ew", pady=(0, 10))


        search_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        search_frame.pack(fill="x",pady=15,padx=10)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search ...",
            width=300
        )
        self.search_entry.pack(side="left",fill="x",expand=True, padx=10)

        search_button = ctk.CTkButton(
            search_frame, text="Search", command=self.search_users
        )
        search_button.pack(side="left")

        tree_frame = ctk.CTkFrame(bottom_frame) 
        tree_frame.pack(fill="both", expand=True)

        cols = ("ID", "Username", "Role", "Created At")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings")
        self.get_all_users()
                
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
            
        self.tree.pack(fill="both", expand=True)

    def get_all_users(self):
           users = User.get_all_users()
           self.tree.delete(*self.tree.get_children())
           for user in users:
               self.tree.insert("", "end", values=(user[0], user[1], user[3], user[4]))

    def search_users(self):
            search_text = self.search_entry.get()
            if search_text.strip() == "":
                self.get_all_users()
                return
            
            users = User.search_users(search_text)
            self.tree.delete(*self.tree.get_children())
            for user in users:
                self.tree.insert("", "end", values=(user[0], user[1], user[3], user[4]))
    
    def delete_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a user to delete")
            return
        if self.controller.get_current_user()[3] != "admin":
            messagebox.showerror("Error", "You are not authorized to delete users")
            return
        user_id = self.tree.item(selected_item)['values'][0]
        User.delete_user(user_id)
        self.get_all_users()
        self.count_all_users()
        self.count_secretary_users()
        self.count_admin_users()

    def update_user(self):
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a user to update")
                return
            if self.controller.get_current_user()[3] != "admin":
                messagebox.showerror("Error", "You are not authorized to update users")
                return
        
            user_id = self.tree.item(selected_item)['values'][0]
            self.dialog = ctk.CTkToplevel(self.controller)

            self.dialog.title("Update User")
            self.dialog.geometry("400x300")
            label = ctk.CTkLabel(self.dialog, text="Update User")
            label.pack(pady=10)
            username_entry = ctk.CTkEntry(self.dialog,placeholder_text="Username")
            username_entry.insert(0,self.tree.item(selected_item)['values'][1])
            username_entry.pack(pady=10)
            role_dropdown = ctk.CTkComboBox(self.dialog, values=["admin", "secretary"])
            role_dropdown.set(self.tree.item(selected_item)['values'][2])
            role_dropdown.pack(pady=10)
            password_entry = ctk.CTkEntry(self.dialog)
            password_entry.pack(pady=10)

            update_button = ctk.CTkButton(
                self.dialog,
                text="Update Info",
                command=lambda: self.update_user_validation(user_id,username_entry.get(), password_entry.get(), role_dropdown.get()))
            update_button.pack(pady=10)
            self.error_label = ctk.CTkLabel(self.dialog, text="", text_color="red")
            self.error_label.pack(pady=10)
    def update_user_validation(self,user_id,username,password,role):
        try:
            if len(password) < 8:
                self.error_label.configure(text="Password must be at least 8 characters long.")
                return
            if password.isdigit():
                self.error_label.configure(text="Password must contain at least one letter.")
                return
            if password.isalpha():
                self.error_label.configure(text="Password must contain at least one number.")
                return
            if password.isalnum():
                self.error_label.configure(text="Password must contain at least one special character.")
                return
            if not any(char.isupper() for char in password):
                self.error_label.configure(text="Password must contain at least one uppercase letter.")
                return
            if password.strip() == "":
                self.error_label.configure(text="Password cannot be empty.")
                return
            if username.strip() == "":
                self.error_label.configure(text="Username cannot be empty.")
                return
            if role.strip() == "":
                self.error_label.configure(text="Role cannot be empty.")
                return
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            User.update_user_info(user_id,username,hashed_password,role)
            self.get_all_users()
            self.count_secretary_users()
            self.count_admin_users()
            self.dialog.destroy()
        except Exception as e:
            self.error_label.configure(text =  str(e))


    def add_user(self):
        if self.controller.get_current_user()[3] != "admin":
            messagebox.showerror("Error", "You are not authorized to add users")
            return
        self.dialog2 = ctk.CTkToplevel(self.controller)
        self.dialog2.title("Add User")
        self.dialog2.geometry("400x300")
        label = ctk.CTkLabel(self.dialog2, text="Add User")
        label.pack(pady=10)
        self.username_entry = ctk.CTkEntry(self.dialog2,placeholder_text="Username")
        self.username_entry.pack(pady=10)
        self.password_entry = ctk.CTkEntry(self.dialog2,placeholder_text="Password",show="*")
        self.password_entry.pack(pady=10)
        self.error_label = ctk.CTkLabel(self.dialog2, text="", text_color="red")
        self.error_label.pack(pady=10)

        add_button = ctk.CTkButton(
            self.dialog2,
            text="Add User",
            command=self.handle_add_user)
        add_button.pack(pady=10)
        self.error_label2 = ctk.CTkLabel(self.dialog2, text="", text_color="red")
        self.error_label2.pack(pady=10)

    def handle_add_user(self):
            result , message = Auth.signUp(self.username_entry.get(), self.password_entry.get())
            if result:
                self.get_all_users()
                self.count_all_users()
                self.count_secretary_users()
                self.count_admin_users()
                self.dialog2.destroy()
            else:
                self.error_label2.configure(text=message)

    def count_all_users(self):
        User.count_all_users()
        self.count_all_users_count.configure(text=User.count_all_users())
    def count_secretary_users(self):
        User.count_secretary_users()
        self.count_secretary_users_count.configure(text=User.count_secretary_users())
    def count_admin_users(self):
        User.count_admin_users()
        self.count_admin_users_count.configure(text=User.count_admin_users())




    