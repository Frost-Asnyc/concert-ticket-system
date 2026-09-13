import pytest

from models.booking import (
    create_booking,
    get_booking_by_id,
    list_bookings,
    cancel_booking,
)


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

