import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from backend.models.doctor import Doctor
from backend.database.connectDB import connect
from .styles import HEADER_FONT, BODY_FONT



class DoctorsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(header_frame, text="Doctors Management", font=HEADER_FONT).pack(side="left")
        
        # Action Buttons
        btn_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        btn_frame.pack(side="right")
        
        add_btn = ctk.CTkButton(btn_frame, text="+ Add", width=100, font=BODY_FONT, cursor="hand2", command=self.open_add_doctor_dialog)
        add_btn.pack(side="left", padx=5)
        
        update_btn = ctk.CTkButton(btn_frame, text="Update", width=100, font=BODY_FONT, cursor="hand2", fg_color="#FBC02D", hover_color="#F9A825", command=self.open_update_doctor_dialog)
        update_btn.pack(side="left", padx=5)
        
        delete_btn = ctk.CTkButton(btn_frame, text="Delete", width=100, font=BODY_FONT, cursor="hand2", fg_color="#D32F2F", hover_color="#B71C1C", command=self.delete_doctor)
        delete_btn.pack(side="left", padx=5)
        
        # Search
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 10))
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search Doctor...", width=300)
        self.search_entry.pack(side="left")
        ctk.CTkButton(search_frame, text="Search", width=100, command=self.perform_search).pack(side="left", padx=10)

        # Treeview (Table)
        tree_frame = ctk.CTkFrame(self) 
        tree_frame.pack(fill="both", expand=True)

        cols = ("ID", "Name", "Age", "Gender", "Specialty", "Phone", "Email", "Dept ID")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=15)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
            
        self.tree.pack(fill="both", expand=True)


        self.load_doctors()

    def load_doctors(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = connect()
        if conn:
            try:
                cursor = conn.cursor()
                doctors = Doctor.get_all(cursor)
                
                for doc in doctors:
                    values = (doc[0], doc[1], doc[2], doc[3], doc[6], doc[4], doc[5], doc[7])
                    self.tree.insert("", "end", values=values)
            except Exception as e:
                messagebox.showerror("Error", f"Error loading doctors: {e}")
            finally:
                conn.close()

    def perform_search(self):
        query = self.search_entry.get()

        if not query.strip():
            self.load_doctors()
            return
            
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = connect()
        if conn:
            try:
                cursor = conn.cursor()
                doctors = Doctor.search(cursor, query)
                
                for doc in doctors:
                    values = (doc[0], doc[1], doc[2], doc[3], doc[6], doc[4], doc[5], doc[7])
                    self.tree.insert("", "end", values=values)
            except Exception as e:
                messagebox.showerror("Error", f"Error searching doctors: {e}")

            finally:
                conn.close()

    def open_add_doctor_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Doctor")
        dialog.geometry("400x600")
        dialog.transient(self)
        
        # Center the window
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        
        ctk.CTkLabel(dialog, text="Add New Doctor", font=("Roboto Medium", 18)).pack(pady=20)
        
        # Form
        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(form_frame, text="Name:").pack(anchor="w")
        name_entry = ctk.CTkEntry(form_frame)
        name_entry.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Age:").pack(anchor="w")
        age_entry = ctk.CTkEntry(form_frame)
        age_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Gender:").pack(anchor="w")
        gender_entry = ctk.CTkOptionMenu(form_frame, values=["Male", "Female"])
        gender_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Phone:").pack(anchor="w")
        phone_entry = ctk.CTkEntry(form_frame)
        phone_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Email:").pack(anchor="w")
        email_entry = ctk.CTkEntry(form_frame)
        email_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Specialization:").pack(anchor="w")
        spec_entry = ctk.CTkEntry(form_frame)
        spec_entry.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Department ID:").pack(anchor="w")
        dept_entry = ctk.CTkEntry(form_frame)
        dept_entry.pack(fill="x", pady=(0, 10))
        
        save_btn = ctk.CTkButton(dialog, text="Save Doctor", 
                                 command=lambda: self.save_new_doctor(dialog, 
                                                                    name_entry.get(), 
                                                                    age_entry.get(),
                                                                    gender_entry.get(), 
                                                                    phone_entry.get(), 
                                                                    email_entry.get(),
                                                                    spec_entry.get(), 
                                                                    dept_entry.get()))
        save_btn.pack(pady=20)
        
        dialog.after(100, dialog.grab_set)

    def save_new_doctor(self, dialog, name, age, gender, phone, email, spec, dept_id):
        if not name or not spec or not dept_id:
            messagebox.showwarning("Warning", "All fields are required")
            return
            
        try:
            dept_id = int(dept_id)
        except ValueError:
            messagebox.showwarning("Warning", "Department ID must be an integer")
            return

        conn = connect()
        if conn:
            try:
                cursor = conn.cursor()
                new_doc = Doctor(name, age, gender, phone, email, spec, dept_id)
                new_doc.save_to_db(cursor, conn)
                messagebox.showinfo("Success", "Doctor saved successfully!")
                dialog.destroy()
                self.load_doctors() 
            except Exception as e:
                messagebox.showerror("Error", f"Error saving doctor: {e}")
            finally:
                conn.close()

    def delete_doctor(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a doctor to delete")
            return
            
        # Get ID (first column)
        item = self.tree.item(selected_item)
        values = item['values']
        if not values: return
        doctor_id = values[0]
        
        conn = connect()
        if conn:
            try:
                cursor = conn.cursor()
                Doctor.delete_from_db(cursor, conn, doctor_id)
                messagebox.showinfo("Success", "Doctor deleted successfully")
                self.load_doctors()
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting doctor: {e}")
            finally:
                conn.close()

    def open_update_doctor_dialog(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a doctor to update")
            return
            
        item = self.tree.item(selected_item)
        values = item['values']
        if not values: return
        
        doc_id = values[0]
        current_name = values[1]
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Update Doctor")
        dialog.geometry("400x600")
        dialog.transient(self)
        
        # Doc values: ID, Name, Age, Gender, Specialty, Phone, Email, DeptID
        current_age = values[2]
        current_gender = values[3]
        current_spec = values[4]
        current_phone = values[5]
        current_email = values[6]
        current_dept_id = values[7]
        
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        
        ctk.CTkLabel(dialog, text="Update Doctor", font=("Roboto Medium", 18)).pack(pady=20)
        
        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(form_frame, text="Name:").pack(anchor="w")
        name_entry = ctk.CTkEntry(form_frame)
        name_entry.insert(0, current_name)
        name_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Age:").pack(anchor="w")
        age_entry = ctk.CTkEntry(form_frame)
        age_entry.insert(0, current_age)
        age_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Gender:").pack(anchor="w")
        gender_entry = ctk.CTkOptionMenu(form_frame, values=["Male", "Female"])
        gender_entry.set(current_gender)
        gender_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Phone:").pack(anchor="w")
        phone_entry = ctk.CTkEntry(form_frame)
        phone_entry.insert(0, current_phone)
        phone_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Email:").pack(anchor="w")
        email_entry = ctk.CTkEntry(form_frame)
        email_entry.insert(0, current_email)
        email_entry.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Specialization:").pack(anchor="w")
        spec_entry = ctk.CTkEntry(form_frame)
        spec_entry.insert(0, current_spec)
        spec_entry.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Department ID:").pack(anchor="w")
        dept_entry = ctk.CTkEntry(form_frame)
        
        dept_entry.insert(0, str(current_dept_id))
        dept_entry.pack(fill="x", pady=(0, 10))
        
        save_btn = ctk.CTkButton(dialog, text="Update Doctor", 
                                 command=lambda: self.save_updated_doctor(dialog, 
                                                                        doc_id,
                                                                        name_entry.get(),
                                                                        age_entry.get(),
                                                                        gender_entry.get(),
                                                                        phone_entry.get(),
                                                                        email_entry.get(),
                                                                        spec_entry.get(),
                                                                        dept_entry.get()))
        save_btn.pack(pady=20)
        
        dialog.after(100, dialog.grab_set)

    def save_updated_doctor(self, dialog, doc_id, name, age, gender, phone, email, spec, dept_id):
        if not name or not spec or not dept_id:
            messagebox.showwarning("Warning", "All fields are required")
            return
            
        try:
            dept_id = int(dept_id)
        except ValueError:
            messagebox.showwarning("Warning", "Department ID must be an integer")
            return

        conn = connect()
        if conn:
            try:
                cursor = conn.cursor()
                doc = Doctor(name, age, gender, phone, email, spec, dept_id)
                doc.update_doc_info(cursor, conn, doc_id)
                messagebox.showinfo("Success", "Doctor updated successfully!")
                dialog.destroy()
                self.load_doctors()
            except Exception as e:
                messagebox.showerror("Error", f"Error updating doctor: {e}")
            finally:
                conn.close()