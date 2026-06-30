from event_manager import EventManager

manager = EventManager()

while True:

    print("\n===== EVENT MANAGEMENT SYSTEM =====")
    print("1. Add Event")
    print("2. View Event")
    print("3. Edit Event")
    print("4. Search Event")
    print("5. Sort Event")
    print("6. Filter Event")
    print("7. Delete Events")
    print("8. Exit")
    
    choice = input("Enter your choice: ")

    if choice == "1":
        manager.add_event()
    
    elif choice == "2":
        manager.view_events()

    elif choice == "3":
        manager.edit_event()
    
    elif choice == "4":
        manager.search_event()
    
    elif choice == "5":
        manager.sort_events()

    elif choice == "6":
        manager.filter_events()

    elif choice == "7":
        manager.delete_event()

    elif choice == "8":
        print("Exiting...")
        break

    else:
        print("Invalid choice.")
        