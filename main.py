from event_manager import EventManager

manager = EventManager()

while True:

    print("\n===== EVENT MANAGEMENT SYSTEM =====")
    print("1. Dashboard")
    print("2. Add Event")
    print("3. View Event")
    print("4. Edit Event")
    print("5. Search Event")
    print("6. Sort Event")
    print("7. Filter Event")
    print("8. Delete Event")
    print("9. Exit")
    
    choice = input("Enter your choice: ")

    if choice == "1":
        manager.dashboard()

    elif choice == "2":
        manager.add_event()
    
    elif choice == "3":
        manager.view_events()

    elif choice == "4":
        manager.edit_event()
    
    elif choice == "5":
        manager.search_event()
    
    elif choice == "6":
        manager.sort_events()

    elif choice == "7":
        manager.filter_events()

    elif choice == "8":
        manager.delete_event()

    elif choice == "9":
        print("Exiting...")
        break

    else:
        print("Invalid choice.")
        