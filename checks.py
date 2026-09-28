from datetime import datetime, time

APPROVED = "одобрена"


def check_capacity(participants: int, capacity: int) -> bool:
    return participants <= capacity


def get_occupancy_percent(participants: int, capacity: int) -> float:
    return round(participants / capacity * 100, 1)


def check_working_hours(start: datetime, end: datetime,
                        opens: time, closes: time) -> bool:
    return opens <= start.time() < end.time() <= closes


def has_time_conflict(start: datetime, end: datetime,
                      booked_start: datetime, booked_end: datetime) -> bool:
    return start < booked_end and booked_start < end


def check_equipment(needs_projector: bool, has_projector: bool) -> bool:
    return has_projector or not needs_projector


def get_decision(in_hours: bool, conflict: bool, fits: bool,
                 equipped: bool) -> str:
    if not in_hours:
        return "отклонена: время вне часов работы помещения"
    elif conflict:
        return "отклонена: в это время помещение занято"
    elif not fits:
        return "отклонена: не хватает мест"
    elif not equipped:
        return "отклонена: в помещении нет проектора"
    else:
        return APPROVED
