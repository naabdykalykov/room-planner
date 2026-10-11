from models import Room
from models.rooms import find_room_by_id, sort_rooms


def make_rooms():
    return [
        Room(1, "Кабинет 204", 2, "Иванова А. С."),
        Room(2, "Переговорная 305", 3, "Петров Д. И."),
        Room(3, "Серверная 101", 1, "Смирнов К. А."),
    ]


def test_room_creation():
    room = Room(1, "Кабинет 204", 2, "Иванова А. С.")
    assert room.id == 1
    assert room.name == "Кабинет 204"
    assert room.floor == 2
    assert room.responsible == "Иванова А. С."


def test_room_str():
    room = Room(1, "Кабинет 204", 2, "Иванова А. С.")
    assert str(room) == "Кабинет 204, этаж 2, ответственный: Иванова А. С."


def test_room_from_data_and_back():
    data = {"id": 1, "name": "Кабинет 204", "floor": 2,
            "responsible": "Иванова А. С."}
    room = Room.from_data(data)
    assert room.name == "Кабинет 204"
    assert room.to_data() == data


def test_find_room_by_id():
    rooms = make_rooms()
    assert find_room_by_id(rooms, 2) is rooms[1]
    assert find_room_by_id(rooms, 99) is None


def test_sort_rooms():
    names = [room.name for room in sort_rooms(make_rooms())]
    assert names == ["Серверная 101", "Кабинет 204", "Переговорная 305"]
