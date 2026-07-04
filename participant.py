class Participant:

    def __init__(self, id, event_id, name, email, contact, registration_date, attendance=False):
        self.id = id
        self.event_id = event_id
        self.name = name
        self.email = email
        self.contact = contact
        self.registration_date = registration_date
        self.attendance = attendance


    def to_dict(self):
        return {
            "id": self.id,
            "event_id": self.event_id,
            "name": self.name,
            "email": self.email,
            "contact": self.contact,
            "registration_date": self.registration_date,
            "attendance": self.attendance
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["event_id"],
            data["name"],
            data["email"],
            data["contact"],
            data["registration_date"],
            data.get("attendance", False)
        )