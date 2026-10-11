from datetime import date

from models import Check, Item, Result, Room
from storage import (load_checks, load_data, load_items, load_results,
                     load_rooms, save_checks, save_data, save_items,
                     save_results, save_rooms)


def make_objects():
    room = Room(1, "Кабинет 204", 2, "Иванова А. С.")
    item = Item(1, "1001", "Кресло офисное", room, 12, 4500.5,
                date(2022, 3, 15), 7)
    check = Check(1, room, date(2026, 10, 12), "Иванова А. С.")
    result = Result(1, check, item, 12, 10, True)
    return room, item, check, result


def test_missing_file_gives_empty_list(tmp_path):
    assert load_data(tmp_path / "no_file.json") == []
    assert load_rooms(tmp_path / "no_file.json") == []


def test_rooms_round_trip(tmp_path):
    room = make_objects()[0]
    path = tmp_path / "rooms.json"
    save_rooms([room], path)
    loaded = load_rooms(path)
    assert loaded[0].name == "Кабинет 204"
    assert loaded[0].to_data() == room.to_data()


def test_json_keeps_ids_instead_of_objects(tmp_path):
    item = make_objects()[1]
    path = tmp_path / "items.json"
    save_items([item], path)
    assert load_data(path)[0]["room_id"] == 1


def test_items_are_linked_to_rooms(tmp_path):
    room, item, check, result = make_objects()
    path = tmp_path / "items.json"
    save_items([item], path)
    loaded = load_items([room], path)
    assert loaded[0].room is room
    assert loaded[0].purchase_date == date(2022, 3, 15)


def test_item_without_room_is_skipped(tmp_path):
    item = make_objects()[1]
    path = tmp_path / "items.json"
    save_items([item], path)
    assert load_items([], path) == []


def test_results_are_linked_to_checks_and_items(tmp_path):
    room, item, check, result = make_objects()
    save_checks([check], tmp_path / "checks.json")
    save_results([result], tmp_path / "results.json")
    checks = load_checks([room], tmp_path / "checks.json")
    results = load_results(checks, [item], tmp_path / "results.json")
    assert results[0].check is checks[0]
    assert results[0].item is item
    assert results[0].shortage_cost == 9001.0


def test_broken_json_gives_empty_list(tmp_path):
    path = tmp_path / "rooms.json"
    path.write_text("{ это не json", encoding="utf-8")
    assert load_data(path) == []


def test_save_data_writes_readable_text(tmp_path):
    path = tmp_path / "rooms.json"
    save_data(path, [{"name": "Кабинет 204"}])
    assert "Кабинет 204" in path.read_text(encoding="utf-8")
