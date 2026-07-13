from event_manager import EventManager

manager = EventManager()

while True:

    print("\n========== EVENT MANAGEMENT SYSTEM ==========")
    print("1. Event Management")
    print("2. Participant Management")
    print("3. Dashboard")
    print("4. Attendance Report")
    print("5. Export Reports")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        manager.event_menu()
    elif choice == "2":
        manager.participant_menu()
    elif choice == "3":
        manager.dashboard()
    elif choice == "4":
        manager.attendance_report()
    elif choice == "5":
        manager.export_menu()
    elif choice == "6":
        print("Exiting...")
        break
    else:
        print("Invalid choice.")