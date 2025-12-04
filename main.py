from core.repair_loop import RepairLoop

def main():
    print("=== L.A.P.H. — Local Autonomous Programming Helper ===")

    task = input("\nDescribe the program you want L.A.P.H. to build:\n> ")

    agent = RepairLoop()
    final_code = agent.run_task(task)

    if final_code:
        print("\n=== FINAL CODE GENERATED ===\n")
        print(final_code)

if __name__ == "__main__":
    main()
