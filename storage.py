import json

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
