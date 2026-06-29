import json
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

    def load_events(self):
        try:
            with open("events.json", "r") as file:
                data = json.load(file)
                return [Event.from_dict(event) for event in data]
        except FileNotFoundError:
            return []

    def save_events(self):
        with open("events.json", "w") as file:
            json.dump(
                [event.to_dict() for event in self.events],
                file,
                indent=4
            )

    def get_next_id(self):
        used_ids = {event.id for event in self.events}

        next_id = 1

        while next_id in used_ids:
            next_id += 1

        return next_id
    
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
    
    def add_event(self):
        print("\n===== ADD EVENT =====")

        name = input("Enter event name: ")
        date = input("Enter event date (YYYY-MM-DD): ")
        time = input("Enter event time (HH:MM): ")
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

    def view_events(self):

        if not self.events:
            print("\nNo events found.")
            return

        print("\n===== EVENT LIST =====")

        for event in self.events:
            self.display_event(event)

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