from collections.abc import Iterable, Iterator
from datetime import date

from utils import get_next_id


def get_room_items(items: list[dict], room_id: int) -> Iterator[dict]:
    """Выдает по одному предметы, которые стоят в помещении."""
    for item in items:
        if item["room_id"] == room_id:
            yield item


def get_total(items: Iterable[dict]) -> tuple[int, float]:
    """Считает, сколько всего штук и на какую сумму."""
    count = 0
    cost = 0.0
    for item in items:
        count += item["quantity"]
        cost += item["price"] * item["quantity"]
    return count, cost


def find_item_by_number(items: list[dict], number: str) -> dict | None:
    """Ищет предмет по инвентарному номеру, если нет - None."""
    for item in items:
        if item["number"] == number:
            return item
    return None


def find_items(items: list[dict], query: str) -> list[dict]:
    """Ищет предметы по части названия или инвентарного номера."""
    query = query.strip().lower()
    return [
        item for item in items
        if query in item["name"].lower() or query in item["number"].lower()
    ]


def sort_items(items: Iterable[dict], key: str = "name") -> list[dict]:
    """Сортирует предметы по названию или другому полю."""
    return sorted(items, key=lambda item: item[key])


def add_item(items: list[dict], number: str, name: str, room_id: int,
             quantity: int, price: float, purchase_date: date,
             service_life: int) -> dict:
    """Добавляет предмет, инвентарный номер не должен повторяться."""
    if find_item_by_number(items, number) is not None:
        raise ValueError(f"инвентарный номер {number} уже занят")
    if quantity <= 0:
        raise ValueError("количество должно быть больше нуля")
    item = {
        "id": get_next_id(items),
        "number": number,
        "name": name,
        "room_id": room_id,
        "quantity": quantity,
        "price": price,
        "purchase_date": purchase_date.isoformat(),
        "service_life": service_life,
    }
    items.append(item)
    return item


def move_item(items: list[dict], number: str, room_id: int) -> dict:
    """Переносит предмет в другое помещение."""
    item = find_item_by_number(items, number)
    if item is None:
        raise ValueError(f"предмет с номером {number} не найден")
    if item["room_id"] == room_id:
        raise ValueError("предмет уже находится в этом помещении")
    item["room_id"] = room_id
    return item


def write_off_item(items: list[dict], number: str) -> dict:
    """Списывает предмет: удаляет его из учета."""
    for index, item in enumerate(items):
        if item["number"] == number:
            return items.pop(index)
    raise ValueError(f"предмет с номером {number} не найден")
