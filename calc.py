from datetime import date

OK = "в наличии"
SHORTAGE = "недостача"
SURPLUS = "излишек"
REPLACE = "в наличии, требуется замена"


def get_difference(expected: int, actual: int) -> int:
    """Сколько штук не хватает: плюс - недостача, минус - излишек."""
    return expected - actual


def get_shortage_cost(expected: int, actual: int, price: float) -> float:
    """Сумма недостачи в рублях, если недостачи нет - 0."""
    if actual >= expected:
        return 0.0
    return round(get_difference(expected, actual) * price, 2)


def get_age_years(purchase_date: date, check_date: date) -> float:
    """Возраст предмета в годах на дату проверки."""
    return round((check_date - purchase_date).days / 365, 1)


def needs_replacement(age_years: float, service_life: int,
                      is_working: bool) -> bool:
    """Нужна ли замена: предмет сломан или старше срока службы."""
    return not is_working or age_years > service_life


def get_result(difference: int, replace: bool) -> str:
    """Итог проверки предмета по разнице и признаку замены."""
    if difference > 0:
        return SHORTAGE
    elif difference < 0:
        return SURPLUS
    elif replace:
        return REPLACE
    else:
        return OK
