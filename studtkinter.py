import pandas as pd
import os
import tkinter as tk
from tkinter import messagebox, Toplevel

# Excel file and sheet setup
file_name = 'Book1.xlsx'
sheet_name = 'Sheet1'
columns = ["NAME", "ROLL.NO", "SUB 1", "SUB 2", "SUB 3", "SUB 4", "SUB 5", "TOTAL", "GPA"]

# Create Excel file if it doesn't exist
if not os.path.exists(file_name):
    df = pd.DataFrame(columns=columns)
    df.to_excel(file_name, index=False, sheet_name=sheet_name)

# Load and Save functions
def load_data():
    df = pd.read_excel(file_name, sheet_name=sheet_name)
    df.columns = df.columns.str.strip().str.upper()  # Normalize column names
    print("Loaded Columns:", df.columns.tolist())  # Debug line to confirm column names
    return df

def save_data(df):
    df.to_excel(file_name, index=False, sheet_name=sheet_name)

# Insert Window
def open_insert_window():
    win = Toplevel(root)
    win.title("Insert Student Record")
    win.attributes("-fullscreen", True)

    frame = tk.Frame(win)
    frame.pack(expand=True)

    tk.Label(frame, text="Insert New Student", font=('Helvetica', 18)).pack(pady=10)

    entry_name = tk.Entry(frame)
    entry_roll = tk.Entry(frame)
    entries_sub = [tk.Entry(frame) for _ in range(5)]

    tk.Label(frame, text="NAME").pack()
    entry_name.pack()

    tk.Label(frame, text="ROLL.NO").pack()
    entry_roll.pack()

    for i in range(5):
        tk.Label(frame, text=f"SUB {i+1}").pack()
        entries_sub[i].pack()

    def insert_row():
        try:
            name = entry_name.get().strip()
            roll = entry_roll.get().strip()

            if not name or not roll:
                messagebox.showerror("Error", "Name and Roll No are required.")
                return

            subs = []
            for i in range(5):
                val = entries_sub[i].get().strip()
                if not val.isdigit():
                    messagebox.showerror("Error", f"Invalid marks in SUB {i+1}")
                    return
                subs.append(int(val))

            total = sum(subs)
            cgpa = round(total / 50, 2)

            df = load_data()
            if roll in df["ROLL.NO"].astype(str).values:
                messagebox.showerror("Error", "ROLL.NO already exists.")
                return

            new_row = {
                "NAME": name,
                "ROLL.NO": roll,
                "SUB 1": subs[0],
                "SUB 2": subs[1],
                "SUB 3": subs[2],
                "SUB 4": subs[3],
                "SUB 5": subs[4],
                "TOTAL": total,
                "CGPA": cgpa
            }

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            messagebox.showinfo("Success", "Student added successfully.")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(frame, text="Insert", command=insert_row, bg='lightgreen', width=20).pack(pady=10)

# Update Window
def open_update_window():
    win = Toplevel(root)
    win.title("Update Student Record")
    win.attributes("-fullscreen", True)

    frame = tk.Frame(win)
    frame.pack(expand=True)

    tk.Label(frame, text="Update Student Record", font=('Helvetica', 18)).pack(pady=10)

    entry_name = tk.Entry(frame)
    entry_roll = tk.Entry(frame)
    entries_sub = [tk.Entry(frame) for _ in range(5)]

    tk.Label(frame, text="ROLL.NO (to find record)").pack()
    entry_roll.pack()

    tk.Label(frame, text="NAME (leave blank to keep same)").pack()
    entry_name.pack()

    for i in range(5):
        tk.Label(frame, text=f"SUB {i+1} (leave blank to keep same)").pack()
        entries_sub[i].pack()

    def update_row():
        try:
            roll = entry_roll.get().strip()
            df = load_data()
            idx = df[df["ROLL.NO"].astype(str) == roll].index

            if idx.empty:
                messagebox.showerror("Error", "ROLL.NO not found.")
                return

            name = entry_name.get().strip() or df.loc[idx[0], "NAME"]
            subs = []
            for i in range(5):
                val = entries_sub[i].get().strip()
                if val:
                    if not val.isdigit():
                        messagebox.showerror("Error", f"Invalid marks in SUB {i+1}")
                        return
                    subs.append(int(val))
                else:
                    subs.append(df.loc[idx[0], f"SUB {i+1}"])

            total = sum(subs)
            cgpa = round(total / 50, 2)

            df.loc[idx[0]] = [name, roll, *subs, total, cgpa]
            save_data(df)
            messagebox.showinfo("Success", "Student updated successfully.")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(frame, text="Update", command=update_row, bg='lightblue', width=20).pack(pady=10)

# Delete Window
def open_delete_window():
    win = Toplevel(root)
    win.title("Delete Student Record")
    win.attributes("-fullscreen", True)

    frame = tk.Frame(win)
    frame.pack(expand=True)

    tk.Label(frame, text="Delete Student by ROLL.NO", font=('Helvetica', 18)).pack(pady=10)

    entry_roll = tk.Entry(frame)
    tk.Label(frame, text="ROLL.NO").pack()
    entry_roll.pack()

    def delete_row():
        try:
            roll = entry_roll.get().strip()
            df = load_data()
            idx = df[df["ROLL.NO"].astype(str) == roll].index

            if idx.empty:
                messagebox.showerror("Error", "ROLL.NO not found.")
                return

            df = df.drop(idx)
            save_data(df)
            messagebox.showinfo("Success", "Student deleted successfully.")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(frame, text="Delete", command=delete_row, bg='salmon', width=20).pack(pady=10)

# Main GUI
root = tk.Tk()
root.title("Student Record System - Book1 Sheet1")
root.attributes("-fullscreen", True)

main_frame = tk.Frame(root)
main_frame.pack(expand=True)

tk.Label(main_frame, text="Student Record System", font=("Helvetica", 24)).pack(pady=20)

tk.Button(main_frame, text="Insert Record", command=open_insert_window, width=25, height=2, bg='lightgreen').pack(pady=10)
tk.Button(main_frame, text="Update Record", command=open_update_window, width=25, height=2, bg='lightblue').pack(pady=10)
tk.Button(main_frame, text="Delete Record", command=open_delete_window, width=25, height=2, bg='salmon').pack(pady=10)
tk.Button(main_frame, text="Exit", command=root.destroy, width=25, height=2).pack(pady=40)

root.mainloop()