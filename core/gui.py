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
        style = tb.Style("cyborg")  # More modern dark theme
        frame = tb.Frame(self.root, padding=30, bootstyle="secondary")
        frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Title with shadow effect
        title_frame = tb.Frame(frame, bootstyle="secondary")
        title_frame.pack(pady=(0, 10))
        tb.Label(title_frame, text="L.A.P.H.", font=("Orbitron", 38, "bold"), bootstyle=PRIMARY).pack()
        tb.Label(title_frame, text="Local Autonomous Programming Helper", font=("Segoe UI", 14, "italic"), bootstyle="info").pack()

        # Card-like input area
        input_card = tb.Frame(frame, padding=20, bootstyle="info rounded-pill")
        input_card.pack(pady=10, fill="x")
        tb.Label(input_card, text="Describe the program you want L.A.P.H. to build:", font=("Segoe UI", 14, "bold"), bootstyle="inverse-info").pack(anchor="w", pady=(0, 8))
        self.task_entry = tb.Entry(input_card, width=70, font=("Segoe UI", 13), bootstyle="rounded-pill")
        self.task_entry.pack(pady=5, padx=5, ipady=6, fill="x")

        # Button row
        button_row = tb.Frame(input_card, bootstyle="info")
        button_row.pack(pady=10, fill="x")
        self.run_button = tb.Button(button_row, text="🚀 Run Task", bootstyle="success-outline rounded-pill", command=self.run_task_thread, width=18)
        self.run_button.pack(side="left", padx=(0, 10))
        tb.Button(button_row, text="🎲 Dice Roller Example", bootstyle="warning-outline rounded-pill", command=self.fill_dice_prompt, width=22).pack(side="left")

        # Status label
        self.status_label = tb.Label(input_card, text="Idle", font=("Segoe UI", 12, "bold"), bootstyle="primary rounded-pill")
        self.status_label.pack(pady=5, anchor="w")

        # Output area in a card
        output_card = tb.Frame(frame, padding=18, bootstyle="dark rounded-pill")
        output_card.pack(pady=18, fill="both", expand=True)
        tb.Label(output_card, text="Generated Code Output", font=("Segoe UI", 13, "bold"), bootstyle="inverse-dark").pack(anchor="w", pady=(0, 8))
        self.output_box = scrolledtext.ScrolledText(output_card, width=100, height=22, font=("Fira Mono", 12), bg="#181c20", fg="#e0e0e0", insertbackground="#e0e0e0", borderwidth=0, relief="flat")
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
        self.status_label.config(text="Running...", bootstyle=WARNING)
        self.output_box.delete(1.0, "end")
        final_code = self.agent.run_task(task)
        if final_code:
            self.status_label.config(text="Success!", bootstyle=SUCCESS)
            self.output_box.insert("end", final_code)
        else:
            self.status_label.config(text="Failed after max iterations.", bootstyle=DANGER)