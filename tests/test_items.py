from datetime import date

import pytest

from models import Item, Room
from models.items import (add_item, find_items, get_room_items, get_total,
                          move_item, write_off_item)

CHECK_DATE = date(2026, 10, 12)


def make_rooms():
    return [
        Room(1, "Кабинет 204", 2, "Иванова А. С."),
        Room(2, "Переговорная 305", 3, "Петров Д. И."),
    ]


def make_items(rooms):
    items = []
    add_item(items, "1001", "Кресло офисное", rooms[0], 12, 4500.50,
             date(2022, 3, 15), 7)
    add_item(items, "1005", "Проектор", rooms[1], 1, 54000.00,
             date(2019, 2, 11), 5)
    return items


def test_item_creation():
    room = make_rooms()[0]
    item = Item(1, "1001", "Кресло офисное", room, 12, 4500.50,
                date(2022, 3, 15), 7)
    assert item.number == "1001"
    assert item.room is room
    assert item.room.name == "Кабинет 204"
    assert not item.is_written_off


def test_total_cost():
    item = make_items(make_rooms())[0]
    assert item.total_cost == 54006.0


def test_age_and_replacement():
    rooms = make_rooms()
    chair, projector = make_items(rooms)
    assert projector.get_age_years(CHECK_DATE) == 7.7
    assert projector.needs_replacement(CHECK_DATE, True)
    assert not chair.needs_replacement(CHECK_DATE, True)
    assert chair.needs_replacement(CHECK_DATE, False)


def test_move_to():
    rooms = make_rooms()
    item = make_items(rooms)[0]
    item.move_to(rooms[1])
    assert item.room is rooms[1]
    with pytest.raises(ValueError):
        item.move_to(rooms[1])


def test_write_off_keeps_item():
    rooms = make_rooms()
    items = make_items(rooms)
    write_off_item(items, "1001")
    assert len(items) == 2
    assert items[0].is_written_off
    assert list(get_room_items(items, rooms[0])) == []
    with pytest.raises(ValueError):
        write_off_item(items, "1001")


def test_item_str():
    item = make_items(make_rooms())[0]
    assert str(item) == ("1001 Кресло офисное, Кабинет 204: "
                         "12 шт. по 4500.5 руб.")


def test_item_from_data_and_back():
    room = make_rooms()[0]
    data = {"id": 1, "number": "1001", "name": "Кресло офисное",
            "room_id": 1, "quantity": 12, "price": 4500.5,
            "purchase_date": "2022-03-15", "service_life": 7,
            "is_written_off": False}
    item = Item.from_data(data, room)
    assert item.purchase_date == date(2022, 3, 15)
    assert item.room is room
    assert item.to_data() == data


def test_find_items_by_name_and_number():
    items = make_items(make_rooms())
    assert find_items(items, "кресло") == [items[0]]
    assert find_items(items, "1005") == [items[1]]


def test_duplicate_number_forbidden():
    rooms = make_rooms()
    items = make_items(rooms)
    with pytest.raises(ValueError, match="уже занят"):
        add_item(items, "1001", "Стул", rooms[0], 4, 2300.00,
                 date(2020, 1, 10), 7)


def test_get_room_items():
    rooms = make_rooms()
    items = make_items(rooms)
    assert list(get_room_items(items, rooms[1])) == [items[1]]


def test_move_item():
    rooms = make_rooms()
    items = make_items(rooms)
    move_item(items, "1005", rooms[0])
    assert items[1].room is rooms[0]


def test_unknown_item():
    items = make_items(make_rooms())
    with pytest.raises(ValueError):
        write_off_item(items, "9999")


def test_get_total():
    assert get_total(make_items(make_rooms())) == (13, 108006.0)
