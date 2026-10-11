from checks import (add_result, create_check, get_check_results,
                    get_statistics, get_summary)
from items import (add_item, find_items, get_room_items, get_total,
                   move_item, sort_items, write_off_item)
from rooms import find_room_by_id, sort_rooms
from storage import (CHECKS_FILE, ITEMS_FILE, RESULTS_FILE, ROOMS_FILE,
                     load_data, save_data)
from utils import (format_date, input_date, input_float, input_int,
                   input_text, input_yes_no)

MENU_ITEMS = (
    "Показать помещения",
    "Предметы помещения",
    "Найти предмет",
    "Добавить предмет",
    "Переместить предмет",
    "Списать предмет",
    "Провести проверку помещения",
    "Результаты проверок",
    "Статистика",
)


def print_menu() -> None:
    """Печатает пункты меню с номерами."""
    print()
    for number, item in enumerate(MENU_ITEMS, start=1):
        print(f"{number}. {item}")
    print("0. Выход")


def get_room_name(rooms: list[dict], room_id: int) -> str:
    """Название помещения по номеру."""
    room = find_room_by_id(rooms, room_id)
    return room["name"] if room else f"помещение {room_id}"


def print_item(rooms: list[dict], item: dict) -> None:
    """Печатает одну строку с предметом."""
    print(f"   {item['number']} {item['name']}, "
          f"{get_room_name(rooms, item['room_id'])}: "
          f"{item['quantity']} шт. по {item['price']} руб., "
          f"куплено {format_date(item['purchase_date'])}")


def show_rooms(rooms: list[dict], items: list[dict]) -> None:
    """Помещения с количеством и стоимостью предметов."""
    for room in sort_rooms(rooms):
        count, cost = get_total(get_room_items(items, room["id"]))
        print(f"{room['id']}. {room['name']}, этаж {room['floor']}, "
              f"ответственный: {room['responsible']}, "
              f"предметов: {count} шт. на {cost} руб.")


def show_summary(summary: dict) -> None:
    """Печатает итоги проверки."""
    print(f"Проверено предметов: {summary['checked']}")
    print(f"Недостач: {summary['shortages']}, "
          f"излишков: {summary['surpluses']}, "
          f"требуют замены: {summary['replacements']}")
    print(f"Сумма недостачи: {summary['shortage_cost']} руб.")


def ask_room(rooms: list[dict], items: list[dict]) -> dict | None:
    """Показывает помещения и спрашивает номер одного из них."""
    show_rooms(rooms, items)
    room = find_room_by_id(rooms, input_int("Номер помещения: "))
    if room is None:
        print("Такого помещения нет")
    return room


def room_items_menu(rooms: list[dict], items: list[dict]) -> None:
    """Пункт 2: предметы одного помещения по названию."""
    room = ask_room(rooms, items)
    if room is None:
        return
    room_items = sort_items(get_room_items(items, room["id"]))
    if not room_items:
        print("В помещении нет предметов")
    for item in room_items:
        print_item(rooms, item)


def find_item_menu(rooms: list[dict], items: list[dict]) -> None:
    """Пункт 3: поиск предмета по названию или номеру."""
    found = find_items(items, input_text("Название или инвентарный номер: "))
    if not found:
        print("Ничего не найдено")
    for item in sort_items(found):
        print_item(rooms, item)


def add_item_menu(rooms: list[dict], items: list[dict]) -> None:
    """Пункт 4: добавление предмета в помещение."""
    room = ask_room(rooms, items)
    if room is None:
        return
    number = input_text("Инвентарный номер: ")
    name = input_text("Название предмета: ")
    quantity = input_int("Количество: ", min_value=1)
    price = input_float("Цена за штуку: ", min_value=0.01)
    purchase_date = input_date("Дата покупки (ДД.ММ.ГГГГ): ")
    service_life = input_int("Срок службы (лет): ", min_value=1)
    try:
        add_item(items, number, name, room["id"], quantity, price,
                 purchase_date, service_life)
    except ValueError as error:
        print(f"Не получилось: {error}")
    else:
        save_data(ITEMS_FILE, items)
        print(f"Предмет {number} добавлен в помещение {room['name']}")


def move_item_menu(rooms: list[dict], items: list[dict]) -> None:
    """Пункт 5: перенос предмета в другое помещение."""
    number = input_text("Инвентарный номер предмета: ")
    print("Куда переносим:")
    room = ask_room(rooms, items)
    if room is None:
        return
    try:
        item = move_item(items, number, room["id"])
    except ValueError as error:
        print(f"Не получилось: {error}")
    else:
        save_data(ITEMS_FILE, items)
        print(f"{item['name']} теперь в помещении {room['name']}")


def write_off_menu(items: list[dict]) -> None:
    """Пункт 6: списание предмета."""
    number = input_text("Инвентарный номер предмета: ")
    try:
        item = write_off_item(items, number)
    except ValueError as error:
        print(f"Не получилось: {error}")
    else:
        save_data(ITEMS_FILE, items)
        print(f"Предмет списан: {item['name']}")


def run_check_menu(rooms: list[dict], items: list[dict],
                   checks: list[dict], results: list[dict]) -> None:
    """Пункт 7: проверка всех предметов одного помещения."""
    room = ask_room(rooms, items)
    if room is None:
        return
    room_items = sort_items(get_room_items(items, room["id"]))
    if not room_items:
        print("В помещении нет предметов")
        return
    day = input_date("Дата проверки (ДД.ММ.ГГГГ): ")
    inspector = input_text("Проверяющий: ")
    check = create_check(checks, room["id"], day, inspector)
    for item in room_items:
        print(f"{item['number']} {item['name']}, "
              f"по учету: {item['quantity']}")
        actual = input_int("  Фактически: ")
        is_working = input_yes_no("  Исправен (да/нет): ")
        result = add_result(results, check, item, actual, is_working)
        print(f"  Результат: {result['status']}")
    save_data(CHECKS_FILE, checks)
    save_data(RESULTS_FILE, results)
    print("Итоги проверки:")
    show_summary(get_summary(get_check_results(results, check["id"])))


def results_menu(rooms: list[dict], checks: list[dict],
                 results: list[dict]) -> None:
    """Пункт 8: все проверки с результатами по предметам."""
    if not checks:
        print("Проверок еще не было")
    for check in sorted(checks, key=lambda check: check["date"]):
        print(f"Проверка {check['id']}: {format_date(check['date'])}, "
              f"{get_room_name(rooms, check['room_id'])}, "
              f"проверяющий: {check['inspector']}")
        check_results = get_check_results(results, check["id"])
        for result in check_results:
            print(f"   {result['number']} {result['name']}: "
                  f"по учету {result['expected']}, "
                  f"фактически {result['actual']}, {result['status']}")
        show_summary(get_summary(check_results))


def statistics_menu(rooms: list[dict], items: list[dict],
                    checks: list[dict], results: list[dict]) -> None:
    """Пункт 9: общая статистика."""
    stats = get_statistics(rooms, items, checks, results)
    print(f"Всего предметов: {stats['units']} шт. на {stats['cost']} руб.")
    print("По помещениям:")
    for name, (count, cost) in stats["by_room"].items():
        print(f"   {name}: {count} шт. на {cost} руб.")
    print(f"Проверено помещений: {stats['checked_rooms']} из {len(rooms)}")
    print(f"Общая сумма недостачи: {stats['shortage_cost']} руб.")


def main() -> None:
    """Загружает данные из JSON и запускает меню программы."""
    print("Сервис инвентаризации офисных помещений")
    rooms = load_data(ROOMS_FILE)
    items = load_data(ITEMS_FILE)
    checks = load_data(CHECKS_FILE)
    results = load_data(RESULTS_FILE)
    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            break
        elif choice == "1":
            show_rooms(rooms, items)
        elif choice == "2":
            room_items_menu(rooms, items)
        elif choice == "3":
            find_item_menu(rooms, items)
        elif choice == "4":
            add_item_menu(rooms, items)
        elif choice == "5":
            move_item_menu(rooms, items)
        elif choice == "6":
            write_off_menu(items)
        elif choice == "7":
            run_check_menu(rooms, items, checks, results)
        elif choice == "8":
            results_menu(rooms, checks, results)
        elif choice == "9":
            statistics_menu(rooms, items, checks, results)
        else:
            print("Нет такого пункта")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nПрограмма остановлена")
