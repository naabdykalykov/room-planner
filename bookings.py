from datetime import date, datetime, time

from checks import (APPROVED, check_capacity, check_equipment,
                    check_working_hours, get_decision, has_time_conflict)
from rooms import filter_rooms, sort_rooms
from utils import get_next_id


def get_period(booking: dict) -> tuple[datetime, datetime]:
    day = date.fromisoformat(booking["date"])
    start = datetime.combine(day, time.fromisoformat(booking["start"]))
    end = datetime.combine(day, time.fromisoformat(booking["end"]))
    return start, end


def find_conflicts(bookings: list[dict], room_id: int,
                   start: datetime, end: datetime) -> list[dict]:
    conflicts = []
    for booking in bookings:
        if booking["room_id"] != room_id:
            continue
        booked_start, booked_end = get_period(booking)
        if has_time_conflict(start, end, booked_start, booked_end):
            conflicts.append(booking)
    return conflicts


def is_room_free(bookings: list[dict], room_id: int,
                 start: datetime, end: datetime) -> bool:
    return not find_conflicts(bookings, room_id, start, end)


def check_request(room: dict, bookings: list[dict], request: dict) -> str:
    """Проверяет заявку по правилам из ПР1 и возвращает решение."""
    start, end = get_period(request)
    opens = time.fromisoformat(room["opens"])
    closes = time.fromisoformat(room["closes"])
    in_hours = check_working_hours(start, end, opens, closes)
    conflict = not is_room_free(bookings, room["id"], start, end)
    fits = check_capacity(request["participants"], room["capacity"])
    equipped = check_equipment(request["needs_projector"],
                               room["has_projector"])
    return get_decision(in_hours, conflict, fits, equipped)


def create_booking(bookings: list[dict], room: dict, request: dict) -> dict:
    """Создает бронирование, если заявка одобрена, иначе ValueError."""
    decision = check_request(room, bookings, request)
    if decision != APPROVED:
        raise ValueError(decision)
    booking = {"id": get_next_id(bookings)}
    booking.update(request)
    bookings.append(booking)
    return booking


def cancel_booking(bookings: list[dict], booking_id: int) -> dict:
    """Удаляет бронирование по номеру, если его нет - ValueError."""
    for index, booking in enumerate(bookings):
        if booking["id"] == booking_id:
            return bookings.pop(index)
    raise ValueError(f"бронирование номер {booking_id} не найдено")


def get_room_schedule(bookings: list[dict], room_id: int,
                      day: date) -> list[dict]:
    schedule = [
        booking for booking in bookings
        if booking["room_id"] == room_id
        and booking["date"] == day.isoformat()
    ]
    return sorted(schedule, key=lambda booking: get_period(booking)[0])


def find_free_rooms(rooms: list[dict], bookings: list[dict],
                    request: dict) -> list[dict]:
    """Подбирает помещения, в которых заявку можно одобрить."""
    suitable = []
    for room in filter_rooms(rooms, request["participants"],
                             request["needs_projector"]):
        if check_request(room, bookings, request) == APPROVED:
            suitable.append(room)
    return sort_rooms(suitable)


def get_statistics(rooms: list[dict], bookings: list[dict]) -> dict:
    """Считает количество бронирований, часы и самое загруженное помещение."""
    counts = {room["id"]: 0 for room in rooms}
    hours = 0.0
    for booking in bookings:
        room_id = booking["room_id"]
        counts[room_id] = counts.get(room_id, 0) + 1
        start, end = get_period(booking)
        hours += (end - start).total_seconds() / 3600
    days = {booking["date"] for booking in bookings}
    busiest_id = max(counts, key=counts.get) if bookings else None
    return {
        "total": len(bookings),
        "hours": round(hours, 1),
        "days": len(days),
        "by_room": counts,
        "busiest_id": busiest_id,
    }
