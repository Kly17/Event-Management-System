import json
from datetime import datetime
from event import Event


class EventManager:

    def __init__(self):
        self.events = self.load_events()
        self.categories = [
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
    #========================================================================    
    #VALIDATE DATE AND TIME
    def validate_input(self, prompt, format_string, error_message, allow_empty=False):

        while True:

            value = input(prompt).strip()

            if allow_empty and value == "":
                return ""

            try:
                datetime.strptime(value, format_string)
                return value

            except ValueError:
                print(error_message)
    
    #========================================================================
    # LOAD EVENTS IN JSON FILE
    def load_events(self):
        try:
            with open("events.json", "r") as file:
                data = json.load(file)
                return [Event.from_dict(event) for event in data]
        except FileNotFoundError:
            return []
        
    #SAVE EVENTS IN JSON FILE
    def save_events(self):
        with open("events.json", "w") as file:
            json.dump(
                [event.to_dict() for event in self.events],
                file,
                indent=4
            )

    #=========================================================================
    #EVENT IDs
    def get_next_id(self):
        used_ids = {event.id for event in self.events}

        next_id = 1

        while next_id in used_ids:
            next_id += 1

        return next_id
    
    #=========================================================================
    #EVENT CATEGORY PICKER
    def select_category(self):
        while True:

            print("\n===== EVENT CATEGORIES =====")

            for i, category in enumerate(self.categories, start=1):
                print(f"{i}. {category}")

            try:
                choice = int(input("Select a category: "))

                if 1 <= choice <= len(self.categories):
                    return self.categories[choice - 1]

                print("Invalid category.")

            except ValueError:
                print("Please enter a valid number.")
    
    
    #=========================================================================
    #ADD EVENTS
    def add_event(self):
        print("\n===== ADD EVENT =====")

        name = input("Enter event name: ")
        date = self.validate_input("Enter event date (YYYY-MM-DD): ", "%Y-%m-%d", "Invalid date format. Please use YYYY-MM-DD.")
        time = self.validate_input("Enter event time in 24-hour format (HH:MM): ", "%H:%M", "Invalid time format. Please use HH:MM (24-hour format).")
        description = input("Enter event description: ")

        while True:
            try:
                capacity = int(input("Enter event capacity: "))

                if capacity > 0:
                    break

                print("Capacity must be greater than 0.")

            except ValueError:
                print("Please enter a valid number.")

        location = input("Enter event location: ")
        category = self.select_category()

        new_event = Event(
            event_id=self.get_next_id(),
            name=name,
            category=category,
            date=date,
            time=time,
            description=description,
            capacity=capacity,
            location=location
        )

        self.events.append(new_event)
        self.save_events()

        print("\nEvent added successfully!")


    #=========================================================================
    #EDIT EVENTS
    def edit_event(self):

        if not self.events:
            print("\nNo events available to edit.")
            return

        self.view_events()

        try:
            event_id = int(input("\nEnter the Event ID to edit: "))

        except ValueError:
            print("Please enter a valid number.")
            return

        event = None

        for e in self.events:
            if e.id == event_id:
                event = e
                break

        if event is None:
            print("Event not found.")
            return

        print("\nLeave blank to keep the current value.")

        new_name = input(f"Name ({event.name}): ")
        new_date = self.validate_input(f"Date ({event.date}) [Press Enter to Keep Date]: ", "%Y-%m-%d", "Invalid date format. Please use YYYY-MM-DD.")
        new_time = self.validate_input(f"Time ({event.time}) [Press Enter to Keep Time]: ", "%H:%M", "Invalid time format. Please use HH:MM (24-hour format).")
        new_description = input(f"Description ({event.description}): ")
        new_capacity = input(f"Capacity ({event.capacity}): ")
        new_location = input(f"Location ({event.location}): ")

        change_category = input("Change category? (Y/N): ").lower()

        if change_category == "y":
            event.category = self.select_category()

        if new_name:
            event.name = new_name

        if new_date:
            event.date = new_date

        if new_time:
            event.time = new_time

        if new_description:
            event.description = new_description

        if new_capacity:
            try:
                capacity = int(new_capacity)

                if capacity > 0:
                    event.capacity = capacity
                else:
                    print("Invalid capacity. Keeping old value.")

            except ValueError:
                print("Invalid capacity. Keeping old value.")

        if new_location:
            event.location = new_location

        self.save_events()

        print("\nEvent updated successfully!")
    

    #=========================================================================
    #VIEW EVENTS
    def view_events(self):

        if not self.events:
            print("\nNo events found.")
            return

        print("\n===== EVENT LIST =====")

        for event in self.events:
            self.display_event(event)
    
    
    #=========================================================================
    #DELETE EVENTS
    def delete_event(self):

        if not self.events:
            print("\nNo events available to delete.")
            return

        self.view_events()

        try:
            event_id = int(input("\nEnter the Event ID to delete: "))

        except ValueError:
            print("Please enter a valid number.")
            return

        event = None

        for e in self.events:
            if e.id == event_id:
                event = e
                break

        if event is None:
            print("Event not found.")
            return

        print("\nSelected Event:")
        self.display_event(event)

        confirm = input("Are you sure you want to delete this event? (Y/N): ").lower()

        if confirm == "y":
            self.events.remove(event)
            self.save_events()
            print("Event deleted successfully!")

        else:
            print("Deletion cancelled.")
    

    #=========================================================================
    #SEARCH EVENTS
    def search_event(self):

        if not self.events:
            print("\nNo events available.")
            return

        search_term = input("\nEnter a keyword to search: ").strip().lower()

        found_events = [
            event for event in self.events 
            if search_term in event.name.lower()
            or search_term in event.category.lower()
            or search_term in event.description.lower()
            or search_term in event.location.lower()
        ]

        for event in self.events:

            if (
                search_term in event.name.lower()
                or search_term in event.category.lower()
                or search_term in event.description.lower()
                or search_term in event.location.lower()
            ):
                found_events.append(event)

        if not found_events:
            print("\nNo matching events found.")
            return

        print(f"\nFound {len(found_events)} event(s).\n")

        for event in found_events:
            self.display_event(event)

    #=========================================================================
    # DISPLAY TEXT
    def display_event(self, event):
        print("=" * 50)
        print(f"Event ID    : {event.id}")
        print(f"Name        : {event.name}")
        print(f"Category    : {event.category}")
        print(f"Date        : {event.date}")
        print(f"Time        : {event.time}")
        print(f"Location    : {event.location}")
        print(f"Capacity    : {event.capacity}")
        print(f"Description : {event.description}")
        print("=" * 50)