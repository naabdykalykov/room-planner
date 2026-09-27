from datetime import datetime, time

# помещение
ROOM_NAME = "Конференц-зал Сириус"
ROOM_CAPACITY = 40
ROOM_HAS_PROJECTOR = True
ROOM_OPENS = time(8, 30)
ROOM_CLOSES = time(21, 0)

# мероприятие, которое уже есть в расписании
BOOKED_TITLE = "Защита курсовых проектов"
BOOKED_START = datetime(2026, 10, 15, 10, 0)
BOOKED_END = datetime(2026, 10, 15, 12, 30)


def parse_datetime(date_text, time_text):
    return datetime.strptime(date_text + " " + time_text, "%d.%m.%Y %H:%M")


def check_capacity(participants, capacity):
    return participants <= capacity


def get_occupancy_percent(participants, capacity):
    return round(participants / capacity * 100, 1)


def check_working_hours(start, end, opens, closes):
    return opens <= start.time() < end.time() <= closes


def has_time_conflict(start, end, booked_start, booked_end):
    # интервалы пересекаются, если каждый начинается раньше конца другого
    return start < booked_end and booked_start < end


def check_equipment(needs_projector, has_projector):
    return has_projector or not needs_projector


def get_decision(in_hours, conflict, fits, equipped):
    if not in_hours:
        return "отклонена: время вне часов работы помещения"
    elif conflict:
        return "отклонена: в это время помещение занято"
    elif not fits:
        return "отклонена: не хватает мест"
    elif not equipped:
        return "отклонена: в помещении нет проектора"
    else:
        return "одобрена"


def check_request(title, date_text, start_text, end_text,
                  participants_text, projector_answer):
    # данные заявки приходят строками, переводим их в нужные типы
    start = parse_datetime(date_text, start_text)
    end = parse_datetime(date_text, end_text)
    participants = int(participants_text)
    needs_projector = projector_answer.lower() == "да"

    in_hours = check_working_hours(start, end, ROOM_OPENS, ROOM_CLOSES)
    conflict = has_time_conflict(start, end, BOOKED_START, BOOKED_END)
    fits = check_capacity(participants, ROOM_CAPACITY)
    equipped = check_equipment(needs_projector, ROOM_HAS_PROJECTOR)
    percent = get_occupancy_percent(participants, ROOM_CAPACITY)
    decision = get_decision(in_hours, conflict, fits, equipped)

    print(f"Заявка: {title}")
    print(f"  Когда: {date_text}, {start_text}-{end_text}")
    print(f"  Участников: {participants} (заполненность {percent}%)")
    print(f"  Нужен проектор: {projector_answer}")
    print(f"  Решение: {decision}")
    print()


def main():
    print("Сервис планирования использования помещений")
    print()
    print(f"Помещение: {ROOM_NAME}, мест: {ROOM_CAPACITY}")
    if ROOM_HAS_PROJECTOR:
        print("Оснащение: есть проектор")
    else:
        print("Оснащение: проектора нет")
    opens = ROOM_OPENS.strftime("%H:%M")
    closes = ROOM_CLOSES.strftime("%H:%M")
    print(f"Часы работы: {opens}-{closes}")
    booked_day = BOOKED_START.strftime("%d.%m.%Y")
    booked_from = BOOKED_START.strftime("%H:%M")
    booked_to = BOOKED_END.strftime("%H:%M")
    print(f"Уже в расписании: {BOOKED_TITLE}")
    print(f"  {booked_day}, {booked_from}-{booked_to}")
    print()

    check_request(
        title="Семинар по Python",
        date_text="15.10.2026",
        start_text="12:40",
        end_text="14:10",
        participants_text="32",
        projector_answer="да",
    )
    check_request(
        title="Встреча клуба робототехники",
        date_text="15.10.2026",
        start_text="11:30",
        end_text="13:00",
        participants_text="25",
        projector_answer="нет",
    )


if __name__ == "__main__":
    main()
