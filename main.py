# Event Management System

import json

def select_category(categories):
    while True:
        print("\n===== EVENT CATEGORIES =====")

        for i, category in enumerate(categories, start=1):
            print(f"{i}. {category}")

        try:
            choice = int(input("Select a category: "))

            if 1 <= choice <= len(categories):
                return categories[choice - 1]

            print("Invalid category.")

        except ValueError:
            print("Please enter a valid number.")

def load_events():
    try:
        with open("events.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def save_events(events):
    with open("events.json", "w") as file:
        json.dump(events, file, indent=4)
        
def get_next_id(events):

    used_ids = {event["id"] for event in events}

    next_id = 1

    while next_id in used_ids:
        next_id += 1

    return next_id

events = load_events()

categories = [
    "Academic",
    "Career",
    "Ceremony",
    "Community Service",
    "Competition",
    "Conference",
    "Festival",
    "Meeting",
    "Seminar",
    "Training",
    "Workshop",
    "Others"
]

while True:
    print("\n===== EVENT MANAGEMENT SYSTEM =====")
    print("1. Add Event")
    print("2. View Events")
    print("3. Edit Event")
    print("4. Delete Event")
    print("5. Search Event")
    print("6. Exit")

    choice = input("Enter your choice: ")

    # ADD EVENT
    if choice == "1":
        event_name = input("Enter event name: ")
        event_date = input("Enter event date (YYYY-MM-DD): ")
        event_time = input("Enter event time (HH:MM): ")
        event_description = input("Enter event description: ")

        while True:
            try:
                event_capacity = int(input("Enter event capacity: "))

                if event_capacity > 0:
                    break
                
                print("Capacity must be a greater than 0.")

            except ValueError:
                print("Please enter a valid number for capacity.")
        event_location = input("Enter event location: ")
        event_category = select_category(categories)
            

        event = {
            "id": get_next_id(events),
            "name": event_name,
            "category": event_category,
            "date": event_date,
            "time": event_time,
            "description": event_description,
            "capacity": event_capacity,
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
                    "=============================="
                    f"\nID: {event['id']} \n"
                    f"\nName: {event['name']} "
                    f"\nCategory: {event['category']} "
                    f"\nTime: {event['time']} "
                    f"\nDate: {event['date']} "
                    f"\nDescription: {event['description']} "
                    f"\nCapacity: {event['capacity']} "
                    f"\nLocation: {event['location']}\n"
                    "==============================\n")

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
                    new_time = input(
                        f"New time ({event['time']}): ")
                    new_description = input(
                        f"New description ({event['description']}): ")
                    new_capacity = input(
                        f"New capacity ({event['capacity']}): ")
                    print("\Do you want to change the category?")
                    change_category = input("Enter 'y' for yes or 'n' for no: ").strip().lower()
                    if change_category == 'y':
                        new_category = select_category(categories)
                    else:
                        new_category = event['category']
                    new_location = input(
                        f"New location ({event['location']}): ")

                    if new_name:
                        event['name'] = new_name
                    if new_date:
                        event['date'] = new_date
                    if new_time:
                        event['time'] = new_time
                    if new_description:
                        event['description'] = new_description
                    if new_capacity:
                        event['capacity'] = int(new_capacity)
                    if new_category:
                        event['category'] = new_category
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
                    f"{i}. \n{event['name']}\n{event['date']}\n{event['location']}{event['category']}\n{event['time']}\n{event['description']}\n{event['capacity']}\n")

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
    
    #SEARCH EVENT
    elif choice == "5":
        search_term = input("Enter event name to search: ").strip().lower()
        found_events = [event for event in events 
                        if search_term in event['name'].lower()
                        or search_term in event['description'].lower()
                        or search_term in event['category'].lower()
                        or search_term in event['location'].lower()]

        if found_events:
            print(f"\nFound {len(found_events)} event(s).")
            print("\n--- Search Results ---")

            for i, event in enumerate(found_events, start=1):
                print(f"{i}. \n{event['name']}\n{event['date']}\n{event['location']}{event['category']}\n{event['time']}\n{event['description']}\n{event['capacity']}\n")

        else:
            print("No events found matching the search term.")


    # EXIT
    elif choice == "6":
        print("Exiting system...")
        break

    else:
        print("Invalid choice. Please try again.")