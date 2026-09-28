from collections.abc import Iterator
from datetime import time

from checks import check_capacity, check_equipment
from utils import get_next_id


def find_room_by_id(rooms: list[dict], room_id: int) -> dict | None:
    for room in rooms:
        if room["id"] == room_id:
            return room
    return None


def add_room(rooms: list[dict], name: str, capacity: int,
             has_projector: bool, opens: time, closes: time) -> dict:
    """Добавляет помещение в список и возвращает его."""
    if capacity <= 0:
        raise ValueError("вместимость должна быть больше нуля")
    if opens >= closes:
        raise ValueError("время открытия должно быть раньше закрытия")
    room = {
        "id": get_next_id(rooms),
        "name": name,
        "capacity": capacity,
        "has_projector": has_projector,
        "opens": opens.strftime("%H:%M"),
        "closes": closes.strftime("%H:%M"),
    }
    rooms.append(room)
    return room


def find_rooms(rooms: list[dict], query: str) -> list[dict]:
    query = query.strip().lower()
    return [room for room in rooms if query in room["name"].lower()]


def filter_rooms(rooms: list[dict], participants: int,
                 needs_projector: bool = False) -> Iterator[dict]:
    """Отбирает помещения, где хватит мест и есть нужный проектор."""
    for room in rooms:
        fits = check_capacity(participants, room["capacity"])
        equipped = check_equipment(needs_projector, room["has_projector"])
        if fits and equipped:
            yield room


def sort_rooms(rooms: list[dict], key: str = "capacity") -> list[dict]:
    return sorted(rooms, key=lambda room: room[key])
