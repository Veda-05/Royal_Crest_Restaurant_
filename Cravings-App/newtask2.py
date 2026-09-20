import tkinter as tk
from tkinter import messagebox
from openpyxl import Workbook, load_workbook
import os

EXCEL_FILE = "tasks.xlsx"

class ExcelTaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Excel Task Manager")
        self.root.configure(bg="#e6f2ff")

        self.tasks = []  # List of dicts: {"task": str, "done": bool}

        # UI Setup
        self.setup_ui()

        # Load tasks from Excel file
        self.load_tasks_from_excel()

    def setup_ui(self):
        # Title label
        tk.Label(self.root, text="Excel-Connected Task Manager", font=("Arial", 22, "bold"),
                 bg="#e6f2ff", fg="#003366").pack(pady=20)

        # Entry box for new task
        self.entry = tk.Entry(self.root, width=40, font=("Arial", 14))
        self.entry.pack(pady=10)

        # Buttons frame
        btn_frame = tk.Frame(self.root, bg="#e6f2ff")
        btn_frame.pack(pady=10)

        btn_config = {"font": ("Arial", 12), "width": 15, "padx": 5, "pady": 5}

        tk.Button(btn_frame, text="➕ Add Task", bg="#99ccff", command=self.add_task, **btn_config).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="✅ Mark Done", bg="#99ffcc", command=self.mark_done, **btn_config).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="❌ Delete Task", bg="#ff9999", command=self.delete_task, **btn_config).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="📤 Export to Excel", bg="#ffd966", command=self.save_tasks_to_excel, **btn_config).grid(row=0, column=3, padx=5)

        # Listbox to display tasks
        self.listbox = tk.Listbox(self.root, font=("Arial", 14), width=50, height=15,
                                  selectbackground="#cce5ff", bg="white", bd=2, relief="sunken")
        self.listbox.pack(pady=20)

    def add_task(self):
        task_text = self.entry.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Please enter a task!")
            return

        self.tasks.append({"task": task_text, "done": False})
        self.entry.delete(0, tk.END)
        self.refresh_listbox()
        self.save_tasks_to_excel()

    def delete_task(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showinfo("Info", "No task selected to delete.")
            return

        idx = selected[0]
        del self.tasks[idx]
        self.refresh_listbox()
        self.save_tasks_to_excel()

    def mark_done(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showinfo("Info", "Select a task to mark as done.")
            return

        idx = selected[0]
        self.tasks[idx]["done"] = True
        self.refresh_listbox()
        self.save_tasks_to_excel()

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "[✓]" if task["done"] else "[ ]"
            self.listbox.insert(tk.END, f"{status} {task['task']}")

    def load_tasks_from_excel(self):
        if not os.path.exists(EXCEL_FILE):
            # Create file if doesn't exist
            wb = Workbook()
            ws = wb.active
            ws.title = "Tasks"
            ws.append(["Task", "Status"])
            wb.save(EXCEL_FILE)
            return

        wb = load_workbook(EXCEL_FILE)
        ws = wb.active

        self.tasks.clear()
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0] is None:
                continue
            task_text = row[0]
            status = row[1]
            done = (status.lower() == "done")
            self.tasks.append({"task": task_text, "done": done})

        self.refresh_listbox()

    def save_tasks_to_excel(self):
        wb = Workbook()
        ws = wb.active
        ws.title = "Tasks"

        # Header
        ws.append(["Task", "Status"])

        for task in self.tasks:
            status = "Done" if task["done"] else "Not Done"
            ws.append([task["task"], status])

        wb.save(EXCEL_FILE)
        # Optional: notify user that file saved
        # messagebox.showinfo("Saved", "Tasks saved to Excel successfully.")

if __name__ == "__main__":
    root = tk.Tk()

    # Maximize the window by default (Windows)
    root.state('zoomed')

    # For Linux/macOS, try: root.attributes('-zoomed', True)

    app = ExcelTaskManager(root)
    root.mainloop()
