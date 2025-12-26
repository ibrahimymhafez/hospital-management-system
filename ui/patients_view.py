import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from styles import HEADER_FONT, BODY_FONT
from backend.models.patient import Patient

class PatientsView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.cursor = self.controller.db_conn.cursor()
        
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(header_frame, text="Patients Management", font=HEADER_FONT).pack(side="left")
        
        # Buttons
        btn_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        btn_frame.pack(side="right")

        add_btn = ctk.CTkButton(btn_frame, text="+ Add Patient", font=BODY_FONT, cursor="hand2", command=self.open_add_dialog)
        add_btn.pack(side="right", padx=5)

        update_btn = ctk.CTkButton(btn_frame, text="Update Selected", font=BODY_FONT, cursor="hand2", fg_color="orange", hover_color="#D97706", command=self.open_update_dialog)
        update_btn.pack(side="right", padx=5)
        
        delete_btn = ctk.CTkButton(btn_frame, text="Delete Selected", font=BODY_FONT, cursor="hand2", fg_color="red", hover_color="#C62828", command=self.delete_patient)
        delete_btn.pack(side="right", padx=5)

        # Search
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 10))
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search Patient...", width=300)
        self.search_entry.pack(side="left")
        ctk.CTkButton(search_frame, text="Search", width=100, command=self.search_patient).pack(side="left", padx=10)
        ctk.CTkButton(search_frame, text="Refresh", width=100, command=self.load_data).pack(side="left", padx=0)

        # Table 
        tree_frame = ctk.CTkFrame(self) 
        tree_frame.pack(fill="both", expand=True)

        cols = ("ID", "Name", "Age", "Gender", "Phone", "Email")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=15)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
            
        self.tree.pack(fill="both", expand=True)
        
        self.load_data()

    def load_data(self):
        # Clear 
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch 
        patients = Patient.fetch_all_patients(self.cursor)
        for p in patients:
            values = (p[0], p[1], p[2], p[3], p[4], p[5])
            self.tree.insert("", "end", values=values)

    def search_patient(self):
        term = self.search_entry.get()
        if not term:
            return self.load_data()
            
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        patients = Patient.search_patients(self.cursor, term)
        for p in patients:
            values = (p[0], p[1], p[2], p[3], p[4], p[5])
            self.tree.insert("", "end", values=values)

    def open_add_dialog(self):
        PatientDialog(self, "Add Patient", self.save_patient)

    def open_update_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a patient to update.")
            return

        item = self.tree.item(selected[0])
        values = item['values']
        patient_data = {
            "id": values[0],
            "name": values[1],
            "age": values[2],
            "gender": values[3],
            "phone": values[4],
            "email": values[5]
        }
        
        PatientDialog(self, "Update Patient", self.update_patient_info, patient_data)

    def save_patient(self, data):
        # Create Patient Object
        try:
            p = Patient(data['name'], int(data['age']), data['gender'], data['phone'], data['email'])
            p.save_to_db(self.cursor, self.controller.db_conn)
            self.load_data()
            messagebox.showinfo("Success", "Patient added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add patient: {e}")

    def update_patient_info(self, data):
        try:
            # Update given the current values
            p = Patient(data['name'], int(data['age']), data['gender'], data['phone'], data['email'])
            # Using the update_info from patient model
            p.update_info(self.cursor, self.controller.db_conn, data['id'])
            self.load_data()
            messagebox.showinfo("Success", "Patient updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update patient: {e}")

    def delete_patient(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a patient to delete.")
            return

        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this patient?"):
            return

        item = self.tree.item(selected[0])
        patient_id = item['values'][0]
        
        try:
            Patient.delete_from_db(self.cursor, self.controller.db_conn, patient_id)
            self.load_data()
            messagebox.showinfo("Success", "Patient deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete patient: {e}")


class PatientDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, callback, data=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x500")
        self.callback = callback
        self.data = data # if data is present, then it is an update
        
        self.entries = {}
        fields = ["Name", "Age", "Gender", "Phone", "Email"]
        
        for i, field in enumerate(fields):
            ctk.CTkLabel(self, text=field).pack(pady=(10, 0))
            
            if field == "Gender":
                entry = ctk.CTkOptionMenu(self, values=["Male", "Female"], width=250)
                if data and field.lower() in data:
                    entry.set(data[field.lower()])
            else:
                entry = ctk.CTkEntry(self, width=250)
                if data and field.lower() in data:
                    entry.insert(0, data[field.lower()])
            
            entry.pack()
            self.entries[field.lower()] = entry
                
        # Handle patient id for update
        if data:
            self.patient_id = data['id']
        else:
            self.patient_id = None

        ctk.CTkButton(self, text="Save", command=self.save).pack(pady=20)

    def save(self):
        result = {}
        for field, entry in self.entries.items():
            value = entry.get()
            if not value:
                messagebox.showwarning("Warning", f"{field.capitalize()} is required.")
                return
            result[field] = value
        
        if self.patient_id:
            result['id'] = self.patient_id
            
        self.callback(result)
        self.destroy()
