"""New-sighting detection with persistent state."""

import json
from pathlib import Path

from snowy_sightings.config import SNOWY_OWL
from snowy_sightings.ebird import recent_observations


def load_seen(path: Path) -> set[str]:
    """Load previously seen subIds from a JSON file."""
    if not path.exists():
        return set()
    return set(json.loads(path.read_text()))


def save_seen(path: Path, sub_ids: set[str]) -> None:
    """Save current subIds to JSON."""
    path.write_text(json.dumps(sorted(sub_ids)))


def check_new(
    api_key: str,
    lat: float,
    lng: float,
    dist_km: int,
    back_days: int,
    state_file: Path,
) -> list[dict]:
    """Fetch observations, diff against saved state, return new ones."""
    obs = recent_observations(api_key, SNOWY_OWL, lat, lng, dist_km, back_days)
    seen = load_seen(state_file)

    new = [o for o in obs if o.get("subId") and o["subId"] not in seen]

    # update state with all current subIds
    all_ids = seen | {o["subId"] for o in obs if o.get("subId")}
    save_seen(state_file, all_ids)

    return new
