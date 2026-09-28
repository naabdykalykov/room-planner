import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
ROOMS_FILE = DATA_DIR / "rooms.json"
BOOKINGS_FILE = DATA_DIR / "bookings.json"


def load_data(path: Path) -> list[dict]:
    """Загружает список записей из JSON-файла."""
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Файл {path.name} не найден, список пока пустой")
        return []
    except json.JSONDecodeError:
        print(f"Файл {path.name} поврежден, список пока пустой")
        return []
    if not isinstance(data, list):
        print(f"В файле {path.name} должен быть список, список пока пустой")
        return []
    return data


def save_data(path: Path, data: list[dict]) -> None:
    """Сохраняет список записей в JSON-файл."""
    path.parent.mkdir(exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
