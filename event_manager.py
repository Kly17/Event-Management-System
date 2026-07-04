import json
from datetime import datetime
from event import Event
from participant import Participant


class EventManager:

    #CONSTRUCTOR
    def __init__(self):
        self.events = self.load_events()
        self.page_size = 5
        self.participants = self.load_participants()
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
        except (FileNotFoundError, json.JSONDecodeError):
            with open("events.json", "w") as file:
                json.dump([], file)
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
    
    #========================================================================
    #EVENT MENU
    def event_menu(self):

        while True:

            print("\n========== EVENT MANAGEMENT ==========")
            print("1. Add Event")
            print("2. View Events")
            print("3. Edit Event")
            print("4. Delete Event")
            print("5. Search Event")
            print("6. Sort Events")
            print("7. Filter Events")
            print("8. Back")

            choice = input("\nEnter your choice: ")

            if choice == "1":
                self.add_event()

            elif choice == "2":
                self.view_events()

            elif choice == "3":
                self.edit_event()

            elif choice == "4":
                self.delete_event()

            elif choice == "5":
                self.search_event()

            elif choice == "6":
                self.sort_events()

            elif choice == "7":
                self.filter_events()

            elif choice == "8":
                break

            else:
                print("Invalid choice.")

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
    #VIEW EVENTS PAGINATED
    def view_events(self):
       
        if not self.events:
            print("\nNo events available.")
            return
        
        page = 0

        while True:
            total_events = (len(self.events) )
            total_pages = (total_events - 1)//self.page_size + 1

            start = page * self.page_size
            end = start + self.page_size

            current_page_events = self.events[start:end]

            print (f"\n===== EVENT LIST (Page {page + 1} of {total_pages}) =====")
            print(f"Showing events {start + 1} to {min(end, total_events)} of {total_events}\n")
            print("=" * 50)

            for event in current_page_events:
                self.display_event(event)
            
            print("\nNavigation Options:")
            print("N - Next Page")
            print("P - Previous Page")
            print("S - Go to Specific Page")
            print("E - Exit to Main Menu")

            choice = input("Enter your choice: ").strip().lower()

            if choice == "n":
                if page < total_pages - 1:
                    page += 1
                else:
                    print("You are on the last page.")
            elif choice == "p":
                if page > 0:
                    page -= 1
                else:
                    print("You are on the first page.")
            elif choice == "s":
                try:
                    specific_page = int(input(f"Enter page number (1 to {total_pages}): ")) - 1
                    if 0 <= specific_page < total_pages:
                        page = specific_page
                    else:
                        print("Invalid page number.")
                except ValueError:
                    print("Please enter a valid number.")
            elif choice == "e":
                break
            else:
                print("Invalid choice. Please try again.")
            
            

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
        print(f"Total Participants : {len(self.participants)}")
    
        self.show_category_statistics()
        self.show_capacity_statistics()
        self.show_registration_statistics()

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
    
    #=========================================================================
    #NO VALIDATE NON EMPTY INPUT
    def validate_non_empty(self, prompt):

        while True:

            value = input(prompt).strip()

            if value:
                return value

            print("This field cannot be empty.")

    #=========================================================================
    #PARTICIPANT MENU
    def participant_menu(self):

        while True:

            print("\n========== PARTICIPANT MANAGEMENT ==========")
            print("1. Register Participant")
            print("2. View Participants")
            print("3. Search Participant")
            print("4. Edit Participant")
            print("5. Delete Participant")
            print("6. View Participants by Event")
            print("7. Back")

            choice = input("\nEnter your choice: ")

            if choice == "1":
                self.register_participant()

            elif choice == "2":
                self.view_participants()

            elif choice == "3":
                self.search_participant()

            elif choice == "4":
                self.edit_participant()

            elif choice == "5":
                self.delete_participant()
            
            elif choice == "6":
                self.view_participants_by_event()

            elif choice == "7":
                break

            else:
                print("Invalid choice.")
    #=========================================================================
    #LOAD PARTICIPANTS
    def load_participants(self):

        try:
            with open("participants.json", "r") as file:
                data = json.load(file)
                return [Participant.from_dict(participant) for participant in data]
    
        except (FileNotFoundError, json.JSONDecodeError):
        
            print("participants.json not found or is invalid.")
            print("Creating a new participants.json file...")
    
            with open("participants.json", "w") as file:
                json.dump([], file, indent=4)
    
            return []
    
    #=========================================================================
    #SAVE PARTICIPANTS
    def save_participants(self):

        with open("participants.json", "w") as file:
            json.dump(
                [participant.to_dict() for participant in self.participants],
                file,
                indent=4
            )
    
    #=========================================================================
    #GET PARTICIPANT BY ID 
    def get_next_participant_id(self):

        used_ids = {participant.id for participant in self.participants}

        next_id = 1

        while next_id in used_ids:
            next_id += 1

        return next_id


    #=========================================================================
    #FIND PARTICIPANT BY ID
    def find_participant_by_id(self, participant_id):

        for participant in self.participants:

            if participant.id == participant_id:
                return participant

        return None

    #=========================================================================
    #FIND PARTICIPANT BY EVENT ID
    def find_participants_by_event(self, event_id):


        return [
            participant
            for participant in self.participants
            if participant.event_id == event_id
        ]
    

    #=========================================================================
    #PARTICIPANT ALREADY REGISTERED CHECK
    def is_already_registered(self, event_id, email):

        for participant in self.participants:

            if (
                participant.event_id == event_id
                and participant.email.lower() == email.lower()
            ):
                return True

        return False
    
    #=========================================================================
    #REGISTER PARTICIPANT
    def register_participant(self):
        if not self.events:
            print("\nNo events available for registration.")
            return

        print("\n===== REGISTER FOR EVENT =====")
        for event in self.events:
            print(f"ID: {event.id} | Name: {event.name} | Date: {event.date} | Time: {event.time} | Location: {event.location}")

        try:
            event_id = int(input("\nEnter the Event ID to register for: "))

        except ValueError:
            print("Please enter a valid number.")
            return

        event = self.find_event_by_id(event_id)

        if event is None:
            print("Event not found.")
            return

        registered = len(self.find_participants_by_event(event_id))

        if registered >= event.capacity:
            print("Event is full. Registration closed.")
            return

        print(f"\nRegistering for '{event.name}' on {event.date} at {event.time} in {event.location}.")
        print(f"Current Registrations: {registered}/{event.capacity}")

        print("\nPlease provide your details for registration.")
        
        while True:

            name = self.validate_non_empty("Enter your name: ")
            email = self.validate_non_empty("Enter your email: ")
            contact = self.validate_non_empty("Enter your contact number: ")

            if not name or not email or not contact:
                print("All fields are required. Please try again.")
                continue
            break

        if self.is_already_registered(event_id, email):
                print("You are already registered for this event.")
                return

        new_participant = Participant(
            id=self.get_next_participant_id(),
            event_id=event_id,
            name=name,
            email=email,
            contact=contact,
            registration_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        self.participants.append(new_participant)
        self.save_participants()

        print("\n==========================================")
        print("Participant registered successfully!")
        print("==========================================")
        print(f"Participant ID : {new_participant.id}")
        print(f"Event          : {event.name}")
        print(f"Participant    : {new_participant.name}")
        print(f"Email          : {new_participant.email}")
        print(f"Contact        : {new_participant.contact}")
    
    #=========================================================================
    #DISPLAY PARTICIPANTS
    def display_participant(self, participant):

        event = self.find_event_by_id(participant.event_id)

        if event:
            event_name = event.name
        else:
            event_name = "Unknown Event"

        print("----------------------------------------")
        print(f"Participant ID : {participant.id}")
        print(f"Event ID       : {participant.event_id}")
        print(f"Event Name     : {event_name}")
        print(f"Name           : {participant.name}")
        print(f"Email          : {participant.email}")
        print(f"Contact        : {participant.contact}")

        # Only display this if your Participant class has it
        if hasattr(participant, "registration_date"):
            print(f"Registered On  : {participant.registration_date}")

        print("----------------------------------------")

    #==========================================================================
    #VIEW PARTICIPANTS
    def view_participants(self):

        if not self.participants:
            print("\nNo participants found.")
            return
        print("\n========== PARTICIPANTS ==========")
        for participant in self.participants:
            self.display_participant(participant)

    #=========================================================================
    #SEARCH PARTICIPANTS
    def search_participant(self):

        if not self.participants:
            print("\nNo participants found.")
            return

        search_term = input(
            "\nEnter Participant ID, Name, Email, Contact, or Event Name: "
        ).strip().lower()

        found_participants = []

        for participant in self.participants:

            event = self.find_event_by_id(participant.event_id)

            event_name = ""
            if event:
                event_name = event.name.lower()

            if (
                search_term == str(participant.id)
                or search_term in participant.name.lower()
                or search_term in participant.email.lower()
                or search_term in participant.contact.lower()
                or search_term in event_name
            ):
                found_participants.append(participant)

        if not found_participants:
            print("\nNo matching participants found.")
            return

        print(f"\nFound {len(found_participants)} participant(s).\n")

        for participant in found_participants:
            self.display_participant(participant)
    
    #=========================================================================
    #EDIT PARTICIPANTS
    def edit_participant(self):

        if not self.participants:
            print("\nNo participants available to edit.")
            return

        self.view_participants()

        try:
            participant_id = int(input("\nEnter the Participant ID to edit: "))

        except ValueError:
            print("Please enter a valid number.")
            return

        participant = self.find_participant_by_id(participant_id)

        if participant is None:
            print("Participant not found.")
            return

        print("\nLeave blank to keep the current value.")

        new_name = input(f"Name ({participant.name}): ").strip()
        new_email = input(f"Email ({participant.email}): ").strip()
        new_contact = input(f"Contact ({participant.contact}): ").strip()

        # Use existing values if left blank
        check_email = new_email if new_email else participant.email

        # Prevent duplicate registration
        if (
            check_email.lower() != participant.email.lower()
            and self.is_already_registered(participant.event_id, check_email)
        ):
            print("\nAnother participant is already registered for this event using that email.")
            return

        if new_name:
            participant.name = new_name

        if new_email:
            participant.email = new_email

        if new_contact:
            participant.contact = new_contact

        self.save_participants()

        print("\nParticipant updated successfully!")
    
    #=========================================================================
    #DELETE PARTICIPANTS
    def delete_participant(self):

        if not self.participants:
            print("\nNo participants available.")
            return

        self.view_participants()

        try:
            participant_id = int(input("\nEnter the Participant ID to delete: "))

        except ValueError:
            print("Please enter a valid number.")
            return

        participant = self.find_participant_by_id(participant_id)

        if participant is None:
            print("Participant not found.")
            return

        event = self.find_event_by_id(participant.event_id)

        print("\n========== PARTICIPANT DETAILS ==========")
        print(f"Participant ID : {participant.id}")
        print(f"Name           : {participant.name}")
        print(f"Email          : {participant.email}")
        print(f"Contact        : {participant.contact}")
        print(f"Event          : {event.name if event else 'Unknown Event'}")

        confirm = input("\nAre you sure you want to delete this participant? (Y/N): ").strip().lower()

        if confirm != "y":
            print("\nDeletion cancelled.")
            return

        self.participants.remove(participant)

        self.save_participants()

        print("\nParticipant deleted successfully!")

    #=========================================================================
    #VIEW PARTICIPANTS BY EVENT
    def view_participants_by_event(self):

        if not self.events:
            print("\nNo events available.")
            return

        print("\n========== EVENTS ==========")

        for event in self.events:
            print(f"ID: {event.id} | {event.name}")

        try:
            event_id = int(input("\nEnter Event ID: "))

        except ValueError:
            print("Please enter a valid number.")
            return

        event = self.find_event_by_id(event_id)

        if event is None:
            print("Event not found.")
            return

        participants = self.find_participants_by_event(event_id)

        print("\n========================================")
        print(f"Participants for: {event.name}")
        print("========================================")

        if not participants:
            print("\nNo participants registered for this event.")
            return

        for participant in participants:
            self.display_participant(participant)

        print("----------------------------------------")
        print(f"Total Registered : {len(participants)}")
        print(f"Capacity         : {event.capacity}")
        print(f"Remaining Slots  : {event.capacity - len(participants)}")

        if len(participants) >= event.capacity:
            print("Status           : FULL")
        else:
            print("Status           : OPEN")

    
    #=========================================================================
    #REGISTRATION STATISTICS
    def show_registration_statistics(self):

        print("\n========== REGISTRATION STATISTICS ==========")

        print(
            f"{'ID':<4}"
            f"{'Event Name':<30}"
            f"{'Reg/Cap':<12}"
            f"{'Remaining':<12}"
            f"{'% Full':<10}"
            f"{'Status'}"
        )

        print("-" * 80)

        total_registered = 0

        for event in self.events:

            registered = len(self.find_participants_by_event(event.id))
            remaining = event.capacity - registered

            percent = (registered / event.capacity) * 100 if event.capacity > 0 else 0

            status = "FULL" if remaining == 0 else "OPEN"

            total_registered += registered

            print(
                f"{event.id:<4}"
                f"{event.name[:28]:<30}"
                f"{f'{registered}/{event.capacity}':<12}"
                f"{remaining:<12}"
                f"{f'{percent:.1f}%':<10}"
                f"{status}"
            )

        print("-" * 80)
        print(f"Total Registered Participants : {total_registered}")