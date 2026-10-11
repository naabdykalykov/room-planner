def find_room_by_id(rooms: list[dict], room_id: int) -> dict | None:
    """Ищет помещение по номеру, если его нет - возвращает None."""
    for room in rooms:
        if room["id"] == room_id:
            return room
    return None


def sort_rooms(rooms: list[dict]) -> list[dict]:
    """Сортирует помещения по этажу и названию."""
    return sorted(rooms, key=lambda room: (room["floor"], room["name"]))
