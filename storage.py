import json

from models import Check, Item, Result, Room
from models.checks import find_check_by_id
from models.items import find_item_by_id
from models.rooms import find_room_by_id

ROOMS_FILE = "data/rooms.json"
ITEMS_FILE = "data/items.json"
CHECKS_FILE = "data/checks.json"
RESULTS_FILE = "data/results.json"


def load_data(path: str) -> list[dict]:
    """Загружает список записей из JSON-файла."""
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {path} не найден, список пустой")
        return []
    except json.JSONDecodeError:
        print(f"Файл {path} поврежден, список пустой")
        return []


def save_data(path: str, data: list[dict]) -> None:
    """Сохраняет список записей в JSON-файл."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_rooms(path: str = ROOMS_FILE) -> list[Room]:
    """Загружает помещения и превращает словари в объекты Room."""
    return [Room.from_data(data) for data in load_data(path)]


def save_rooms(rooms: list[Room], path: str = ROOMS_FILE) -> None:
    """Сохраняет помещения в JSON."""
    save_data(path, [room.to_data() for room in rooms])


def load_items(rooms: list[Room], path: str = ITEMS_FILE) -> list[Item]:
    """Загружает предметы и связывает каждый с объектом помещения."""
    items = []
    for data in load_data(path):
        room = find_room_by_id(rooms, data["room_id"])
        if room is None:
            print(f"Предмет {data['number']} пропущен: нет помещения")
            continue
        items.append(Item.from_data(data, room))
    return items


def save_items(items: list[Item], path: str = ITEMS_FILE) -> None:
    """Сохраняет предметы в JSON."""
    save_data(path, [item.to_data() for item in items])


def load_checks(rooms: list[Room], path: str = CHECKS_FILE) -> list[Check]:
    """Загружает проверки и связывает каждую с объектом помещения."""
    checks = []
    for data in load_data(path):
        room = find_room_by_id(rooms, data["room_id"])
        if room is None:
            print(f"Проверка {data['id']} пропущена: нет помещения")
            continue
        checks.append(Check.from_data(data, room))
    return checks


def save_checks(checks: list[Check], path: str = CHECKS_FILE) -> None:
    """Сохраняет проверки в JSON."""
    save_data(path, [check.to_data() for check in checks])


def load_results(checks: list[Check], items: list[Item],
                 path: str = RESULTS_FILE) -> list[Result]:
    """Загружает результаты и связывает их с проверкой и предметом."""
    results = []
    for data in load_data(path):
        check = find_check_by_id(checks, data["check_id"])
        item = find_item_by_id(items, data["item_id"])
        if check is None or item is None:
            print(f"Результат {data['id']} пропущен: нет проверки "
                  "или предмета")
            continue
        results.append(Result.from_data(data, check, item))
    return results


def save_results(results: list[Result], path: str = RESULTS_FILE) -> None:
    """Сохраняет результаты в JSON."""
    save_data(path, [result.to_data() for result in results])
