from datetime import date

from bookings import (cancel_booking, create_booking, find_free_rooms,
                      get_period, get_room_schedule, get_statistics)
from checks import get_occupancy_percent
from rooms import add_room, find_room_by_id, find_rooms, sort_rooms
from storage import BOOKINGS_FILE, ROOMS_FILE, load_data, save_data
from utils import input_date, input_int, input_time, input_yes_no

MENU_ITEMS = (
    "Показать помещения",
    "Найти помещение по названию",
    "Подобрать свободное помещение",
    "Забронировать помещение",
    "Отменить бронирование",
    "Расписание помещения на день",
    "Показать все бронирования",
    "Добавить помещение",
    "Статистика",
)


def print_menu() -> None:
    print("\n=== Сервис планирования использования помещений ===")
    for number, item in enumerate(MENU_ITEMS, start=1):
        print(f"{number}. {item}")
    print("0. Выход")


def get_room_name(rooms: list[dict], room_id: int) -> str:
    room = find_room_by_id(rooms, room_id)
    return room["name"] if room else f"помещение {room_id}"


def show_rooms(rooms: list[dict]) -> None:
    for room in rooms:
        projector = "да" if room["has_projector"] else "нет"
        print(f"{room['id']:>3}. {room['name']}, мест: {room['capacity']}, "
              f"проектор: {projector}, {room['opens']}-{room['closes']}")


def format_booking(rooms: list[dict], booking: dict) -> str:
    day = date.fromisoformat(booking["date"]).strftime("%d.%m.%Y")
    room_name = get_room_name(rooms, booking["room_id"])
    return (f"{booking['id']:>3}. {day} {booking['start']}-{booking['end']}"
            f", {room_name}: {booking['title']}"
            f" ({booking['participants']} чел.)")


def show_bookings(rooms: list[dict], bookings: list[dict]) -> None:
    if not bookings:
        print("Бронирований нет")
    for booking in sorted(bookings, key=lambda b: get_period(b)[0]):
        print(format_booking(rooms, booking))


def ask_room(rooms: list[dict]) -> dict | None:
    show_rooms(rooms)
    room = find_room_by_id(rooms, input_int("Номер помещения: "))
    if room is None:
        print("Такого помещения нет")
    return room


def ask_request() -> dict:
    day = input_date("Дата (ДД.ММ.ГГГГ): ")
    start = input_time("Начало (ЧЧ:ММ): ")
    end = input_time("Конец (ЧЧ:ММ): ")
    return {
        "date": day.isoformat(),
        "start": start.strftime("%H:%M"),
        "end": end.strftime("%H:%M"),
        "participants": input_int("Количество участников: ", min_value=1),
        "needs_projector": input_yes_no("Нужен проектор (да/нет): "),
    }


def search_rooms_menu(rooms: list[dict]) -> None:
    found = find_rooms(rooms, input("Часть названия: "))
    if found:
        show_rooms(found)
    else:
        print("Ничего не найдено")


def free_rooms_menu(rooms: list[dict], bookings: list[dict]) -> None:
    free = find_free_rooms(rooms, bookings, ask_request())
    if free:
        print("Подходят и свободны:")
        show_rooms(free)
    else:
        print("Свободных подходящих помещений нет")


def book_room_menu(rooms: list[dict], bookings: list[dict]) -> None:
    room = ask_room(rooms)
    if room is None:
        return
    title = input("Название мероприятия: ").strip() or "Без названия"
    request = {"room_id": room["id"], "title": title}
    request.update(ask_request())
    percent = get_occupancy_percent(request["participants"], room["capacity"])
    print(f"Заполненность помещения: {percent}%")
    try:
        booking = create_booking(bookings, room, request)
    except ValueError as error:
        print(f"Заявка {error}")
    else:
        save_data(BOOKINGS_FILE, bookings)
        print(f"Заявка одобрена, номер бронирования: {booking['id']}")


def cancel_booking_menu(rooms: list[dict], bookings: list[dict]) -> None:
    show_bookings(rooms, bookings)
    if not bookings:
        return
    booking_id = input_int("Номер бронирования для отмены: ", min_value=1)
    try:
        booking = cancel_booking(bookings, booking_id)
    except ValueError as error:
        print(f"Не получилось: {error}")
    else:
        save_data(BOOKINGS_FILE, bookings)
        print(f"Бронирование отменено: {booking['title']}")


def schedule_menu(rooms: list[dict], bookings: list[dict]) -> None:
    room = ask_room(rooms)
    if room is None:
        return
    day = input_date("Дата (ДД.ММ.ГГГГ): ")
    schedule = get_room_schedule(bookings, room["id"], day)
    if not schedule:
        print("В этот день помещение свободно")
    for booking in schedule:
        print(format_booking(rooms, booking))


def add_room_menu(rooms: list[dict]) -> None:
    name = input("Название помещения: ").strip()
    if not name:
        print("Название не может быть пустым")
        return
    capacity = input_int("Количество мест: ", min_value=1)
    has_projector = input_yes_no("Есть проектор (да/нет): ")
    opens = input_time("Открывается в (ЧЧ:ММ): ")
    closes = input_time("Закрывается в (ЧЧ:ММ): ")
    try:
        room = add_room(rooms, name, capacity, has_projector, opens, closes)
    except ValueError as error:
        print(f"Не получилось: {error}")
    else:
        save_data(ROOMS_FILE, rooms)
        print(f"Помещение добавлено под номером {room['id']}")


def statistics_menu(rooms: list[dict], bookings: list[dict]) -> None:
    stats = get_statistics(rooms, bookings)
    print(f"Всего бронирований: {stats['total']}")
    print(f"Занято часов: {stats['hours']}")
    print(f"Дней с мероприятиями: {stats['days']}")
    print("По помещениям:")
    for room_id, count in stats["by_room"].items():
        print(f"  {get_room_name(rooms, room_id)}: {count}")
    if stats["busiest_id"] is not None:
        busiest = get_room_name(rooms, stats["busiest_id"])
        print(f"Самое загруженное помещение: {busiest}")


def main() -> None:
    """Загружает данные из JSON и запускает меню программы."""
    rooms = load_data(ROOMS_FILE)
    bookings = load_data(BOOKINGS_FILE)
    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            print("До свидания!")
            break
        elif choice == "1":
            show_rooms(sort_rooms(rooms))
        elif choice == "2":
            search_rooms_menu(rooms)
        elif choice == "3":
            free_rooms_menu(rooms, bookings)
        elif choice == "4":
            book_room_menu(rooms, bookings)
        elif choice == "5":
            cancel_booking_menu(rooms, bookings)
        elif choice == "6":
            schedule_menu(rooms, bookings)
        elif choice == "7":
            show_bookings(rooms, bookings)
        elif choice == "8":
            add_room_menu(rooms)
        elif choice == "9":
            statistics_menu(rooms, bookings)
        else:
            print("Нет такого пункта меню")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nПрограмма остановлена")
