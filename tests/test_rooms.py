from datetime import time

import pytest

from rooms import add_room, filter_rooms, find_rooms, sort_rooms

ROOMS = [
    {"id": 1, "name": "Конференц-зал Сириус", "capacity": 40,
     "has_projector": True, "opens": "08:30", "closes": "21:00"},
    {"id": 2, "name": "Переговорная 3", "capacity": 8,
     "has_projector": False, "opens": "09:00", "closes": "19:00"},
]


def test_find_rooms_ignores_case():
    assert find_rooms(ROOMS, "сириус") == [ROOMS[0]]


def test_filter_rooms_by_projector():
    assert list(filter_rooms(ROOMS, 5, needs_projector=True)) == [ROOMS[0]]


def test_sort_rooms_by_capacity():
    names = [room["name"] for room in sort_rooms(ROOMS)]
    assert names == ["Переговорная 3", "Конференц-зал Сириус"]


def test_add_room_with_wrong_hours():
    with pytest.raises(ValueError):
        add_room([], "Кабинет", 10, False, time(18, 0), time(9, 0))
