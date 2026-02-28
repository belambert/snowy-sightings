"""CLI for checking recent snowy owl sightings."""

import os
import sys
from pathlib import Path

import typer

from snowy_sightings.check import check_new
from snowy_sightings.config import (
    DEFAULT_BACK_DAYS,
    DEFAULT_DIST_MILES,
    DEFAULT_LAT,
    DEFAULT_LNG,
    SNOWY_OWL,
    checklist_url,
)
from snowy_sightings.ebird import recent_observations
from snowy_sightings.notify import send_email

app = typer.Typer(
    help="Check eBird for recent snowy owl observations.", add_completion=False
)


def _require_api_key(api_key: str) -> str:
    if not api_key:
        typer.echo("Error: set EBIRD_API_KEY env var or pass --api-key")
        sys.exit(1)
    return api_key


def _format_sighting(o: dict) -> str:
    loc = o.get("locName", "Unknown")
    dt = o.get("obsDt", "")
    count = o.get("howMany", "?")
    url = checklist_url(o["subId"]) if "subId" in o else ""
    lines = [f"  {dt}  {count:>3} bird(s)  {loc}"]
    if url:
        lines.append(f"    {url}")
    return "\n".join(lines)


@app.command()
def sightings(
    lat: float = typer.Option(DEFAULT_LAT, help="Latitude (default: Salem, MA)"),
    lng: float = typer.Option(DEFAULT_LNG, help="Longitude (default: Salem, MA)"),
    dist: int = typer.Option(DEFAULT_DIST_MILES, help="Search radius in miles"),
    days: int = typer.Option(DEFAULT_BACK_DAYS, help="Days back to search (max 30)"),
    api_key: str = typer.Option("", envvar="EBIRD_API_KEY", help="eBird API key"),
):
    """Show recent snowy owl observations near a location."""
    _require_api_key(api_key)

    dist_km = round(dist * 1.60934)
    obs = recent_observations(api_key, SNOWY_OWL, lat, lng, dist_km, days)
    if not obs:
        typer.echo("No snowy owl sightings found.")
        return

    typer.echo(f"Found {len(obs)} snowy owl sighting(s):\n")
    for o in obs:
        typer.echo(_format_sighting(o))


@app.command()
def check(
    to: str = typer.Option(..., help="Recipient email address"),
    state_file: Path = typer.Option(
        ".snowy-state.json", help="Path to state JSON file"
    ),
    lat: float = typer.Option(DEFAULT_LAT, help="Latitude (default: Salem, MA)"),
    lng: float = typer.Option(DEFAULT_LNG, help="Longitude (default: Salem, MA)"),
    dist: int = typer.Option(DEFAULT_DIST_MILES, help="Search radius in miles"),
    days: int = typer.Option(DEFAULT_BACK_DAYS, help="Days back to search (max 30)"),
    api_key: str = typer.Option("", envvar="EBIRD_API_KEY", help="eBird API key"),
):
    """Check for new snowy owl sightings and send email alerts."""
    _require_api_key(api_key)

    dist_km = round(dist * 1.60934)
    new = check_new(api_key, lat, lng, dist_km, days, state_file)

    if not new:
        typer.echo("No new snowy owl sightings.")
        return

    typer.echo(f"Found {len(new)} new snowy owl sighting(s):\n")
    for o in new:
        typer.echo(_format_sighting(o))

    # build and send email
    rows = "".join(
        f"<tr><td>{o.get('obsDt', '')}</td>"
        f"<td>{o.get('howMany', '?')}</td>"
        f"<td>{o.get('locName', 'Unknown')}</td>"
        f"<td><a href='{checklist_url(o['subId'])}'>checklist</a></td></tr>"
        for o in new
        if o.get("subId")
    )
    html = (
        f"<h2>🦉 {len(new)} new snowy owl sighting(s)!</h2>"
        f"<table><tr><th>Date</th><th>Count</th><th>Location</th><th>Link</th></tr>"
        f"{rows}</table>"
    )
    send_email(to, f"🦉 {len(new)} new snowy owl sighting(s)", html)
    typer.echo("Email sent.")


if __name__ == "__main__":
    app()
