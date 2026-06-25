# Simple Event Management System

events = []

while True:
    print("\n===== EVENT MANAGEMENT SYSTEM =====")
    print("1. Add Event")
    print("2. View Events")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        event_name = input("Enter event name: ")
        event_date = input("Enter event date (YYYY-MM-DD): ")
        event_location = input("Enter event location: ")

        event = {
            "name": event_name,
            "date": event_date,
            "location": event_location
        }

        events.append(event)
        print("Event added successfully!")

    elif choice == "2":
        if len(events) == 0:
            print("No events found.")
        else:
            print("\n--- Event List ---")
            for i, event in enumerate(events, start=1):
                print(f"\nEvent #{i}")
                print(f"Name: {event['name']}")
                print(f"Date: {event['date']}")
                print(f"Location: {event['location']}")

    elif choice == "3":
        print("Exiting system...")
        break

    else:
        print("Invalid choice. Please try again.")