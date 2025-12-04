import sys

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        from core.gui import LAPH_GUI
        import tkinter as tk
        root = tk.Tk()
        app = LAPH_GUI(root)
        root.mainloop()
    elif len(sys.argv) > 1 and sys.argv[1] == "--clear-logs":
        from core.logger import Logger
        Logger().clear()
        print("L.A.P.H. logs cleared.")
    else:
        from core.repair_loop import RepairLoop
        print("=== L.A.P.H. — Local Autonomous Programming Helper ===")
        task = input("\nDescribe the program you want L.A.P.H. to build:\n> ")
        agent = RepairLoop()
        final_code = agent.run_task(task)
        if final_code:
            print("\n=== FINAL CODE GENERATED ===\n")
            print(final_code)

if __name__ == "__main__":
    main()
