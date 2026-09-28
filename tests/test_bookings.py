from datetime import datetime

import pytest

from bookings import cancel_booking, create_booking
from checks import has_time_conflict

ROOM = {"id": 1, "name": "Конференц-зал Сириус", "capacity": 40,
        "has_projector": True, "opens": "08:30", "closes": "21:00"}


def make_request(start, end, participants=10):
    return {"room_id": 1, "title": "Тест", "date": "2026-10-15",
            "start": start, "end": end, "participants": participants,
            "needs_projector": False}


def test_intervals_overlap():
    assert has_time_conflict(
        datetime(2026, 10, 15, 11, 30), datetime(2026, 10, 15, 13, 0),
        datetime(2026, 10, 15, 10, 0), datetime(2026, 10, 15, 12, 30),
    )


def test_back_to_back_is_not_conflict():
    assert not has_time_conflict(
        datetime(2026, 10, 15, 12, 30), datetime(2026, 10, 15, 14, 0),
        datetime(2026, 10, 15, 10, 0), datetime(2026, 10, 15, 12, 30),
    )


def test_create_booking():
    bookings = []
    booking = create_booking(bookings, ROOM, make_request("10:00", "12:00"))
    assert booking["id"] == 1
    assert len(bookings) == 1


def test_double_booking_forbidden():
    bookings = []
    create_booking(bookings, ROOM, make_request("10:00", "12:00"))
    with pytest.raises(ValueError, match="занято"):
        create_booking(bookings, ROOM, make_request("11:00", "13:00"))


def test_too_many_participants():
    with pytest.raises(ValueError, match="не хватает мест"):
        create_booking([], ROOM, make_request("10:00", "12:00", 45))


def test_cancel_booking():
    bookings = []
    booking = create_booking(bookings, ROOM, make_request("10:00", "12:00"))
    cancel_booking(bookings, booking["id"])
    assert bookings == []
