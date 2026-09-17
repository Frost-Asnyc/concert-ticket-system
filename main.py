import json
import os

from models.event import create_event, list_events, search_events
from models.ticket import create_tickets, cancel_ticket, get_tickets_by_user
from models.booking import create_booking
from models.user import register_user as save_user, login_user as authenticate_user


EVENTS_FILE = "data/event.json"
TICKETS_FILE = "data/ticket.json"
BOOKINGS_FILE = "data/booking.json"
current_user = None


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
    print("9. Add Event")


def register_user():
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ")
    ok, result = save_user(username, email, password)
    if ok:
        print(f"Registered successfully. Your user ID is {result.user_id}.")
    else:
        print(result)


def login_user():
    global current_user
    username = input("Username: ").strip()
    password = input("Password: ")
    ok, result = authenticate_user(username, password)
    if ok:
        current_user = result
        print(f"Logged in as {result.username}.")
    else:
        print(result)


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
    if current_user is None:
        print("Please login first.")
        return
    event_id = input("Event ID: ").strip()
    quantity = input("Number of tickets: ").strip()
    price = input("Price per ticket: ").strip()

    ok, booking = create_booking(
        current_user.user_id,
        event_id,
        quantity,
        price,
        BOOKINGS_FILE,
        EVENTS_FILE,
    )
    if ok:
        ok_ticket, tickets = create_tickets(
            current_user.user_id, event_id, booking.quantity, TICKETS_FILE
        )
        if ok_ticket:
            print(
                f"Booked {len(tickets)} ticket(s). Booking: {booking.booking_id}. "
                f"Tickets: {', '.join(ticket.ticket_id for ticket in tickets)}"
            )
        else:
            print(tickets)
    else:
        print(booking)


def my_tickets():
    if current_user is None:
        print("Please login first.")
        return
    tickets = get_tickets_by_user(current_user.user_id, TICKETS_FILE)
    if not tickets:
        print("No tickets found for that user.")
        return

    for ticket in tickets:
        print(f"{ticket.ticket_id} | {ticket.event_id} | {ticket.status}")


def cancel_ticket_cli():
    if current_user is None:
        print("Please login first.")
        return
    ticket_id = input("Ticket ID: ").strip()
    ok, result = cancel_ticket(
        ticket_id,
        TICKETS_FILE,
        EVENTS_FILE,
        current_user.user_id,
    )
    if ok:
        print(f"Ticket {ticket_id} cancelled.")
    else:
        print(result)


def add_event_cli():
    if current_user is None or current_user.role != "admin":
        print("Admin access required.")
        return
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
        choice = input("Choose an option: ").strip()

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
            print("Thank you for using the Event Ticket System. Goodbye!")
            break
        elif choice == "9":
            add_event_cli()
        else:
            print("Choose a valid number from the menu.")


if __name__ == "__main__":
    run_cli()

