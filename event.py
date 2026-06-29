class Event:
    def __init__(self, event_id, name, category, date, time, description, capacity, location):
        self.id = event_id
        self.name = name
        self.category = category
        self.date = date
        self.time = time
        self.description = description
        self.capacity = capacity
        self.location = location

    def to_dict(self):
        """Convert the Event object into a dictionary for JSON storage."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "date": self.date,
            "time": self.time,
            "description": self.description,
            "capacity": self.capacity,
            "location": self.location
        }

    @classmethod
    def from_dict(cls, data):
        """Create an Event object from a dictionary."""
        return cls(
            event_id=data["id"],
            name=data["name"],
            category=data["category"],
            date=data["date"],
            time=data["time"],
            description=data["description"],
            capacity=data["capacity"],
            location=data["location"]
        )