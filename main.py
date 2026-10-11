from models import Check, Item, Result, Room
from models.checks import create_check
from models.items import (add_item, find_items, get_room_items, get_total,
                          move_item, sort_items, write_off_item)
from models.results import (add_result, get_check_results, get_statistics,
                            get_summary)
from models.rooms import find_room_by_id, sort_rooms
from storage import (load_checks, load_items, load_results, load_rooms,
                     save_checks, save_items, save_results, save_rooms)
from utils import (input_date, input_float, input_int, input_text,
                   input_yes_no)

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


def show_rooms(rooms: list[Room], items: list[Item]) -> None:
    """Помещения с количеством и стоимостью предметов."""
    for room in sort_rooms(rooms):
        count, cost = get_total(get_room_items(items, room))
        print(f"{room.id}. {room}, предметов: {count} шт. на {cost} руб.")


def show_summary(summary: dict) -> None:
    """Печатает итоги проверки."""
    print(f"Проверено предметов: {summary['checked']}")
    print(f"Недостач: {summary['shortages']}, "
          f"излишков: {summary['surpluses']}, "
          f"требуют замены: {summary['replacements']}")
    print(f"Сумма недостачи: {summary['shortage_cost']} руб.")


def ask_room(rooms: list[Room], items: list[Item]) -> Room | None:
    """Показывает помещения и спрашивает номер одного из них."""
    show_rooms(rooms, items)
    room = find_room_by_id(rooms, input_int("Номер помещения: "))
    if room is None:
        print("Такого помещения нет")
    return room


def room_items_menu(rooms: list[Room], items: list[Item]) -> None:
    """Пункт 2: предметы одного помещения по названию."""
    room = ask_room(rooms, items)
    if room is None:
        return
    room_items = sort_items(get_room_items(items, room))
    if not room_items:
        print("В помещении нет предметов")
    for item in room_items:
        print(f"   {item}")


def find_item_menu(items: list[Item]) -> None:
    """Пункт 3: поиск предмета по названию или номеру."""
    found = find_items(items, input_text("Название или инвентарный номер: "))
    if not found:
        print("Ничего не найдено")
    for item in sort_items(found):
        print(f"   {item}")


def add_item_menu(rooms: list[Room], items: list[Item]) -> None:
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
        item = add_item(items, number, name, room, quantity, price,
                        purchase_date, service_life)
    except ValueError as error:
        print(f"Не получилось: {error}")
    else:
        save_items(items)
        print(f"Добавлен предмет: {item}")


def move_item_menu(rooms: list[Room], items: list[Item]) -> None:
    """Пункт 5: перенос предмета в другое помещение."""
    number = input_text("Инвентарный номер предмета: ")
    print("Куда переносим:")
    room = ask_room(rooms, items)
    if room is None:
        return
    try:
        item = move_item(items, number, room)
    except ValueError as error:
        print(f"Не получилось: {error}")
    else:
        save_items(items)
        print(f"{item.name} теперь в помещении {item.room.name}")


def write_off_menu(items: list[Item]) -> None:
    """Пункт 6: списание предмета."""
    number = input_text("Инвентарный номер предмета: ")
    try:
        item = write_off_item(items, number)
    except ValueError as error:
        print(f"Не получилось: {error}")
    else:
        save_items(items)
        print(f"Предмет списан: {item.name}")


def run_check_menu(rooms: list[Room], items: list[Item],
                   checks: list[Check], results: list[Result]) -> None:
    """Пункт 7: проверка всех предметов одного помещения."""
    room = ask_room(rooms, items)
    if room is None:
        return
    room_items = sort_items(get_room_items(items, room))
    if not room_items:
        print("В помещении нет предметов")
        return
    day = input_date("Дата проверки (ДД.ММ.ГГГГ): ")
    inspector = input_text("Проверяющий: ")
    check = create_check(checks, room, day, inspector)
    for item in room_items:
        print(f"{item.number} {item.name}, по учету: {item.quantity}")
        actual = input_int("  Фактически: ")
        is_working = input_yes_no("  Исправен (да/нет): ")
        result = add_result(results, check, item, actual, is_working)
        print(f"  Результат: {result.status}")
    save_checks(checks)
    save_results(results)
    print("Итоги проверки:")
    show_summary(get_summary(get_check_results(results, check)))


def results_menu(checks: list[Check], results: list[Result]) -> None:
    """Пункт 8: все проверки с результатами по предметам."""
    if not checks:
        print("Проверок еще не было")
    for check in sorted(checks, key=lambda check: check.date):
        print(check)
        check_results = get_check_results(results, check)
        for result in check_results:
            print(f"   {result}")
        show_summary(get_summary(check_results))


def statistics_menu(rooms: list[Room], items: list[Item],
                    checks: list[Check], results: list[Result]) -> None:
    """Пункт 9: общая статистика."""
    stats = get_statistics(rooms, items, checks, results)
    print(f"Всего предметов: {stats['units']} шт. на {stats['cost']} руб.")
    print("По помещениям:")
    for name, (count, cost) in stats["by_room"].items():
        print(f"   {name}: {count} шт. на {cost} руб.")
    print(f"Списано предметов: {stats['written_off']}")
    print(f"Проверено помещений: {stats['checked_rooms']} из {len(rooms)}")
    print(f"Общая сумма недостачи: {stats['shortage_cost']} руб.")


def save_all(rooms: list[Room], items: list[Item], checks: list[Check],
             results: list[Result]) -> None:
    """Сохраняет все данные в JSON перед выходом."""
    save_rooms(rooms)
    save_items(items)
    save_checks(checks)
    save_results(results)


def main() -> None:
    """Загружает объекты из JSON и запускает меню программы."""
    print("Сервис инвентаризации офисных помещений")
    rooms = load_rooms()
    items = load_items(rooms)
    checks = load_checks(rooms)
    results = load_results(checks, items)
    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            save_all(rooms, items, checks, results)
            break
        elif choice == "1":
            show_rooms(rooms, items)
        elif choice == "2":
            room_items_menu(rooms, items)
        elif choice == "3":
            find_item_menu(items)
        elif choice == "4":
            add_item_menu(rooms, items)
        elif choice == "5":
            move_item_menu(rooms, items)
        elif choice == "6":
            write_off_menu(items)
        elif choice == "7":
            run_check_menu(rooms, items, checks, results)
        elif choice == "8":
            results_menu(checks, results)
        elif choice == "9":
            statistics_menu(rooms, items, checks, results)
        else:
            print("Нет такого пункта")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nПрограмма остановлена")
