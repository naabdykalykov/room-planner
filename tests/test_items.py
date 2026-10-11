from datetime import date

import pytest

from items import (add_item, find_items, get_room_items, get_total,
                   move_item, write_off_item)


def make_items():
    items = []
    add_item(items, "1001", "Кресло офисное", 1, 12, 4500.50,
             date(2022, 3, 15), 7)
    add_item(items, "1005", "Проектор", 2, 1, 54000.00,
             date(2019, 2, 11), 5)
    return items


def test_find_items_by_name_and_number():
    items = make_items()
    assert find_items(items, "кресло") == [items[0]]
    assert find_items(items, "1005") == [items[1]]


def test_duplicate_number_forbidden():
    items = make_items()
    with pytest.raises(ValueError, match="уже занят"):
        add_item(items, "1001", "Стул", 1, 4, 2300.00, date(2020, 1, 10), 7)


def test_get_room_items():
    items = make_items()
    assert list(get_room_items(items, 2)) == [items[1]]


def test_move_item():
    items = make_items()
    move_item(items, "1005", 1)
    assert items[1]["room_id"] == 1


def test_write_off_item():
    items = make_items()
    write_off_item(items, "1001")
    assert len(items) == 1


def test_write_off_unknown_item():
    with pytest.raises(ValueError):
        write_off_item(make_items(), "9999")


def test_get_total():
    assert get_total(make_items()) == (13, 108006.0)
