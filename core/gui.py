import ttkbootstrap as tb
from ttkbootstrap.constants import PRIMARY, SUCCESS, DANGER, WARNING, INFO
import threading
from core.repair_loop import RepairLoop
import tkinter as tk
from tkinter import scrolledtext
from core.logger import Logger

class LAPH_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("L.A.P.H. — Local Autonomous Programming Helper")
        self.root.geometry("1400x900")
        self.logger = Logger()
        self.logger.register_callback(self.log_message)
        self.agent = RepairLoop(self.logger)
        self.setup_widgets()

    def setup_widgets(self):
        style = tb.Style("superhero")

        main_frame = tb.Frame(self.root, padding=20, bootstyle="dark")
        main_frame.pack(fill="both", expand=True)

        # Title
        title_frame = tb.Frame(main_frame, bootstyle="dark")
        title_frame.pack(pady=(0, 20))
        tb.Label(title_frame, text="L.A.P.H.", font=("Orbitron", 48, "bold"), bootstyle=PRIMARY).pack()
        tb.Label(title_frame, text="Local Autonomous Programming Helper", font=("Segoe UI", 16, "italic"), bootstyle="info").pack()

        # Input Frame
        input_frame = tb.Labelframe(main_frame, text="Your Task", padding=20, bootstyle=PRIMARY)
        input_frame.pack(fill="x", pady=(0, 20))

        self.task_entry = tb.Entry(input_frame, width=70, font=("Fira Sans", 14))
        self.task_entry.pack(pady=10, padx=5, ipady=10, fill="x", expand=True)
        
        # Options Frame
        options_frame = tb.Frame(input_frame, bootstyle="dark")
        options_frame.pack(fill="x", expand=True)

        tb.Label(options_frame, text="Max Iterations:", font=("Segoe UI", 12), bootstyle="inverse-dark").pack(side="left", padx=(5,5))
        self.max_iters_entry = tb.Entry(options_frame, width=10, font=("Fira Sans", 12))
        self.max_iters_entry.insert(0, "10")
        self.max_iters_entry.pack(side="left", padx=(0, 10))

        unlimited_button = tb.Button(options_frame, text="♾️ Unlimited", bootstyle="info", command=lambda: self.max_iters_entry.delete(0, "end") or self.max_iters_entry.insert(0, "60"))
        unlimited_button.pack(side="left", padx=(0, 20))

        self.run_button = tb.Button(options_frame, text="🚀 Run Task", bootstyle=SUCCESS, command=self.run_task_thread)
        self.run_button.pack(side="right", padx=5)
        
        self.example_button = tb.Button(options_frame, text="🎲 Dice Roller Example", bootstyle=WARNING, command=self.fill_dice_prompt)
        self.example_button.pack(side="right", padx=5)


        # Paned Window for Output and Logs
        paned_window = tb.Panedwindow(main_frame, orient="horizontal", bootstyle="dark")
        paned_window.pack(fill="both", expand=True, pady=(10, 0))

        # Left Paned Window for Thinker and Coder
        left_paned_window = tb.Panedwindow(paned_window, orient="vertical", bootstyle="dark")
        paned_window.add(left_paned_window, weight=1)
        
        # Thinker area
        thinker_frame = tb.Labelframe(left_paned_window, text="Thinker Output", padding=10, bootstyle=INFO)
        left_paned_window.add(thinker_frame, weight=1)

        self.thinker_box = scrolledtext.ScrolledText(thinker_frame, width=100, height=10, font=("Fira Mono", 11), bg="#1e1e1e", fg="#a9a9a9", insertbackground="white", borderwidth=0, relief="flat")
        self.thinker_box.pack(pady=5, fill="both", expand=True)

        # Coder area
        coder_frame = tb.Labelframe(left_paned_window, text="Generated Code", padding=10, bootstyle=SUCCESS)
        left_paned_window.add(coder_frame, weight=2)
        
        self.output_box = scrolledtext.ScrolledText(coder_frame, width=100, height=15, font=("Fira Mono", 12), bg="#1e1e1e", fg="#d4d4d4", insertbackground="white", borderwidth=0, relief="flat")
        self.output_box.pack(pady=5, fill="both", expand=True)
        
        copy_button = tb.Button(coder_frame, text="Copy Code", command=self.copy_code, bootstyle="info-outline")
        copy_button.pack(pady=5)


        # Log area
        log_frame = tb.Labelframe(paned_window, text="LLM Status & Execution", padding=10, bootstyle=INFO)
        paned_window.add(log_frame, weight=1)

        self.log_box = scrolledtext.ScrolledText(log_frame, width=100, height=10, font=("Fira Mono", 11), bg="#1e1e1e", fg="#a9a9a9", insertbackground="white", borderwidth=0, relief="flat")
        self.log_box.pack(pady=5, fill="both", expand=True)
        
        self.status_label = tb.Label(main_frame, text="Idle", font=("Fira Sans", 12, "bold"), bootstyle=PRIMARY)
        self.status_label.pack(pady=10, anchor="w")

    def copy_code(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output_box.get(1.0, tk.END))

    def log_message(self, message):
        self.log_box.insert(tk.END, message)
        self.log_box.see(tk.END)

    def stream_callback(self, chunk, source):
        if source == "coder":
            self.output_box.insert(tk.END, chunk)
            self.output_box.see(tk.END)
        elif source == "thinker":
            self.thinker_box.insert(tk.END, chunk)
            self.thinker_box.see(tk.END)
        
        self.log_box.insert(tk.END, chunk)
        self.log_box.see(tk.END)

    def fill_dice_prompt(self):
        example = (
            "a program that makes a simple dice roller where you can choose any dice with any amount of sides and then roll them, "
            "maybe add extra dice like two 20 sided dices or 1 four sided dice, and 2 six sided dices, all rolling together "
            "(and maybe total all the dices values and also make it so whatever the dice rolls to you can add a custom value to it)"
        )
        self.task_entry.delete(0, "end")
        self.task_entry.insert(0, example)

    def run_task_thread(self):
        self.run_button.config(state="disabled")
        self.example_button.config(state="disabled")
        self.log_box.delete(1.0, tk.END)
        self.output_box.delete(1.0, tk.END)
        self.thinker_box.delete(1.0, tk.END)
        threading.Thread(target=self.run_task, daemon=True).start()

    def run_task(self):
        task = self.task_entry.get()
        
        # Validate task input
        if not task or not task.strip():
            self.logger.log("ERROR: Task description cannot be empty.")
            self.status_label.config(text="Error: Empty task", bootstyle=DANGER)
            self.run_button.config(state="normal")
            self.example_button.config(state="normal")
            return
        
        # Validate max iterations
        try:
            max_iters = int(self.max_iters_entry.get())
            if max_iters < 1:
                raise ValueError("Must be positive")
            if max_iters > 100:
                self.logger.log("WARNING: Max iterations is very high (>100), capping at 100.")
                max_iters = 100
        except ValueError:
            max_iters = 10
            self.logger.log("Invalid max iterations value, defaulting to 10.")
        
        self.status_label.config(text="Running...", bootstyle=WARNING)
        self.logger.log(f"Starting task with max {max_iters} iterations.")

        final_code = self.agent.run_task(task, max_iters=max_iters, stream_callback=self.stream_callback)

        if final_code:
            self.status_label.config(text="Success! ✨", bootstyle=SUCCESS)
            self.logger.log("Task finished successfully.")
        else:
            self.status_label.config(text="Failed to generate a working script. Try a different prompt or more iterations.", bootstyle=DANGER)
            self.logger.log("Task failed. Maximum iterations reached.")
        
        self.run_button.config(state="normal")
        self.example_button.config(state="normal")