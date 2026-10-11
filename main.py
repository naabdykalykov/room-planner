from datetime import date, datetime
from calc import (get_age_years, get_difference, get_result,
                  get_shortage_cost, needs_replacement)

# помещение и дата проверки, одни на всю программу
ROOM_NAME = "Кабинет 204"
CHECK_DATE = date(2026, 10, 12)


# проверяет один предмет и печатает отчет по нему
def check_item(number, name, expected_text, actual_text, price_text,
               purchase_text, life_text, working_answer):
    # данные приходят строками, переводим их в нужные типы
    expected = int(expected_text)
    actual = int(actual_text)
    price = float(price_text)
    purchase_date = datetime.strptime(purchase_text, "%d.%m.%Y").date()
    service_life = int(life_text)
    is_working = working_answer.lower() == "да"

    # считаем через функции выше
    difference = get_difference(expected, actual)
    shortage_cost = get_shortage_cost(expected, actual, price)
    age_years = get_age_years(purchase_date, CHECK_DATE)
    replace = needs_replacement(age_years, service_life, is_working)
    result = get_result(difference, replace)

    # печатаем отчет
    print(f"Предмет: {name} (инв. номер {number})")
    print(f"  По учету: {expected}, фактически: {actual}")
    print(f"  Возраст, лет: {age_years}, срок службы, лет: {service_life}")
    print(f"  Исправен: {working_answer}")
    print(f"  Результат: {result}")
    if shortage_cost > 0:
        print(f"  Сумма недостачи: {shortage_cost} руб.")
    print()


# шапка и проверка трех предметов
def main():
    print("Сервис инвентаризации офисных помещений")
    print(f"Помещение: {ROOM_NAME}")
    print(f"Дата проверки: {CHECK_DATE.strftime('%d.%m.%Y')}")
    print()
    check_item("1001", "Кресло офисное", "12", "10", "4500.50",
               "15.03.2022", "7", "да")
    check_item("1003", "Ноутбук", "10", "10", "62000",
               "01.09.2023", "5", "да")
    check_item("1004", "Принтер", "1", "1", "18500",
               "20.05.2018", "5", "да")


if __name__ == "__main__":
    main()
