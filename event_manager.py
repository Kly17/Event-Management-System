import json
from datetime import datetime
from event import Event


class EventManager:

    #CONSTRUCTOR
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
    #DUPLICATOR DETECTION
    def is_duplicate_event(self, name, date, time, exclude_id=None):

        print(f"\nChecking new event:")
        print(f"Name : '{name}'")
        print(f"Date : '{date}'")
        print(f"Time : '{time}'")

        for event in self.events:

            print("\nComparing with:")
            print(f"Name : '{event.name}'")
            print(f"Date : '{event.date}'")
            print(f"Time : '{event.time}'")

            print("Name Match:", event.name.strip().lower() == name.strip().lower())
            print("Date Match:", event.date == date)
            print("Time Match:", event.time == time)

            if exclude_id is not None and event.id == exclude_id:
                continue

            if (
                event.name.strip().lower() == name.strip().lower()
                and event.date == date
                and event.time == time
            ):
                print(">>> DUPLICATE FOUND <<<")
                return True

        print(">>> NO DUPLICATE <<<")
        return False

    #========================================================================
    #CONFLICT DETECTION
    def has_schedule_conflict(self, location, date, time, exclude_id=None):

        for event in self.events:

            if exclude_id is not None and event.id == exclude_id:
                continue

            if (
                event.location.lower() == location.lower()
                and event.date == date
                and event.time == time
            ):
                return event

        return None


    #========================================================================    
    #VALIDATE DATE AND TIME
    def validate_input(self, prompt, format_string, error_message, allow_empty=False):

        while True:

            value = input(prompt).strip()

            if allow_empty and not value :
                return ""

            try:
                datetime.strptime(value, format_string)
                return value

            except ValueError:
                print(error_message)
    
    #========================================================================
    #VALIDATE CAPACITY
    def validate_capacity(self, prompt, allow_empty=False):

        while True:

            value = input(prompt).strip()

            if allow_empty and value == "":
                return ""

            try:
                capacity = int(value)

                if capacity > 0:
                    return capacity

                print("Capacity must be greater than 0.")

            except ValueError:
                print("Please enter a valid number.")
    
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
    #GET EVENT IDs
    def get_next_id(self):
        used_ids = {event.id for event in self.events}

        next_id = 1

        while next_id in used_ids:
            next_id += 1

        return next_id

    #========================================================================
    #FIND EVENT BY ID
    def find_event_by_id(self, event_id):

        for event in self.events:
            if event.id == event_id:
                return event

        return None
    
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
        capacity = self.validate_capacity("Enter event capacity: ")
        location = input("Enter event location: ")
        category = self.select_category()

        if self.is_duplicate_event(name, date, time):
            print("\nDuplicate event detected. Event not added.")
            return
        
        conflict = self.has_schedule_conflict(
            location,
            date,
            time
        )
        if conflict:
            print("\nSchedule conflict detected!")
            print(f"'{conflict.name}' is already scheduled.")
            print(f"Location : {conflict.location}")
            print(f"Date     : {conflict.date}")
            print(f"Time     : {conflict.time}")
            return
        

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

        event = self.find_event_by_id(event_id)

        if event is None:
            print("Event not found.")
            return

        print("\nLeave blank to keep the current value.")

        new_name = input(f"Name ({event.name}): ")
        new_date = self.validate_input(f"Date ({event.date}) [Press Enter to Keep Date]: ", "%Y-%m-%d", "Invalid date format. Please use YYYY-MM-DD.", allow_empty=True)
        new_time = self.validate_input(f"Time ({event.time}) [Press Enter to Keep Time]: ", "%H:%M", "Invalid time format. Please use HH:MM (24-hour format).", allow_empty=True)
        new_description = input(f"Description ({event.description}): ")
        new_capacity = self.validate_capacity(f"Capacity ({event.capacity}) [Press Enter to Keep]: ", allow_empty=True)
        new_location = input(f"Location ({event.location}): ")
        new_category = event.category
        change_category = input(f"Change category? (Y/N) [Current: {event.category}]: ").lower()
        if change_category == "y":
            new_category = self.select_category()
        
        check_name = new_name if new_name else event.name
        check_date = new_date if new_date else event.date
        check_time = new_time if new_time else event.time
        check_location = new_location if new_location else event.location

        if self.is_duplicate_event(
            check_name,
            check_date,
            check_time,
            exclude_id=event.id
        ):
            print("\nDuplicate event detected. Event not updated.")
            return
        
        conflict = self.has_schedule_conflict(
            check_location,
            check_date,
            check_time,
            exclude_id=event.id
        )

        if conflict:
            print("\nSchedule conflict detected!")
            print(f"'{conflict.name}' is already scheduled.")
            print(f"Location : {conflict.location}")
            print(f"Date     : {conflict.date}")
            print(f"Time     : {conflict.time}")
            return

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
                    print("Capacity must be greater than 0.")
        
            except ValueError:
                print("Please enter a valid number.")
        
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
    #SORT EVENTS
    def sort_events(self):

        if not self.events:
            print("\nNo events available.")
            return

        while True:

            print("\n===== SORT EVENTS =====")
            print("1. Sort by ID")
            print("2. Sort by Date")
            print("3. Sort by Name")
            print("4. Sort by Category")
            print("5. Sort by Capacity")
            print("6. Sort by Location")
            print("7. Back")

            choice = input("Enter your choice: ")

            if choice == "1":

                print("\nChoose sort Order:")
                print("1. Ascending")
                print("2. Descending\n")
                order = input("Sort Order: ")
                if order == "1":
                    self.events.sort(key = lambda event: event.id)
                elif order == "2":
                    self.events.sort(key = lambda event: event.id, reverse = True)
                else:
                    print("Invalid Sort Order")
                    continue

            elif choice == "2":
                self.events.sort(key=lambda event: event.date)
                print("\nEvents sorted by date.")

            elif choice == "3":
                self.events.sort(key=lambda event: event.name.lower())
                print("\nEvents sorted by name.")

            elif choice == "4":
                self.events.sort(key=lambda event: event.category.lower())
                print("\nEvents sorted by category.")

            elif choice == "5":
                self.events.sort(key=lambda event: event.capacity)
                print("\nEvents sorted by capacity.")

            elif choice == "6":
                self.events.sort(key=lambda event: event.location.lower())
                print("\nEvents sorted by location.")

            elif choice == "7":
                break

            else:
                print("Invalid choice.")
                continue

            self.view_events()
    
    #=========================================================================
    #FILTER BY CATEGORY
    def filter_by_category(self):

        category = self.select_category()

        filtered_events = [
            event for event in self.events
            if event.category == category
        ]

        if not filtered_events:
            print("\nNo events found.")
            return

        print(f"\n===== {category.upper()} EVENTS =====")

        for event in filtered_events:
            self.display_event(event)

    
    #=========================================================================
    #FILTER BY LOCATION
    def filter_by_location(self):

        location = input("Enter location: ").strip().lower()

        filtered_events = [
            event for event in self.events
            if location in event.location.lower()
        ]

        if not filtered_events:
            print("\nNo events found.")
            return

        for event in filtered_events:
            self.display_event(event)
    
    #=========================================================================
    #FILTER BY MONTH
    def filter_by_month(self):

        month = input("Enter month (01-12): ")
        filtered_events = [
            event for event in self.events
            if event.date[5:7] == month
        ]
        if not filtered_events:
            print("\nNo events found.")
            return
        for event in filtered_events:
            self.display_event(event)
    
    #=========================================================================
    #FILTER BY CAPACITY
    def filter_by_capacity(self):

        try:
            minimum = int(input("Minimum capacity: "))
            maximum = int(input("Maximum capacity: "))

        except ValueError:
            print("Invalid capacity.")
            return

        filtered_events = [
            event for event in self.events
            if minimum <= event.capacity <= maximum
        ]

        if not filtered_events:
            print("\nNo events found.")
            return

        for event in filtered_events:
            self.display_event(event)

    #=========================================================================
    #FILTER EVENTS
    def filter_events(self):

        if not self.events:
            print("\nNo events available.")
            return

        while True:

            print("\n===== FILTER EVENTS =====")
            print("1. Filter by Category")
            print("2. Filter by Location")
            print("3. Filter by Month")
            print("4. Filter by Capacity")
            print("5. Back")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.filter_by_category()

            elif choice == "2":
                self.filter_by_location()

            elif choice == "3":
                self.filter_by_month()

            elif choice == "4":
                self.filter_by_capacity()

            elif choice == "5":
                break

            else:
                print("Invalid choice.")

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

        event = self.find_event_by_id(event_id)

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

        if not search_term:
            print("Search term cannot be empty.")
            return

        found_events = [
            event for event in self.events
            if (
                search_term in event.name.lower()
                or search_term in event.category.lower()
                or search_term in event.description.lower()
                or search_term in event.location.lower()
            )
        ]
        if not found_events:
            print("\nNo matching events found.")
            return

        print(f"\nFound {len(found_events)} event(s).\n")

        for event in found_events:
            self.display_event(event)

    #=========================================================================
    #CATEGORY STATISTICS
    def show_category_statistics(self):

        print("\n----- Events by Category -----")

        category_count = {}

        for event in self.events:

            if event.category not in category_count:
                category_count[event.category] = 0

            category_count[event.category] += 1

        for category, total in sorted(category_count.items()):
            print(f"{category}: {total}")
    
    #========================================================================
    #CAPACITY STATISTICS
    def show_capacity_statistics(self):

        print("\n----- Capacity Statistics -----")

        total_capacity = sum(event.capacity for event in self.events)

        average_capacity = total_capacity / len(self.events)

        largest = max(self.events, key=lambda event: event.capacity)

        smallest = min(self.events, key=lambda event: event.capacity)

        print(f"Total Capacity : {total_capacity}")
        print(f"Average Capacity : {average_capacity:.2f}")

        print("\nLargest Event")
        print(f"{largest.name} ({largest.capacity})")

        print("\nSmallest Event")
        print(f"{smallest.name} ({smallest.capacity})")
    
    #=========================================================================
    #DASHBOARD
    def dashboard(self):

        if not self.events:
            print("\nNo events available.")
            return
    
        print("\n========== EVENT DASHBOARD ==========")
    
        print(f"\nTotal Events : {len(self.events)}")
    
        self.show_category_statistics()
        self.show_capacity_statistics()

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