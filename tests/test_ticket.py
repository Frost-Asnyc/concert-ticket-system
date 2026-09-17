import pytest

from models.ticket import (
    create_ticket,
    create_tickets,
    get_tickets_by_user,
    get_ticket_by_id,
    cancel_ticket,
)


@pytest.fixture
def test_file(tmp_path):
    # gives each test its own throwaway json file so they don't mess with
    # the real data or with each other
    return str(tmp_path / "tickets.json")


def test_create_ticket(test_file):
    ok, ticket = create_ticket("U001", "E001", test_file)
    assert ok is True
    assert ticket.ticket_id == "T001"
    assert ticket.status == "active"


def test_create_ticket_missing_ids(test_file):
    ok, msg = create_ticket("", "E001", test_file)
    assert ok is False


def test_ticket_ids_go_up(test_file):
    _, t1 = create_ticket("U001", "E001", test_file)
    _, t2 = create_ticket("U001", "E001", test_file)
    assert t1.ticket_id == "T001"
    assert t2.ticket_id == "T002"


def test_get_tickets_by_user(test_file):
    create_ticket("U001", "E001", test_file)
    create_ticket("U001", "E002", test_file)
    create_ticket("U002", "E001", test_file)

    tickets = get_tickets_by_user("U001", test_file)
    assert len(tickets) == 2


def test_get_ticket_by_id(test_file):
    _, created = create_ticket("U001", "E001", test_file)
    found = get_ticket_by_id(created.ticket_id, test_file)
    assert found.ticket_id == created.ticket_id


def test_get_ticket_by_id_missing(test_file):
    assert get_ticket_by_id("T999", test_file) is None


def test_cancel_ticket(test_file):
    _, created = create_ticket("U001", "E001", test_file)
    ok, cancelled = cancel_ticket(created.ticket_id, test_file)
    assert ok is True
    assert cancelled.status == "cancelled"


def test_cancel_twice_fails(test_file):
    _, created = create_ticket("U001", "E001", test_file)
    cancel_ticket(created.ticket_id, test_file)
    ok, msg = cancel_ticket(created.ticket_id, test_file)
    assert ok is False


def test_cancel_ticket_not_found(test_file):
    ok, msg = cancel_ticket("T999", test_file)
    assert ok is False


def test_create_tickets_creates_requested_quantity(test_file):
    ok, tickets = create_tickets("U001", "E001", 5, test_file)
    assert ok is True
    assert len(tickets) == 5
    assert len(get_tickets_by_user("U001", test_file)) == 5


def test_cancel_ticket_requires_owner(test_file):
    _, created = create_ticket("U001", "E001", test_file)
    ok, message = cancel_ticket(created.ticket_id, test_file, owner_user_id="U002")
    assert ok is False
    assert message == "you can only cancel your own tickets"