import customtkinter as ctk
from tkinter import messagebox
from backend.models.appointment import Appointment
from backend.models.doctor import Doctor
from backend.models.patient import Patient
from backend.database.connectDB import connect
from datetime import datetime
from styles import HEADER_FONT, BODY_FONT

class AppointmentsView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Header
        ctk.CTkLabel(self, text="Appointments Management", font=HEADER_FONT).pack(pady=20)

        # Main Content - Split into Add and Delete sections
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # --- Add Appointment Section ---
        add_frame = ctk.CTkFrame(self)
        add_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(add_frame, text="Add Appointment", font=("Roboto Medium", 16)).pack(pady=10)

        # Patient Name
        ctk.CTkLabel(add_frame, text="Patient Name:").pack(anchor="w", padx=20)
        self.add_patient_entry = ctk.CTkEntry(add_frame)
        self.add_patient_entry.pack(fill="x", padx=20, pady=(0, 10))

        # Department Dropdown
        ctk.CTkLabel(add_frame, text="Department:").pack(anchor="w", padx=20)
        self.dept_var = ctk.StringVar(value="Select Department")
        self.dept_menu = ctk.CTkOptionMenu(add_frame, variable=self.dept_var, command=self.on_department_change)
        self.dept_menu.pack(fill="x", padx=20, pady=(0, 10))

        # Doctor Dropdown
        ctk.CTkLabel(add_frame, text="Doctor:").pack(anchor="w", padx=20)
        self.doctor_var = ctk.StringVar(value="Select Doctor")
        self.doctor_menu = ctk.CTkOptionMenu(add_frame, variable=self.doctor_var, state="disabled", command=self.on_doctor_change)
        self.doctor_menu.pack(fill="x", padx=20, pady=(0, 10))

        # Day Display
        ctk.CTkLabel(add_frame, text="Day:").pack(anchor="w", padx=20)
        self.day_label = ctk.CTkLabel(add_frame, text="-", font=("Roboto", 14, "bold"))
        self.day_label.pack(anchor="w", padx=20, pady=(0, 10))

        # Case Dropdown
        ctk.CTkLabel(add_frame, text="Case Type:").pack(anchor="w", padx=20)
        self.case_var = ctk.StringVar(value="First Visit")
        self.case_menu = ctk.CTkOptionMenu(add_frame, variable=self.case_var, values=["First Visit", "Follow-up", "Emergency"])
        self.case_menu.pack(fill="x", padx=20, pady=(0, 10))

        # Payment Dropdown
        ctk.CTkLabel(add_frame, text="Payment:").pack(anchor="w", padx=20)
        self.payment_var = ctk.StringVar(value="Cash")
        self.payment_menu = ctk.CTkOptionMenu(add_frame, variable=self.payment_var, values=["Visa", "Cash"])
        self.payment_menu.pack(fill="x", padx=20, pady=(0, 10))

        # Add Button
        ctk.CTkButton(add_frame, text="Add Appointment", command=self.add_appointment).pack(pady=20)


        # --- Delete Appointment Section ---
        delete_frame = ctk.CTkFrame(self)
        delete_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(delete_frame, text="Delete Appointment", font=("Roboto Medium", 16)).pack(pady=10)

        # Patient Name (Delete)
        ctk.CTkLabel(delete_frame, text="Patient Name:").pack(anchor="w", padx=20)
        self.del_patient_entry = ctk.CTkEntry(delete_frame)
        self.del_patient_entry.pack(fill="x", padx=20, pady=(0, 10))

        # Doctor Dropdown (Delete)
        ctk.CTkLabel(delete_frame, text="Doctor:").pack(anchor="w", padx=20)
        self.del_doctor_var = ctk.StringVar(value="Select Doctor")
        self.del_doctor_menu = ctk.CTkOptionMenu(delete_frame, variable=self.del_doctor_var)
        self.del_doctor_menu.pack(fill="x", padx=20, pady=(0, 10))

        # Delete Button
        ctk.CTkButton(delete_frame, text="Delete Appointment", fg_color="#D32F2F", hover_color="#B71C1C", command=self.delete_appointment).pack(pady=20)


        # Load initial data
        self.load_departments()
        self.load_all_doctors_for_delete()


    def load_departments(self):
        conn = connect()
        if conn:
            try:
                cursor = conn.cursor()
                depts = Doctor.get_all_departments(cursor)
                self.dept_map = {name: id for id, name in depts}
                self.dept_menu.configure(values=list(self.dept_map.keys()))
            except Exception as e:
                messagebox.showerror("Error", f"Error loading departments: {e}")
            finally:
                conn.close()

    def load_all_doctors_for_delete(self):
        conn = connect()
        if conn:
            try:
                cursor = conn.cursor()
                # Assuming get_all returns (id, name, ...)
                doctors = Doctor.get_all(cursor) 
                self.del_doctor_names = [doc[1] for doc in doctors] # doc[1] is name
                self.del_doctor_menu.configure(values=self.del_doctor_names)
            except Exception as e:
                print(f"Error loading doctors for delete: {e}")
            finally:
                conn.close()

    def on_department_change(self, choice):
        if choice == "Select Department":
            return
        
        self.doctor_menu.set("Select Doctor")
        self.doctor_menu.configure(state="normal", values=[])
        self.day_label.configure(text="-")
        
        conn = connect()
        if conn:
            try:
                cursor = conn.cursor()
                doctors = Doctor.get_doctors_by_dept_name(cursor, choice)
                # doctors is list of (id, name, specialization)
                self.curr_dept_doctors = {doc[1]: doc[0] for doc in doctors} # name -> id
                self.doctor_menu.configure(values=list(self.curr_dept_doctors.keys()))
            except Exception as e:
                messagebox.showerror("Error", f"Error loading doctors: {e}")
            finally:
                conn.close()

    def on_doctor_change(self, choice):
        # Update day to current day
        current_day = datetime.now().strftime("%A") # e.g., Monday
        self.day_label.configure(text=current_day)

    def add_appointment(self):
        patient_name = self.add_patient_entry.get().strip()
        doctor_name = self.doctor_var.get()
        dept_name = self.dept_var.get()
        
        if not patient_name or doctor_name == "Select Doctor" or dept_name == "Select Department":
            messagebox.showwarning("Warning", "Please fill in all fields")
            return

        conn = connect()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Check patient exists
                # Using Patient.search_patients which returns list of matches
                patients = Patient.search_patients(cursor, patient_name)
                # Filter for exact name match to be safe, or take first if name is unique enough
                # The requirement says: "if the name isn't found, display the error message"
                
                found_patient_id = None
                for p in patients:
                    # p structure depends on table Columns. Assuming p[1] is name based on save_to_db order or schema.
                    # Patient.search_patients SELECT * from patients.
                    # Let's assume name is column 1 (0 is id).
                    if p[1].lower() == patient_name.lower():
                        found_patient_id = p[0]
                        break
                
                if not found_patient_id:
                    messagebox.showerror("Error", f"Patient '{patient_name}' not found.")
                    print(f"Error: Patient '{patient_name}' not found.")
                    return

                doctor_id = self.curr_dept_doctors.get(doctor_name)
                if not doctor_id:
                    messagebox.showerror("Error", "Selected doctor invalid.")
                    return

                day = self.day_label.cget("text")
                status = self.case_var.get()
                payment = self.payment_var.get()

                # Create Appointment
                appt = Appointment(found_patient_id, doctor_id, day, status, payment)
                appt.save_to_db(cursor, conn)
                
                messagebox.showinfo("Success", "Appointment added successfully!")
                
                # Reset fields
                self.add_patient_entry.delete(0, 'end')
                # Optional: Reset dropdowns
                
            except Exception as e:
                messagebox.showerror("Error", f"Error adding appointment: {e}")
                print(f"Error adding appointment: {e}")
            finally:
                conn.close()

    def delete_appointment(self):
        patient_name = self.del_patient_entry.get().strip()
        doctor_name = self.del_doctor_var.get()

        if not patient_name or doctor_name == "Select Doctor":
            messagebox.showwarning("Warning", "Please enter patient name and select a doctor.")
            return

        conn = connect()
        if conn:
            try:
                cursor = conn.cursor()

                
                Appointment.delete_appointment_by_names(cursor, conn, patient_name, doctor_name)

                
                messagebox.showinfo("Info", "Deletion process completed. Check console for details.")

            except Exception as e:
                messagebox.showerror("Error", f"Error deleting appointment: {e}")
            finally:
                conn.close()
