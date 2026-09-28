from datetime import date, datetime, time


def get_next_id(items: list[dict]) -> int:
    return max((item["id"] for item in items), default=0) + 1


def input_int(prompt: str, min_value: int = 0) -> int:
    while True:
        try:
            number = int(input(prompt))
        except ValueError:
            print("Нужно ввести целое число")
            continue
        if number < min_value:
            print(f"Число должно быть не меньше {min_value}")
            continue
        return number


def _input_datetime(prompt: str, fmt: str, example: str) -> datetime:
    while True:
        text = input(prompt).strip()
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            print(f"Неверный формат, пример: {example}")


def input_date(prompt: str) -> date:
    return _input_datetime(prompt, "%d.%m.%Y", "15.10.2026").date()


def input_time(prompt: str) -> time:
    return _input_datetime(prompt, "%H:%M", "09:30").time()


def input_yes_no(prompt: str) -> bool:
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("да", "д"):
            return True
        if answer in ("нет", "н"):
            return False
        print("Ответьте да или нет")
