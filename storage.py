import json

ROOMS_FILE = "data/rooms.json"
ITEMS_FILE = "data/items.json"


def load_data(path: str):
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
    """Сохраняет список записей в JSON-ФАЙЛ"""
    with open(path, "w", encoding="UTF-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
