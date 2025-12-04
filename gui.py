import tkinter as tk
from tkinter import scrolledtext
import threading
from core.repair_loop import RepairLoop

if __name__ == "__main__":
    from core.gui import LAPH_GUI
    root = tk.Tk()
    app = LAPH_GUI(root)
    root.mainloop()
