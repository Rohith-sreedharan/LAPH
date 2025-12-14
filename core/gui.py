import ttkbootstrap as tb
from ttkbootstrap.constants import PRIMARY, SUCCESS, DANGER, WARNING
import threading
from core.repair_loop import RepairLoop
import tkinter as tk
from tkinter import scrolledtext

class LAPH_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("L.A.P.H. — Local Autonomous Programming Helper")
        self.root.geometry("900x700")
        self.agent = RepairLoop()
        self.setup_widgets()

    def setup_widgets(self):
        style = tb.Style("superhero")  # Brighter, modern dark theme

        frame = tb.Frame(self.root, padding=0, bootstyle="dark")
        frame.pack(fill="both", expand=True)

        # Title area
        title_frame = tb.Frame(frame, bootstyle="dark")
        title_frame.pack(pady=(20, 5))
        tb.Label(title_frame, text="L.A.P.H.", font=("Orbitron", 40, "bold"), bootstyle=PRIMARY).pack()
        tb.Label(title_frame, text="Local Autonomous Programming Helper", font=("Segoe UI", 15, "italic"), bootstyle="info").pack()

        # Card-like input area
        input_card = tb.Frame(frame, padding=24, bootstyle="info")
        input_card.pack(pady=18, padx=40, fill="x")
        tb.Label(input_card, text="Describe your program:", font=("Segoe UI", 15, "bold"), bootstyle="inverse-info").pack(anchor="w", pady=(0, 10))
        
        # New LabeledEntry for Max Iterations
        max_iters_frame = tb.Frame(input_card, bootstyle="info")
        max_iters_frame.pack(fill="x", pady=(0, 10))
        tb.Label(max_iters_frame, text="Max Iterations:", font=("Segoe UI", 12, "bold"), bootstyle="inverse-info").pack(side="left", anchor="w")
        self.max_iters_entry = tb.Entry(max_iters_frame, width=10, font=("Fira Sans", 12))
        self.max_iters_entry.insert(0, "10")  # Default value
        self.max_iters_entry.pack(side="left", padx=5)

        self.task_entry = tb.Entry(input_card, width=70, font=("Fira Sans", 14))
        self.task_entry.pack(pady=6, padx=2, ipady=8, fill="x")

        # Button row
        button_row = tb.Frame(input_card, bootstyle="info")
        button_row.pack(pady=12, fill="x")
        self.run_button = tb.Button(button_row, text="🚀 Run Task", bootstyle="success", command=self.run_task_thread, width=18)
        self.run_button.pack(side="left", padx=(0, 12))
        tb.Button(button_row, text="🎲 Dice Roller Example", bootstyle="warning", command=self.fill_dice_prompt, width=22).pack(side="left")

        # Status label
        self.status_label = tb.Label(input_card, text="Idle", font=("Fira Sans", 12, "bold"), bootstyle="primary")
        self.status_label.pack(pady=7, anchor="w")

        # Output area
        output_card = tb.Frame(frame, padding=18, bootstyle="dark")
        output_card.pack(pady=(18, 0), padx=40, fill="both", expand=True)
        tb.Label(output_card, text="Generated Code Output", font=("Fira Sans", 13, "bold"), bootstyle="inverse-dark").pack(anchor="w", pady=(0, 8))
        self.output_box = scrolledtext.ScrolledText(output_card, width=100, height=20, font=("Fira Mono", 13), bg="#181c20", fg="#e0e0e0", insertbackground="#e0e0e0", borderwidth=2, relief="groove")
        self.output_box.pack(pady=5, fill="both", expand=True)

        # Add subtle drop shadow to main window (if supported)
        try:
            self.root.tk.call("wm", "attributes", ".", "-alpha", 0.98)
        except Exception:
            pass

    def fill_dice_prompt(self):
        example = (
            "a program that makes a simple dice roller where you can choose any dice with any amount of sides and then roll them, "
            "maybe add extra dice like two 20 sided dices or 1 four sided dice, and 2 six sided dices, all rolling together "
            "(and maybe total all the dices values and also make it so whatever the dice rolls to you can add a custom value to it)"
        )
        self.task_entry.delete(0, "end")
        self.task_entry.insert(0, example)

    def run_task_thread(self):
        threading.Thread(target=self.run_task, daemon=True).start()

    def run_task(self):
        task = self.task_entry.get()
        try:
            max_iters = int(self.max_iters_entry.get())
        except ValueError:
            max_iters = 10  # Default to 10 if input is invalid
        self.status_label.config(text="Running...", bootstyle=WARNING)
        self.output_box.delete(1.0, "end")
        final_code = self.agent.run_task(task)
        if final_code:
            self.status_label.config(text="Success!", bootstyle=SUCCESS)
            self.output_box.insert("end", final_code)
        else:
            self.status_label.config(text="Failed after max iterations.", bootstyle=DANGER)