import tempfile

from models.event import (
    create_event,
    get_event_by_id,
    list_events,
    search_events,
    update_event_seats,
)


def test_event_create_list_search_and_persistence(tmp_path):
    event_file = tmp_path / "events.json"

    ok, event = create_event(
        "Winter Concert",
        "2026-09-13",
        "Hall A",
        50,
        str(event_file),
    )

    assert ok is True
    assert event.event_id == "E001"
    assert event.available_seats == 50

    events = list_events(str(event_file))
    assert len(events) == 1

    found = get_event_by_id("E001", str(event_file))
    assert found is not None
    assert found.name == "Winter Concert"

    matches = search_events("concert", str(event_file))
    assert len(matches) == 1

    ok, updated = update_event_seats("E001", -5, str(event_file))
    assert ok is True
    assert updated.available_seats == 45

