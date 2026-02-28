"""Shared constants and helpers."""

SNOWY_OWL = "snoowl1"
DEFAULT_LAT = 42.52
DEFAULT_LNG = -70.90
DEFAULT_DIST_MILES = 30
DEFAULT_BACK_DAYS = 14


def checklist_url(sub_id: str) -> str:
    """Build an eBird checklist URL."""
    return f"https://ebird.org/checklist/{sub_id}"
