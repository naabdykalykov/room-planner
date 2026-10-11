from datetime import date

from .common import get_next_id
from .rooms import Room


class Check:
    """Проверка одного помещения в определенный день."""

    def __init__(self, check_id: int, room: Room, day: date,
                 inspector: str) -> None:
        """Создает проверку, room - объект проверяемого помещения."""
        self.id = check_id
        self.room = room
        self.date = day
        self.inspector = inspector

    @classmethod
    def from_data(cls, data: dict, room: Room) -> "Check":
        """Создает проверку из словаря JSON и найденного помещения."""
        return cls(data["id"], room, date.fromisoformat(data["date"]),
                   data["inspector"])

    def to_data(self) -> dict:
        """Превращает проверку в словарь для JSON, помещение - как id."""
        return {
            "id": self.id,
            "room_id": self.room.id,
            "date": self.date.isoformat(),
            "inspector": self.inspector,
        }

    def __str__(self) -> str:
        """Строка, которую печатает print(check)."""
        return (f"Проверка {self.id}: {self.date.strftime('%d.%m.%Y')}, "
                f"{self.room.name}, проверяющий: {self.inspector}")


def find_check_by_id(checks: list[Check], check_id: int) -> Check | None:
    """Ищет проверку по номеру, если ее нет - возвращает None."""
    for check in checks:
        if check.id == check_id:
            return check
    return None


def create_check(checks: list[Check], room: Room, day: date,
                 inspector: str) -> Check:
    """Создает проверку помещения и добавляет ее в список."""
    check = Check(get_next_id(checks), room, day, inspector)
    checks.append(check)
    return check
