import sqlite3
import json
import os

from event import Event
from participant import Participant

class Database:

    
#========================== Initialization ==========================
    def __init__(self):

        self.connection = sqlite3.connect("event_management.db")

        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        self.create_tables()


    def create_tables(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS events(

                id INTEGER PRIMARY KEY,

                name TEXT NOT NULL,

                category TEXT NOT NULL,

                date TEXT NOT NULL,

                time TEXT NOT NULL,

                description TEXT,

                capacity INTEGER NOT NULL,

                location TEXT NOT NULL

            )
        """)


        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS participants(

                id INTEGER PRIMARY KEY,

                event_id INTEGER NOT NULL,

                name TEXT NOT NULL,

                email TEXT NOT NULL,

                contact TEXT NOT NULL,

                registration_date TEXT,

                attendance INTEGER DEFAULT 0,

                FOREIGN KEY(event_id)
                REFERENCES events(id)

            )
        """)

        self.connection.commit()

    #========================= Import JSON Files =========================

    def import_json_data(self):

        # ==========================
        # Import Events
        # ==========================

        if os.path.exists("events.json"):

            with open("events.json", "r") as file:
                events = json.load(file)

            count = self.cursor.execute(
                "SELECT COUNT(*) FROM events"
            ).fetchone()[0]

            if count == 0:

                for event in events:

                    self.cursor.execute("""
                        INSERT INTO events(
                            id,
                            name,
                            category,
                            date,
                            time,
                            description,
                            capacity,
                            location
                        )
                        VALUES(?,?,?,?,?,?,?,?)
                    """, (

                        event["id"],
                        event["name"],
                        event["category"],
                        event["date"],
                        event["time"],
                        event["description"],
                        event["capacity"],
                        event["location"]

                    ))

                print("Events imported successfully!")

        # ==========================
        # Import Participants
        # ==========================

        if os.path.exists("participants.json"):

            with open("participants.json", "r") as file:
                participants = json.load(file)

            count = self.cursor.execute(
                "SELECT COUNT(*) FROM participants"
            ).fetchone()[0]

            if count == 0:

                for participant in participants:

                    self.cursor.execute("""
                        INSERT INTO participants(
                            id,
                            event_id,
                            name,
                            email,
                            contact,
                            registration_date,
                            attendance
                        )
                        VALUES(?,?,?,?,?,?,?)
                    """, (

                        participant["id"],
                        participant["event_id"],
                        participant["name"],
                        participant["email"],
                        participant["contact"],
                        participant["registration_date"],
                        int(participant["attendance"])

                    ))

                print("Participants imported successfully!")

        self.connection.commit()



    #========================= Export JSON Files =========================
    #========================== Export Events =========================
    def get_all_events(self):
        self.cursor.execute("""
            SELECT *
            FROM events
            ORDER BY id
        """)

        rows = self.cursor.fetchall()

        return [
            Event(
                row["id"],
                row["name"],
                row["category"],
                row["date"],
                row["time"],
                row["description"],
                row["capacity"],
                row["location"]
            )
            for row in rows
        ]

    #========================== Export Participants =========================

    def get_all_participants(self):
        self.cursor.execute("""
            SELECT *
            FROM participants
            ORDER BY id
        """)
    
        rows = self.cursor.fetchall()
    
        return [
            Participant(
                row["id"],
                row["event_id"],
                row["name"],
                row["email"],
                row["contact"],
                row["registration_date"],
                bool(row["attendance"])
            )
            for row in rows
        ]

    #========================= Add to Database =========================

    def add_event(self, event):
        self.cursor.execute("""
            INSERT INTO events (
                id,
                name,
                category,
                date,
                time,
                description,
                capacity,
                location
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event.id,
            event.name,
            event.category,
            event.date,
            event.time,
            event.description,
            event.capacity,
            event.location
        ))
    
        self.connection.commit()

    #========================= Edit Values to Database =========================
    def update_event(self, event):
        self.cursor.execute("""
            UPDATE events
            SET
                name = ?,
                category = ?,
                date = ?,
                time = ?,
                description = ?,
                capacity = ?,
                location = ?
            WHERE id = ?
        """, (
            event.name,
            event.category,
            event.date,
            event.time,
            event.description,
            event.capacity,
            event.location,
            event.id
        ))
    
        self.connection.commit()

    #========================= Close Connection =========================


    def close(self):

        self.connection.close()