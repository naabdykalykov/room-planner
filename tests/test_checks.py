from datetime import date

from calc import REPLACE, SHORTAGE
from checks import add_result, create_check, get_summary

CHAIR = {"id": 1, "number": "1007", "name": "Стул", "room_id": 2,
         "quantity": 10, "price": 2300.0, "purchase_date": "2020-01-10",
         "service_life": 7}
PROJECTOR = {"id": 2, "number": "1005", "name": "Проектор", "room_id": 2,
             "quantity": 1, "price": 54000.0, "purchase_date": "2019-02-11",
             "service_life": 5}


def make_check():
    return create_check([], 2, date(2026, 10, 5), "Петров Д. И.")


def test_shortage_result():
    result = add_result([], make_check(), CHAIR, 9, True)
    assert result["status"] == SHORTAGE
    assert result["shortage_cost"] == 2300.0


def test_old_item_result():
    result = add_result([], make_check(), PROJECTOR, 1, True)
    assert result["status"] == REPLACE


def test_summary():
    results = []
    check = make_check()
    add_result(results, check, CHAIR, 9, True)
    add_result(results, check, PROJECTOR, 1, True)
    summary = get_summary(results)
    assert summary["shortages"] == 1
    assert summary["replacements"] == 1
    assert summary["shortage_cost"] == 2300.0
