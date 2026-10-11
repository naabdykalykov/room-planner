from .checks import Check
from .common import get_next_id
from .items import Item, get_room_items, get_total
from .rooms import Room


class Result:
    """Результат проверки одного предмета."""

    OK = "в наличии"
    SHORTAGE = "недостача"
    SURPLUS = "излишек"
    REPLACE = "в наличии, требуется замена"

    def __init__(self, result_id: int, check: Check, item: Item,
                 expected: int, actual: int, is_working: bool) -> None:
        """Создает результат: check и item - объекты, а не номера."""
        self.id = result_id
        self.check = check
        self.item = item
        self.expected = expected
        self.actual = actual
        self.is_working = is_working

    @classmethod
    def from_data(cls, data: dict, check: Check, item: Item) -> "Result":
        """Создает результат из словаря JSON, проверки и предмета."""
        return cls(data["id"], check, item, data["expected"],
                   data["actual"], data["is_working"])

    def to_data(self) -> dict:
        """Превращает результат в словарь, связи - как номера."""
        return {
            "id": self.id,
            "check_id": self.check.id,
            "item_id": self.item.id,
            "expected": self.expected,
            "actual": self.actual,
            "is_working": self.is_working,
        }

    @property
    def difference(self) -> int:
        """Сколько штук не хватает: плюс - недостача, минус - излишек."""
        return self.expected - self.actual

    @property
    def shortage_cost(self) -> float:
        """Сумма недостачи в рублях, если недостачи нет - 0."""
        if self.difference <= 0:
            return 0.0
        return round(self.difference * self.item.price, 2)

    @property
    def needs_replacement(self) -> bool:
        """Нужно ли заменить предмет по итогам этой проверки."""
        return self.item.needs_replacement(self.check.date, self.is_working)

    @property
    def status(self) -> str:
        """Итог проверки предмета одним из четырех вариантов."""
        if self.difference > 0:
            return self.SHORTAGE
        elif self.difference < 0:
            return self.SURPLUS
        elif self.needs_replacement:
            return self.REPLACE
        else:
            return self.OK

    def __str__(self) -> str:
        """Строка, которую печатает print(result)."""
        return (f"{self.item.number} {self.item.name}: "
                f"по учету {self.expected}, "
                f"фактически {self.actual}, {self.status}")


def add_result(results: list[Result], check: Check, item: Item,
               actual: int, is_working: bool) -> Result:
    """Создает результат проверки предмета и добавляет его в список."""
    result = Result(get_next_id(results), check, item, item.quantity,
                    actual, is_working)
    results.append(result)
    return result


def get_check_results(results: list[Result], check: Check) -> list[Result]:
    """Возвращает результаты одной проверки."""
    return [result for result in results if result.check.id == check.id]


def get_summary(results: list[Result]) -> dict:
    """Считает итоги: недостачи, излишки, замены и сумму недостачи."""
    summary = {"checked": len(results), "shortages": 0, "surpluses": 0,
               "replacements": 0, "shortage_cost": 0.0}
    for result in results:
        if result.status == Result.SHORTAGE:
            summary["shortages"] += 1
        elif result.status == Result.SURPLUS:
            summary["surpluses"] += 1
        if result.needs_replacement:
            summary["replacements"] += 1
        summary["shortage_cost"] += result.shortage_cost
    summary["shortage_cost"] = round(summary["shortage_cost"], 2)
    return summary


def get_statistics(rooms: list[Room], items: list[Item],
                   checks: list[Check], results: list[Result]) -> dict:
    """Считает статистику по имуществу и проверкам."""
    active = [item for item in items if not item.is_written_off]
    units, cost = get_total(active)
    by_room = {}
    for room in rooms:
        by_room[room.name] = get_total(get_room_items(items, room))
    checked_rooms = {check.room.id for check in checks}
    return {
        "units": units,
        "cost": cost,
        "by_room": by_room,
        "written_off": len(items) - len(active),
        "checked_rooms": len(checked_rooms),
        "shortage_cost": get_summary(results)["shortage_cost"],
    }
