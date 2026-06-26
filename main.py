# Event Management System

import json

def load_events():
    try:
        with open("events.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def save_events(events):
    with open("events.json", "w") as file:
        json.dump(events, file, indent=4)

events = load_events()

while True:
    print("\n===== EVENT MANAGEMENT SYSTEM =====")
    print("1. Add Event")
    print("2. View Events")
    print("3. Edit Event")
    print("4. Delete Event")
    print("5. Exit")

    choice = input("Enter your choice: ")

    # ADD EVENT
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
        save_events(events)
        print("Event added successfully!")

    # VIEW EVENTS
    elif choice == "2":
        if len(events) == 0:
            print("No events found.")
        else:
            print("\n--- Event List ---")
            for i, event in enumerate(events, start=1):
                print(
                    f"{i}. {event['name']} | {event['date']} | {event['location']}")

    # EDIT EVENT
    elif choice == "3":
        if len(events) == 0:
            print("No events available to edit.")
        else:
            print("\n--- Event List ---")
            for i, event in enumerate(events, start=1):
                print(
                    f"{i}. {event['name']} | {event['date']} | {event['location']}")

            try:
                event_num = int(
                    input("Enter the event number to edit: "))

                if 1 <= event_num <= len(events):
                    event = events[event_num - 1]

                    print("\nLeave blank to keep current value.")

                    new_name = input(
                        f"New name ({event['name']}): ")
                    new_date = input(
                        f"New date ({event['date']}): ")
                    new_location = input(
                        f"New location ({event['location']}): ")

                    if new_name:
                        event['name'] = new_name
                        save_events(events)
                    if new_date:
                        event['date'] = new_date
                        save_events(events)
                    if new_location:
                        event['location'] = new_location
                        save_events(events)

                    print("Event updated successfully!")

                else:
                    print("Invalid event number.")

            except ValueError:
                print("Please enter a valid number.")

    # DELETE EVENT
    elif choice == "4":
        if len(events) == 0:
            print("No events available to delete.")
        else:
            print("\n--- Event List ---")
            for i, event in enumerate(events, start=1):
                print(
                    f"{i}. {event['name']} | {event['date']} | {event['location']}")

            try:
                event_num = int(
                    input("Enter the event number to delete: "))

                if 1 <= event_num <= len(events):
                    deleted_event = events.pop(event_num - 1)
                    save_events(events)
                    print(
                        f"'{deleted_event['name']}' deleted successfully!")
                else:
                    print("Invalid event number.")

            except ValueError:
                print("Please enter a valid number.")

    # EXIT
    elif choice == "5":
        print("Exiting system...")
        break

    else:
        print("Invalid choice. Please try again.")