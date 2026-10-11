from datetime import date

from calc import (OK, REPLACE, SHORTAGE, SURPLUS, get_age_years,
                  get_result, get_shortage_cost, needs_replacement)


def test_shortage_cost():
    assert get_shortage_cost(12, 10, 4500.50) == 9001.0


def test_no_shortage_cost_when_surplus():
    assert get_shortage_cost(5, 7, 100.0) == 0.0


def test_age_years():
    assert get_age_years(date(2018, 5, 20), date(2026, 10, 12)) == 8.4


def test_old_or_broken_item_needs_replacement():
    assert needs_replacement(8.4, 5, True)
    assert needs_replacement(1.0, 5, False)
    assert not needs_replacement(3.1, 5, True)


def test_result_statuses():
    assert get_result(2, False) == SHORTAGE
    assert get_result(-2, False) == SURPLUS
    assert get_result(0, True) == REPLACE
    assert get_result(0, False) == OK
