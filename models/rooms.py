class Room:
    """Помещение офиса."""

    def __init__(self, room_id: int, name: str, floor: int,
                 responsible: str) -> None:
        """Создает помещение и сохраняет его данные в атрибутах."""
        self.id = room_id
        self.name = name
        self.floor = floor
        self.responsible = responsible

    @classmethod
    def from_data(cls, data: dict) -> "Room":
        """Создает помещение из словаря, прочитанного из JSON."""
        return cls(data["id"], data["name"], data["floor"],
                   data["responsible"])

    def to_data(self) -> dict:
        """Превращает помещение в словарь для записи в JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "floor": self.floor,
            "responsible": self.responsible,
        }

    def __str__(self) -> str:
        """Строка, которую печатает print(room)."""
        return (f"{self.name}, этаж {self.floor}, "
                f"ответственный: {self.responsible}")


def find_room_by_id(rooms: list[Room], room_id: int) -> Room | None:
    """Ищет помещение по номеру, если его нет - возвращает None."""
    for room in rooms:
        if room.id == room_id:
            return room
    return None


def sort_rooms(rooms: list[Room]) -> list[Room]:
    """Сортирует помещения по этажу и названию."""
    return sorted(rooms, key=lambda room: (room.floor, room.name))
