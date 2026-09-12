import json
import os

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

    with open(filepath, "r") as f:
        data = json.load(f)

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
    return "T" + str(len(tickets) + 1).zfill(3)


def create_ticket(user_id, event_id, filepath=TICKETS_FILE):
    if not not_empty(user_id) or not not_empty(event_id):
        return False, "user_id and event_id are required"

    tickets = load_tickets(filepath)
    new_id = generate_ticket_id(tickets)
    ticket = Ticket(new_id, user_id, event_id, "active")

    tickets.append(ticket)
    save_tickets(tickets, filepath)

    return True, ticket


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


def cancel_ticket(ticket_id, filepath=TICKETS_FILE):
    tickets = load_tickets(filepath)

    for t in tickets:
        if t.ticket_id == ticket_id:
            if t.status == "cancelled":
                return False, "ticket already cancelled"
            t.status = "cancelled"
            save_tickets(tickets, filepath)
            return True, t

    return False, "ticket not found"


# quick manual test when running this file directly
if __name__ == "__main__":
    ok, ticket = create_ticket("U001", "E001")
    print(ok, ticket)

    print(get_tickets_by_user("U001"))

    ok, result = cancel_ticket(ticket.ticket_id)
    print(ok, result)