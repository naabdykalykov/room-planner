from datetime import date, datetime
from calc import (get_age_years, get_difference, get_result,
                  get_shortage_cost, needs_replacement)
from storage import ROOMS_FILE, load_data, ITEMS_FILE
from items import get_room_items, get_total
from utils import input_int

# дата проверки для примера из ПР1
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

    # считаем через функции из calc
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


# печатает одну строку с предметом
def print_item(item):
    print(f"   {item['number']} {item['name']}: "
          f"{item['quantity']} шт. по {item['price']} руб.")


# все помещения с предметами и итогами
def show_rooms(rooms, items):
    for room in rooms:
        print(f"{room['id']}. {room['name']}, этаж {room['floor']}, "
              f"ответственный: {room['responsible']}")
        room_items = list(get_room_items(items, room["id"]))
        for item in room_items:
            print_item(item)
        count, cost = get_total(room_items)
        print(f"   Всего: {count} шт. на {cost} руб.")


# предметы одного помещения по его номеру
def show_room_items(items):
    room_id = input_int("Номер помещения: ")
    room_items = list(get_room_items(items, room_id))
    if not room_items:
        print("В помещении нет предметов")
    for item in room_items:
        print_item(item)


# пример из ПР1: проверка трех предметов
def show_demo():
    print(f"Дата проверки: {CHECK_DATE.strftime('%d.%m.%Y')}")
    print()
    check_item("1001", "Кресло офисное", "12", "10", "4500.50",
               "15.03.2022", "7", "да")
    check_item("1003", "Ноутбук", "10", "10", "62000",
               "01.09.2023", "5", "да")
    check_item("1004", "Принтер", "1", "1", "18500",
               "20.05.2018", "5", "да")


# загружает данные и запускает меню
def main():
    print("Сервис инвентаризации офисных помещений")
    rooms = load_data(ROOMS_FILE)
    items = load_data(ITEMS_FILE)
    while True:
        print()
        print("1. Показать помещения")
        print("2. Предметы помещения")
        print("3. Проверка трех предметов")
        print("0. Выход")
        choice = input("Выберите действие: ")
        if choice == "0":
            break
        elif choice == "1":
            show_rooms(rooms, items)
        elif choice == "2":
            show_room_items(items)
        elif choice == "3":
            show_demo()
        else:
            print("Нет такого пункта")


if __name__ == "__main__":
    main()
