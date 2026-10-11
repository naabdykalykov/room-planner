from datetime import date

from calc import (SHORTAGE, SURPLUS, get_age_years, get_difference,
                  get_result, get_shortage_cost, needs_replacement)
from items import get_room_items, get_total
from utils import get_next_id


def create_check(checks: list[dict], room_id: int, day: date,
                 inspector: str) -> dict:
    """Создает запись о проверке помещения."""
    check = {
        "id": get_next_id(checks),
        "room_id": room_id,
        "date": day.isoformat(),
        "inspector": inspector,
    }
    checks.append(check)
    return check


def add_result(results: list[dict], check: dict, item: dict,
               actual: int, is_working: bool) -> dict:
    """Считает результат проверки предмета функциями из calc."""
    check_date = date.fromisoformat(check["date"])
    purchase_date = date.fromisoformat(item["purchase_date"])
    age_years = get_age_years(purchase_date, check_date)
    replace = needs_replacement(age_years, item["service_life"], is_working)
    difference = get_difference(item["quantity"], actual)
    result = {
        "id": get_next_id(results),
        "check_id": check["id"],
        "number": item["number"],
        "name": item["name"],
        "expected": item["quantity"],
        "actual": actual,
        "is_working": is_working,
        "needs_replacement": replace,
        "status": get_result(difference, replace),
        "shortage_cost": get_shortage_cost(item["quantity"], actual,
                                           item["price"]),
    }
    results.append(result)
    return result


def get_check_results(results: list[dict], check_id: int) -> list[dict]:
    """Возвращает результаты одной проверки."""
    return [result for result in results if result["check_id"] == check_id]


def get_summary(results: list[dict]) -> dict:
    """Считает итоги: недостачи, излишки, замены и сумму недостачи."""
    summary = {"checked": len(results), "shortages": 0, "surpluses": 0,
               "replacements": 0, "shortage_cost": 0.0}
    for result in results:
        if result["status"] == SHORTAGE:
            summary["shortages"] += 1
        elif result["status"] == SURPLUS:
            summary["surpluses"] += 1
        if result["needs_replacement"]:
            summary["replacements"] += 1
        summary["shortage_cost"] += result["shortage_cost"]
    summary["shortage_cost"] = round(summary["shortage_cost"], 2)
    return summary


def get_statistics(rooms: list[dict], items: list[dict],
                   checks: list[dict], results: list[dict]) -> dict:
    """Считает статистику по имуществу и проверкам."""
    units, cost = get_total(items)
    by_room = {}
    for room in rooms:
        by_room[room["name"]] = get_total(get_room_items(items, room["id"]))
    checked_rooms = {check["room_id"] for check in checks}
    return {
        "units": units,
        "cost": cost,
        "by_room": by_room,
        "checked_rooms": len(checked_rooms),
        "shortage_cost": get_summary(results)["shortage_cost"],
    }
