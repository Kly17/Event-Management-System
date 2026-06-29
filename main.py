from event_manager import EventManager

manager = EventManager()

while True:

    print("\n===== EVENT MANAGEMENT SYSTEM =====")
    print("1. Add Event")
    print("2. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        manager.add_event()

    elif choice == "2":
        print("Exiting...")
        break

    else:
        print("Invalid choice.")