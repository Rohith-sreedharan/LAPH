import tkinter as tk
from tkinter import scrolledtext
import threading
from core.repair_loop import RepairLoop

class LAPH_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("L.A.P.H. — Local Autonomous Programming Helper")
        self.agent = RepairLoop()
        self.setup_widgets()

    def setup_widgets(self):
        tk.Label(self.root, text="Describe the program you want L.A.P.H. to build:").pack(pady=5)
        self.task_entry = tk.Entry(self.root, width=80)
        self.task_entry.pack(pady=5)
        self.run_button = tk.Button(self.root, text="Run", command=self.run_task_thread)
        self.run_button.pack(pady=5)
        self.status_label = tk.Label(self.root, text="Idle", fg="blue")
        self.status_label.pack(pady=5)
        self.output_box = scrolledtext.ScrolledText(self.root, width=100, height=30)
        self.output_box.pack(pady=5)

    def run_task_thread(self):
        threading.Thread(target=self.run_task, daemon=True).start()

    def run_task(self):
        task = self.task_entry.get()
        self.status_label.config(text="Running...", fg="orange")
        self.output_box.delete(1.0, tk.END)
        final_code = self.agent.run_task(task)
        if final_code:
            self.status_label.config(text="Success!", fg="green")
            self.output_box.insert(tk.END, final_code)
        else:
            self.status_label.config(text="Failed after max iterations.", fg="red")