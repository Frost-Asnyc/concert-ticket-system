import pytest

from models.booking import (
    create_booking,
    get_booking_by_id,
    list_bookings,
    cancel_booking,
)
from models.event import create_event, get_event_by_id


@pytest.fixture
def booking_file(tmp_path):
    return str(tmp_path / "bookings.json")


def test_booking_create_list_and_cancel(booking_file):
    ok, booking = create_booking("U001", "E001", 2, 50, booking_file)
    assert ok is True
    assert booking.booking_id == "B001"
    assert booking.status == "confirmed"
    assert booking.total_price == 100

    bookings = list_bookings(booking_file)
    assert len(bookings) == 1

    found = get_booking_by_id("B001", booking_file)
    assert found is not None
    assert found.booking_id == "B001"

    ok, cancelled = cancel_booking("B001", booking_file)
    assert ok is True
    assert cancelled.status == "cancelled"


def test_booking_reserves_and_restores_event_seats(booking_file, tmp_path):
    event_file = str(tmp_path / "events.json")
    create_event("Concert", "2026-12-01", "Hall", 5, event_file)

    ok, booking = create_booking("U001", "E001", 3, 20, booking_file, event_file)
    assert ok is True
    assert booking.quantity == 3
    assert get_event_by_id("E001", event_file).available_seats == 2

    ok, cancelled = cancel_booking("B001", booking_file, event_file)
    assert ok is True
    assert cancelled.status == "cancelled"
    assert get_event_by_id("E001", event_file).available_seats == 5


def test_booking_rejects_more_tickets_than_available(booking_file, tmp_path):
    event_file = str(tmp_path / "events.json")
    create_event("Concert", "2026-12-01", "Hall", 1, event_file)

    ok, message = create_booking("U001", "E001", 2, 20, booking_file, event_file)
    assert ok is False
    assert message == "not enough available seats"

