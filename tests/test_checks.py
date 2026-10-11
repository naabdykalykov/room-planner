from datetime import date

from models import Check, Room
from models.checks import create_check, find_check_by_id

ROOM = Room(2, "Переговорная 305", 3, "Петров Д. И.")


def test_check_creation():
    check = Check(1, ROOM, date(2026, 10, 5), "Петров Д. И.")
    assert check.id == 1
    assert check.room is ROOM
    assert check.room.name == "Переговорная 305"
    assert check.date == date(2026, 10, 5)


def test_check_str():
    check = Check(1, ROOM, date(2026, 10, 5), "Петров Д. И.")
    assert str(check) == ("Проверка 1: 05.10.2026, Переговорная 305, "
                          "проверяющий: Петров Д. И.")


def test_check_from_data_and_back():
    data = {"id": 1, "room_id": 2, "date": "2026-10-05",
            "inspector": "Петров Д. И."}
    check = Check.from_data(data, ROOM)
    assert check.room is ROOM
    assert check.to_data() == data


def test_create_check_gives_next_id():
    checks = []
    first = create_check(checks, ROOM, date(2026, 10, 5), "Петров Д. И.")
    second = create_check(checks, ROOM, date(2026, 10, 12), "Петров Д. И.")
    assert (first.id, second.id) == (1, 2)
    assert find_check_by_id(checks, 2) is second
    assert find_check_by_id(checks, 99) is None
