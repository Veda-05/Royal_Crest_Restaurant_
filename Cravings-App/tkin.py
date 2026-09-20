from sqlalchemy import create_engine, text
import pandas as pd
import tkinter as tk
from tkinter import messagebox

# 1. Create engine to connect to your database
engine = create_engine("mysql+mysqlconnector://root:23022006@localhost/STUDINFO")
# --- Functions ---

def insert_student():
    try:
        name = name_entry.get()
        roll = int(roll_entry.get())
        cgpa = float(cgpa_entry.get())
        query = text("INSERT INTO stud (name, roll_no, cgpa) VALUES (:name, :roll_no, :cgpa)")
        with engine.connect() as conn:
            conn.execute(query, {"name": name, "roll_no": roll, "cgpa": cgpa})
            conn.commit()
        messagebox.showinfo("Success", "Student inserted successfully.")
        display_students()
    except Exception as e:
        messagebox.showerror("Error", str(e))


def update_student():
    try:
        roll = int(update_roll_entry.get())
        new_cgpa = float(update_cgpa_entry.get())

        query = text("UPDATE stud SET cgpa = :cgpa WHERE roll_no = :roll_no")
        with engine.connect() as conn:
            result = conn.execute(query, {"cgpa": new_cgpa, "roll_no": roll})
            conn.commit()
        if result.rowcount == 0:
            messagebox.showinfo("Info", "No record found to update.")
        else:
            messagebox.showinfo("Success", "CGPA updated successfully.")
        display_students()
    except Exception as e:
        messagebox.showerror("Error", str(e))


def delete_student():
    try:
        roll = int(delete_roll_entry.get())
        query = text("DELETE FROM stud WHERE roll_no = :roll_no")
        with engine.connect() as conn:
            result = conn.execute(query, {"roll_no": roll})
            conn.commit()
        if result.rowcount == 0:
            messagebox.showinfo("Info", "No record found to delete.")
        else:
            messagebox.showinfo("Success", "Student deleted successfully.")
        display_students()
    except Exception as e:
        messagebox.showerror("Error", str(e))


def display_students():
    try:
        df = pd.read_sql("SELECT * FROM stud", con=engine)
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, df.to_string(index=False))
    except Exception as e:
        text_output.insert(tk.END, f"Error: {str(e)}")

# --- GUI Design ---

window = tk.Tk()
window.title("Student Database Management")
window.geometry("600x600")

# Insert Section
tk.Label(window, text="Insert Student", font=("Arial", 12, "bold")).pack(pady=5)
tk.Label(window, text="Name:").pack()
name_entry = tk.Entry(window)
name_entry.pack()

tk.Label(window, text="Roll No:").pack()
roll_entry = tk.Entry(window)
roll_entry.pack()

tk.Label(window, text="CGPA:").pack()
cgpa_entry = tk.Entry(window)
cgpa_entry.pack()

tk.Button(window, text="Insert", command=insert_student).pack(pady=5)

# Update Section
tk.Label(window, text="\nUpdate CGPA", font=("Arial", 12, "bold")).pack()
tk.Label(window, text="Roll No:").pack()
update_roll_entry = tk.Entry(window)
update_roll_entry.pack()

tk.Label(window, text="New CGPA:").pack()
update_cgpa_entry = tk.Entry(window)
update_cgpa_entry.pack()

tk.Button(window, text="Update", command=update_student).pack(pady=5)

# Delete Section
tk.Label(window, text="\nDelete Student", font=("Arial", 12, "bold")).pack()
tk.Label(window, text="Roll No:").pack()
delete_roll_entry = tk.Entry(window)
delete_roll_entry.pack()

tk.Button(window, text="Delete", command=delete_student).pack(pady=5)

# Display Table
tk.Label(window, text="\nStudent Records", font=("Arial", 12, "bold")).pack()
text_output = tk.Text(window, height=15, width=70)
text_output.pack()

tk.Button(window, text="Refresh Table", command=display_students).pack(pady=5)

# Run on startup
display_students()

window.mainloop()