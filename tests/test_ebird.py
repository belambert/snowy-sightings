from unittest.mock import patch

from snowy_sightings.ebird import recent_observations

FAKE_OBS = [
    {"locName": "Plum Island", "obsDt": "2026-02-20 10:00", "howMany": 2},
    {"locName": "Salisbury Beach", "obsDt": "2026-02-19 14:30", "howMany": 1},
]


def test_recent_observations():
    mock_resp = type("R", (), {"status_code": 200, "json": lambda self: FAKE_OBS})()
    mock_resp.raise_for_status = lambda: None

    with patch("snowy_sightings.ebird.httpx.get", return_value=mock_resp) as mock_get:
        result = recent_observations("fake-key", "snoowl1", 42.36, -71.06)

    assert len(result) == 2
    assert result[0]["locName"] == "Plum Island"
    mock_get.assert_called_once()
