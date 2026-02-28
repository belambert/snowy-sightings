"""CLI for checking recent snowy owl sightings."""

import os
import sys

import typer

from snowy_sightings.ebird import recent_observations

SNOWY_OWL = "snoowl1"

app = typer.Typer(help="Check eBird for recent snowy owl observations.", add_completion=False)


@app.command()
def sightings(
    lat: float = typer.Option(42.52, help="Latitude (default: Salem, MA)"),
    lng: float = typer.Option(-70.90, help="Longitude (default: Salem, MA)"),
    dist: int = typer.Option(30, help="Search radius in miles"),
    days: int = typer.Option(14, help="Days back to search (max 30)"),
    api_key: str = typer.Option("", envvar="EBIRD_API_KEY", help="eBird API key"),
):
    """Show recent snowy owl observations near a location."""
    if not api_key:
        typer.echo("Error: set EBIRD_API_KEY env var or pass --api-key")
        sys.exit(1)

    dist_km = round(dist * 1.60934)
    obs = recent_observations(api_key, SNOWY_OWL, lat, lng, dist_km, days)
    if not obs:
        typer.echo("No snowy owl sightings found.")
        return

    typer.echo(f"Found {len(obs)} snowy owl sighting(s):\n")
    for o in obs:
        loc = o.get("locName", "Unknown")
        dt = o.get("obsDt", "")
        count = o.get("howMany", "?")
        typer.echo(f"  {dt}  {count:>3} bird(s)  {loc}")


if __name__ == "__main__":
    app()
