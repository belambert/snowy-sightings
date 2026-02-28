# Snowy Sightings

CLI tool to check for recent snowy owl observations using the eBird API.

## Setup

    uv sync
    export EBIRD_API_KEY=your-key-here

Get an API key by signing up at https://ebird.org/api/keygen.

## Usage

    uv run snowy

Defaults to Salem, MA with a 30-mile radius over the last 14 days. Override with options:

    uv run snowy --lat 40.71 --lng -74.01 --dist 50 --days 30

## eBird API

This tool uses the [eBird API 2.0](https://documenter.getpostman.com/view/664302/S1ENwy59) endpoint `GET /v2/data/obs/geo/recent/{speciesCode}` to fetch recent nearby observations of a species.

### Request Parameters

| Parameter | Description |
|-----------|-------------|
| `lat` | Latitude |
| `lng` | Longitude |
| `dist` | Search radius in km (max 50) |
| `back` | Number of days back to search (max 30) |

Authentication is via the `X-eBirdApiToken` header.

### Response Fields

Each observation is returned as a JSON object with these fields:

| Field | Description |
|-------|-------------|
| `speciesCode` | eBird species code (e.g. `snoowl1`) |
| `comName` | Common name (e.g. "Snowy Owl") |
| `sciName` | Scientific name |
| `locName` | Location name |
| `obsDt` | Observation date and time |
| `howMany` | Number of birds observed |
| `lat` | Latitude of observation |
| `lng` | Longitude of observation |
| `subId` | Checklist submission ID (e.g. `S304358788`) |

Checklist URLs can be constructed as `https://ebird.org/checklist/{subId}`.

## References

- [eBird API 2.0 Documentation (Postman)](https://documenter.getpostman.com/view/664302/S1ENwy59)
- [eBird API Key Registration](https://ebird.org/api/keygen)
- [eBird API Tutorial - Eric Nost](http://ericnost.github.io/digitalconservation_ebirdapi.html)
- [ebird-api Python Package (PyPI)](https://pypi.org/project/ebird-api/)
- [rebird R Client - Response Field Documentation](https://docs.ropensci.org/rebird/reference/ebirdnotable.html)
- [ProjectBabbler/ebird-api (GitHub)](https://github.com/ProjectBabbler/ebird-api)
