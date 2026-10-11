from datetime import date, datetime


def input_int(prompt: str, min_value: int = 0) -> int:
    """Спрашивает целое число, пока не введут правильно."""
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


def input_float(prompt: str, min_value: float = 0) -> float:
    """Спрашивает число с дробной частью, пока не введут правильно."""
    while True:
        try:
            number = float(input(prompt).replace(",", "."))
        except ValueError:
            print("Нужно ввести число")
            continue
        if number < min_value:
            print(f"Число должно быть не меньше {min_value}")
            continue
        return number


def input_date(prompt: str) -> date:
    """Спрашивает дату в формате ДД.ММ.ГГГГ."""
    while True:
        try:
            return datetime.strptime(input(prompt).strip(), "%d.%m.%Y").date()
        except ValueError:
            print("Неверный формат, пример: 12.10.2026")


def input_text(prompt: str) -> str:
    """Спрашивает непустую строку."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("Поле не может быть пустым")


def input_yes_no(prompt: str) -> bool:
    """Спрашивает ответ да или нет."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("да", "д"):
            return True
        if answer in ("нет", "н"):
            return False
        print("Ответьте да или нет")
