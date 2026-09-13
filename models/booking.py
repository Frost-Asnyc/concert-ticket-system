import json
import os


BOOKINGS_FILE = "data/booking.json"


class Booking:
    def __init__(self, booking_id, user_id, event_id, quantity, price_per_ticket, status="confirmed"):
        self.booking_id = booking_id
        self.user_id = user_id
        self.event_id = event_id
        self.quantity = quantity
        self.price_per_ticket = price_per_ticket
        self.total_price = quantity * price_per_ticket
        self.status = status

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "user_id": self.user_id,
            "event_id": self.event_id,
            "quantity": self.quantity,
            "price_per_ticket": self.price_per_ticket,
            "total_price": self.total_price,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data):
        booking = Booking(
            data["booking_id"],
            data["user_id"],
            data["event_id"],
            data["quantity"],
            data["price_per_ticket"],
            data.get("status", "confirmed"),
        )
        booking.total_price = data.get("total_price", booking.quantity * booking.price_per_ticket)
        return booking

    def __str__(self):
        return f"{self.booking_id} - {self.event_id} for {self.user_id} ({self.status})"


def load_bookings(filepath=BOOKINGS_FILE):
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(data, list):
        return []

    return [Booking.from_dict(item) for item in data]


def save_bookings(bookings, filepath=BOOKINGS_FILE):
    folder = os.path.dirname(filepath)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    with open(filepath, "w") as f:
        json.dump([booking.to_dict() for booking in bookings], f, indent=4)


def generate_booking_id(bookings):
    if not bookings:
        return "B001"
    number = int(bookings[-1].booking_id.replace("B", "")) + 1
    return f"B{number:03d}"


def create_booking(user_id, event_id, quantity, price_per_ticket, filepath=BOOKINGS_FILE):
    if not user_id or not event_id:
        return False, "user_id and event_id are required"

    try:
        quantity = int(quantity)
        price_per_ticket = int(price_per_ticket)
    except (TypeError, ValueError):
        return False, "quantity and price_per_ticket must be integers"

    if quantity <= 0:
        return False, "quantity must be positive"

    bookings = load_bookings(filepath)
    booking = Booking(
        generate_booking_id(bookings),
        user_id,
        event_id,
        quantity,
        price_per_ticket,
        "confirmed",
    )
    bookings.append(booking)
    save_bookings(bookings, filepath)
    return True, booking


def list_bookings(filepath=BOOKINGS_FILE):
    return load_bookings(filepath)


def get_booking_by_id(booking_id, filepath=BOOKINGS_FILE):
    for booking in load_bookings(filepath):
        if booking.booking_id == booking_id:
            return booking
    return None


def cancel_booking(booking_id, filepath=BOOKINGS_FILE):
    bookings = load_bookings(filepath)
    for booking in bookings:
        if booking.booking_id == booking_id:
            if booking.status == "cancelled":
                return False, "booking already cancelled"
            booking.status = "cancelled"
            save_bookings(bookings, filepath)
            return True, booking
    return False, "booking not found"

