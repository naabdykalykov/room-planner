def get_next_id(objects: list) -> int:
    """Следующий свободный номер в списке объектов."""
    return max((obj.id for obj in objects), default=0) + 1
