import json
import os

from utils.validators import not_empty


EVENTS_FILE = "data/event.json"


class Event:
    def __init__(self, event_id, name, date, venue, available_seats):
        self.event_id = event_id
        self.name = name
        self.date = date
        self.venue = venue
        self.available_seats = available_seats

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "name": self.name,
            "date": self.date,
            "venue": self.venue,
            "available_seats": self.available_seats,
        }

    @staticmethod
    def from_dict(data):
        return Event(
            data["event_id"],
            data["name"],
            data["date"],
            data["venue"],
            data.get("available_seats", 0),
        )

    def __str__(self):
        return f"{self.event_id} - {self.name} ({self.date}) at {self.venue}"


def load_events(filepath=EVENTS_FILE):
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(data, list):
        return []

    return [Event.from_dict(item) for item in data]


def save_events(events, filepath=EVENTS_FILE):
    folder = os.path.dirname(filepath)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    with open(filepath, "w") as f:
        json.dump([event.to_dict() for event in events], f, indent=4)


def generate_event_id(events):
    if not events:
        return "E001"
    number = int(events[-1].event_id.replace("E", "")) + 1
    return f"E{number:03d}"


def create_event(name, date, venue, available_seats, filepath=EVENTS_FILE):
    if not not_empty(name) or not not_empty(date) or not not_empty(venue):
        return False, "name, date and venue are required"

    try:
        seats = int(available_seats)
    except (TypeError, ValueError):
        return False, "available_seats must be an integer"

    if seats < 0:
        return False, "available_seats cannot be negative"

    events = load_events(filepath)
    event = Event(generate_event_id(events), name.strip(), date.strip(), venue.strip(), seats)
    events.append(event)
    save_events(events, filepath)
    return True, event


def list_events(filepath=EVENTS_FILE):
    return load_events(filepath)


def get_event_by_id(event_id, filepath=EVENTS_FILE):
    for event in load_events(filepath):
        if event.event_id == event_id:
            return event
    return None


def search_events(keyword, filepath=EVENTS_FILE):
    keyword = (keyword or "").strip().lower()
    results = []
    for event in load_events(filepath):
        if keyword in event.name.lower() or keyword in event.venue.lower() or keyword in event.date.lower():
            results.append(event)
    return results


def update_event_seats(event_id, delta, filepath=EVENTS_FILE):
    try:
        delta = int(delta)
    except (TypeError, ValueError):
        return False, "seat change must be an integer"

    events = load_events(filepath)
    for event in events:
        if event.event_id == event_id:
            if event.available_seats + delta < 0:
                return False, "not enough available seats"
            event.available_seats += delta
            save_events(events, filepath)
            return True, event

    return False, "event not found"

