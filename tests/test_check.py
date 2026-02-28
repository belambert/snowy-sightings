import json
from pathlib import Path
from unittest.mock import patch

from snowy_sightings.check import check_new, load_seen, save_seen

FAKE_OBS = [
    {
        "subId": "S100",
        "locName": "Plum Island",
        "obsDt": "2026-02-20 10:00",
        "howMany": 2,
    },
    {
        "subId": "S101",
        "locName": "Salisbury Beach",
        "obsDt": "2026-02-19 14:30",
        "howMany": 1,
    },
]


def test_load_seen_missing_file(tmp_path):
    assert load_seen(tmp_path / "nope.json") == set()


def test_load_save_roundtrip(tmp_path):
    path = tmp_path / "state.json"
    save_seen(path, {"S1", "S2"})
    assert load_seen(path) == {"S1", "S2"}


def test_check_new_all_new(tmp_path):
    state = tmp_path / "state.json"
    with patch("snowy_sightings.check.recent_observations", return_value=FAKE_OBS):
        new = check_new("key", 42.0, -71.0, 50, 14, state)
    assert len(new) == 2
    assert load_seen(state) == {"S100", "S101"}


def test_check_new_some_seen(tmp_path):
    state = tmp_path / "state.json"
    save_seen(state, {"S100"})
    with patch("snowy_sightings.check.recent_observations", return_value=FAKE_OBS):
        new = check_new("key", 42.0, -71.0, 50, 14, state)
    assert len(new) == 1
    assert new[0]["subId"] == "S101"
    assert load_seen(state) == {"S100", "S101"}


def test_check_new_none_new(tmp_path):
    state = tmp_path / "state.json"
    save_seen(state, {"S100", "S101"})
    with patch("snowy_sightings.check.recent_observations", return_value=FAKE_OBS):
        new = check_new("key", 42.0, -71.0, 50, 14, state)
    assert new == []
