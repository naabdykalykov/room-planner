from storage import load_data, save_data


def test_save_and_load(tmp_path):
    path = tmp_path / "rooms.json"
    rooms = [{"id": 1, "name": "Аудитория А-214", "capacity": 30}]
    save_data(path, rooms)
    assert load_data(path) == rooms


def test_missing_file_gives_empty_list(tmp_path):
    assert load_data(tmp_path / "no_file.json") == []
