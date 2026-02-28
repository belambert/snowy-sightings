"""eBird API client for fetching recent observations."""

import httpx

BASE_URL = "https://api.ebird.org/v2"


def recent_observations(
    api_key: str,
    species_code: str,
    lat: float,
    lng: float,
    dist_km: int = 50,
    back_days: int = 14,
) -> list[dict]:
    """Fetch recent observations of a species near a location."""
    resp = httpx.get(
        f"{BASE_URL}/data/obs/geo/recent/{species_code}",
        headers={"X-eBirdApiToken": api_key},
        params={"lat": lat, "lng": lng, "dist": dist_km, "back": back_days},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()
