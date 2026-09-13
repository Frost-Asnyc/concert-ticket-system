import json
import os

from models.event import create_event, list_events, search_events
from models.ticket import create_ticket, cancel_ticket, get_tickets_by_user
from models.booking import create_booking


EVENTS_FILE = "data/event.json"
TICKETS_FILE = "data/ticket.json"
BOOKINGS_FILE = "data/booking.json"


def print_menu():
    print("================================")
    print("      EVENT TICKET SYSTEM")
    print("================================")
    print("1. Register")
    print("2. Login")
    print("3. View Events")
    print("4. Search Events")
    print("5. Book Ticket")
    print("6. My Tickets")
    print("7. Cancel Ticket")
    print("8. Exit")


def register_user():
    print("Registration is ready to be added later.")


def login_user():
    print("Login is ready to be added later.")


def view_events():
    events = list_events(EVENTS_FILE)
    if not events:
        print("No events found.")
        return

    for event in events:
        print(f"{event.event_id} | {event.name} | {event.date} | {event.venue} | seats={event.available_seats}")


def search_events_cli():
    keyword = input("Search by event name, venue or date: ").strip()
    events = search_events(keyword, EVENTS_FILE)
    if not events:
        print("No matching events found.")
        return

    for event in events:
        print(f"{event.event_id} | {event.name} | {event.date} | {event.venue} | seats={event.available_seats}")


def book_ticket():
    event_id = input("Event ID: ").strip()
    user_id = input("User ID: ").strip()
    quantity = input("Number of tickets: ").strip()
    price = input("Price per ticket: ").strip()

    ok, booking = create_booking(user_id, event_id, quantity, price, BOOKINGS_FILE)
    if ok:
        ok_ticket, ticket = create_ticket(user_id, event_id, TICKETS_FILE)
        if ok_ticket:
            print(f"Booked. Booking: {booking.booking_id}. Ticket: {ticket.ticket_id}")
        else:
            print(ticket)
    else:
        print(booking)


def my_tickets():
    user_id = input("User ID: ").strip()
    tickets = get_tickets_by_user(user_id, TICKETS_FILE)
    if not tickets:
        print("No tickets found for that user.")
        return

    for ticket in tickets:
        print(f"{ticket.ticket_id} | {ticket.event_id} | {ticket.status}")


def cancel_ticket_cli():
    ticket_id = input("Ticket ID: ").strip()
    ok, result = cancel_ticket(ticket_id, TICKETS_FILE)
    if ok:
        print(f"Ticket {ticket_id} cancelled.")
    else:
        print(result)


def add_event_cli():
    name = input("Event name: ").strip()
    date = input("Event date: ").strip()
    venue = input("Venue: ").strip()
    seats = input("Available seats: ").strip()

    ok, result = create_event(name, date, venue, seats, EVENTS_FILE)
    if ok:
        print(f"Event created: {result.event_id}")
    else:
        print(result)


def run_cli():
    while True:
        print_menu()
        choice = input("Pick your hangover spot: ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            view_events()
        elif choice == "4":
            search_events_cli()
        elif choice == "5":
            book_ticket()
        elif choice == "6":
            my_tickets()
        elif choice == "7":
            cancel_ticket_cli()
        elif choice == "8":
            print("(Touch more grass next time you lazy couch grape)!")
            break
        elif choice == "9":
            add_event_cli()
        else:
            print("Choose a valid number from the menu.")


if __name__ == "__main__":
    run_cli()

