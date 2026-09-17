import json
import os

from models.event import update_event_seats
from utils.validators import not_empty

TICKETS_FILE = "data/ticket.json"


class Ticket:
    def __init__(self, ticket_id, user_id, event_id, status="active"):
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.event_id = event_id
        self.status = status

    def to_dict(self):
        return {
            "ticket_id": self.ticket_id,
            "user_id": self.user_id,
            "event_id": self.event_id,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        return Ticket(data["ticket_id"], data["user_id"], data["event_id"], data["status"])

    def __str__(self):
        return f"{self.ticket_id} - {self.event_id} ({self.status})"


def load_tickets(filepath=TICKETS_FILE):
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(data, list):
        return []

    tickets = []
    for item in data:
        tickets.append(Ticket.from_dict(item))
    return tickets


def save_tickets(tickets, filepath=TICKETS_FILE):
    # make sure the data folder exists before writing to it
    folder = os.path.dirname(filepath)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    data = [t.to_dict() for t in tickets]
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


def generate_ticket_id(tickets):
    if not tickets:
        return "T001"
    number = max(int(ticket.ticket_id.replace("T", "")) for ticket in tickets) + 1
    return f"T{number:03d}"


def create_ticket(user_id, event_id, filepath=TICKETS_FILE):
    tickets = create_tickets(user_id, event_id, 1, filepath)
    if not tickets[0]:
        return tickets
    return True, tickets[1][0]


def create_tickets(user_id, event_id, quantity, filepath=TICKETS_FILE):
    if not not_empty(user_id) or not not_empty(event_id):
        return False, "user_id and event_id are required"

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return False, "quantity must be an integer"
    if quantity <= 0:
        return False, "quantity must be positive"

    tickets = load_tickets(filepath)
    created = []
    next_number = max(
        (int(ticket.ticket_id.replace("T", "")) for ticket in tickets),
        default=0,
    ) + 1
    for offset in range(quantity):
        created.append(Ticket(f"T{next_number + offset:03d}", user_id, event_id, "active"))

    tickets.extend(created)
    save_tickets(tickets, filepath)

    return True, created


def get_tickets_by_user(user_id, filepath=TICKETS_FILE):
    tickets = load_tickets(filepath)
    result = []
    for t in tickets:
        if t.user_id == user_id:
            result.append(t)
    return result


def get_ticket_by_id(ticket_id, filepath=TICKETS_FILE):
    tickets = load_tickets(filepath)
    for t in tickets:
        if t.ticket_id == ticket_id:
            return t
    return None


def cancel_ticket(ticket_id, filepath=TICKETS_FILE, event_filepath=None, owner_user_id=None):
    tickets = load_tickets(filepath)

    for t in tickets:
        if t.ticket_id == ticket_id:
            if owner_user_id is not None and t.user_id != owner_user_id:
                return False, "you can only cancel your own tickets"
            if t.status == "cancelled":
                return False, "ticket already cancelled"
            t.status = "cancelled"
            save_tickets(tickets, filepath)
            if event_filepath is not None:
                update_event_seats(t.event_id, 1, event_filepath)
            return True, t

    return False, "ticket not found"


# quick manual test when running this file directly
if __name__ == "__main__":
    ok, ticket = create_ticket("U001", "E001")
    print(ok, ticket)

    print(get_tickets_by_user("U001"))

    ok, result = cancel_ticket(ticket.ticket_id)
    print(ok, result)