from collections.abc import Iterable, Iterator
from datetime import date

from .common import get_next_id
from .rooms import Room


class Item:
    """Предмет, который числится за помещением."""

    def __init__(self, item_id: int, number: str, name: str, room: Room,
                 quantity: int, price: float, purchase_date: date,
                 service_life: int) -> None:
        """Создает предмет, room - объект помещения, где он стоит."""
        self.id = item_id
        self.number = number
        self.name = name
        self.room = room
        self.quantity = quantity
        self.price = price
        self.purchase_date = purchase_date
        self.service_life = service_life
        self.is_written_off = False

    @classmethod
    def from_data(cls, data: dict, room: Room) -> "Item":
        """Создает предмет из словаря JSON и найденного помещения."""
        item = cls(data["id"], data["number"], data["name"], room,
                   data["quantity"], data["price"],
                   date.fromisoformat(data["purchase_date"]),
                   data["service_life"])
        item.is_written_off = data.get("is_written_off", False)
        return item

    def to_data(self) -> dict:
        """Превращает предмет в словарь для JSON, помещение - как id."""
        return {
            "id": self.id,
            "number": self.number,
            "name": self.name,
            "room_id": self.room.id,
            "quantity": self.quantity,
            "price": self.price,
            "purchase_date": self.purchase_date.isoformat(),
            "service_life": self.service_life,
            "is_written_off": self.is_written_off,
        }

    @staticmethod
    def is_valid_quantity(quantity: int) -> bool:
        """Проверяет, что количество больше нуля."""
        return quantity > 0

    @property
    def total_cost(self) -> float:
        """Стоимость всех штук этого предмета."""
        return self.quantity * self.price

    def get_age_years(self, on_date: date) -> float:
        """Возраст предмета в годах на указанную дату."""
        return round((on_date - self.purchase_date).days / 365, 1)

    def needs_replacement(self, on_date: date, is_working: bool) -> bool:
        """Нужна ли замена: предмет сломан или старше срока службы."""
        age_years = self.get_age_years(on_date)
        return not is_working or age_years > self.service_life

    def move_to(self, room: Room) -> None:
        """Переносит предмет в другое помещение."""
        if self.room.id == room.id:
            raise ValueError("предмет уже находится в этом помещении")
        self.room = room

    def write_off(self) -> None:
        """Списывает предмет: он остается в списке с пометкой."""
        if self.is_written_off:
            raise ValueError("предмет уже списан")
        self.is_written_off = True

    def __str__(self) -> str:
        """Строка, которую печатает print(item)."""
        text = (f"{self.number} {self.name}, {self.room.name}: "
                f"{self.quantity} шт. по {self.price} руб.")
        if self.is_written_off:
            text += " (списан)"
        return text


def get_room_items(items: list[Item], room: Room) -> Iterator[Item]:
    """Выдает по одному несписанные предметы помещения."""
    for item in items:
        if item.room.id == room.id and not item.is_written_off:
            yield item


def get_total(items: Iterable[Item]) -> tuple[int, float]:
    """Считает, сколько всего штук и на какую сумму."""
    count = 0
    cost = 0.0
    for item in items:
        count += item.quantity
        cost += item.total_cost
    return count, cost


def find_item_by_id(items: list[Item], item_id: int) -> Item | None:
    """Ищет предмет по номеру записи, если нет - None."""
    for item in items:
        if item.id == item_id:
            return item
    return None


def find_item_by_number(items: list[Item], number: str) -> Item | None:
    """Ищет предмет по инвентарному номеру, если нет - None."""
    for item in items:
        if item.number == number:
            return item
    return None


def find_items(items: list[Item], query: str) -> list[Item]:
    """Ищет предметы по части названия или инвентарного номера."""
    query = query.strip().lower()
    return [
        item for item in items
        if query in item.name.lower() or query in item.number.lower()
    ]


def sort_items(items: Iterable[Item]) -> list[Item]:
    """Сортирует предметы по названию."""
    return sorted(items, key=lambda item: item.name)


def add_item(items: list[Item], number: str, name: str, room: Room,
             quantity: int, price: float, purchase_date: date,
             service_life: int) -> Item:
    """Создает предмет и добавляет его в список."""
    if find_item_by_number(items, number) is not None:
        raise ValueError(f"инвентарный номер {number} уже занят")
    if not Item.is_valid_quantity(quantity):
        raise ValueError("количество должно быть больше нуля")
    item = Item(get_next_id(items), number, name, room, quantity, price,
                purchase_date, service_life)
    items.append(item)
    return item


def move_item(items: list[Item], number: str, room: Room) -> Item:
    """Находит предмет по номеру и переносит его в помещение."""
    item = find_item_by_number(items, number)
    if item is None:
        raise ValueError(f"предмет с номером {number} не найден")
    item.move_to(room)
    return item


def write_off_item(items: list[Item], number: str) -> Item:
    """Находит предмет по номеру и списывает его."""
    item = find_item_by_number(items, number)
    if item is None:
        raise ValueError(f"предмет с номером {number} не найден")
    item.write_off()
    return item
