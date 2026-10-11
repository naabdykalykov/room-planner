from datetime import date

from models import Check, Item, Result, Room
from models.results import (add_result, get_check_results, get_statistics,
                            get_summary)

ROOM = Room(2, "Переговорная 305", 3, "Петров Д. И.")
CHAIR = Item(7, "1007", "Стул", ROOM, 10, 2300.0, date(2020, 1, 10), 7)
PROJECTOR = Item(5, "1005", "Проектор", ROOM, 1, 54000.0,
                 date(2019, 2, 11), 5)


def make_check():
    return Check(1, ROOM, date(2026, 10, 5), "Петров Д. И.")


def test_result_links_objects():
    check = make_check()
    result = add_result([], check, CHAIR, 9, True)
    assert result.check is check
    assert result.item is CHAIR
    assert result.check.room.name == "Переговорная 305"
    assert result.expected == 10


def test_shortage():
    result = add_result([], make_check(), CHAIR, 9, True)
    assert result.difference == 1
    assert result.status == Result.SHORTAGE
    assert result.shortage_cost == 2300.0


def test_surplus_has_no_shortage_cost():
    result = add_result([], make_check(), CHAIR, 12, True)
    assert result.difference == -2
    assert result.status == Result.SURPLUS
    assert result.shortage_cost == 0.0


def test_old_item_needs_replacement():
    result = add_result([], make_check(), PROJECTOR, 1, True)
    assert result.needs_replacement
    assert result.status == Result.REPLACE


def test_working_item_in_place():
    result = add_result([], make_check(), CHAIR, 10, True)
    assert result.status == Result.OK


def test_result_str():
    result = add_result([], make_check(), CHAIR, 9, True)
    assert str(result) == ("1007 Стул: по учету 10, фактически 9, "
                           "недостача")


def test_result_from_data_and_back():
    check = make_check()
    data = {"id": 3, "check_id": 1, "item_id": 7, "expected": 10,
            "actual": 9, "is_working": True}
    result = Result.from_data(data, check, CHAIR)
    assert result.item is CHAIR
    assert result.to_data() == data


def test_summary():
    results = []
    check = make_check()
    add_result(results, check, CHAIR, 9, True)
    add_result(results, check, PROJECTOR, 1, True)
    summary = get_summary(get_check_results(results, check))
    assert summary["checked"] == 2
    assert summary["shortages"] == 1
    assert summary["replacements"] == 1
    assert summary["shortage_cost"] == 2300.0


def test_statistics():
    check = make_check()
    results = []
    add_result(results, check, CHAIR, 9, True)
    stats = get_statistics([ROOM], [CHAIR, PROJECTOR], [check], results)
    assert stats["units"] == 11
    assert stats["cost"] == 77000.0
    assert stats["checked_rooms"] == 1
    assert stats["shortage_cost"] == 2300.0
