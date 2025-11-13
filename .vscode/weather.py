#!/usr/bin/env python3
"""Fetch and display weather information using the Open-Meteo public API."""

from __future__ import annotations

import argparse
import json
import math
import sys
import textwrap
import urllib.error
import urllib.parse
import urllib.request
import ssl
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
USER_AGENT = "PyPracticeWeather/1.0"


@dataclass(frozen=True)
class Location:
    """Simple data holder for a resolved location."""

    name: str
    country: str
    latitude: float
    longitude: float


def _request_json(
    url: str, params: Dict[str, Any], *, context: ssl.SSLContext | None = None
) -> Dict[str, Any]:
    """Perform a GET request and decode JSON, raising a RuntimeError on issues."""
    query = urllib.parse.urlencode(params)
    req = urllib.request.Request(f"{url}?{query}", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10, context=context) as response:
            if response.status != 200:
                raise RuntimeError(f"API call failed with HTTP {response.status}")
            return json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"API call failed: {exc}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error: {exc}") from exc


def resolve_location(
    city: str, country: str | None, *, context: ssl.SSLContext | None = None
) -> Location:
    """Use the Open-Meteo geocoding API to resolve the city into coordinates."""
    params = {"name": city, "count": 1, "language": "en", "format": "json"}
    if country:
        params["country"] = country
    payload = _request_json(GEOCODE_URL, params, context=context)
    results = payload.get("results") or []
    if not results:
        raise RuntimeError(f"No results found for '{city}'")
    result = results[0]
    return Location(
        name=result.get("name", city),
        country=result.get("country", "Unknown"),
        latitude=result["latitude"],
        longitude=result["longitude"],
    )


def fetch_weather(
    location: Location, *, context: ssl.SSLContext | None = None
) -> Dict[str, Any]:
    """Fetch the current weather for the provided location coordinates."""
    params = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "current": "temperature_2m,apparent_temperature,weather_code,"
        "relative_humidity_2m,wind_speed_10m",
        "hourly": "temperature_2m",
        "timezone": "auto",
    }
    return _request_json(WEATHER_URL, params, context=context)


def c_to_f(temp_c: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return temp_c * 9 / 5 + 32


def format_report(
    location: Location,
    weather: Dict[str, Any],
    *,
    imperial: bool,
    hourly_preview: int,
) -> str:
    """Build a display string summarizing the fetched weather."""
    current = weather.get("current", {})
    temperature = current.get("temperature_2m")
    apparent = current.get("apparent_temperature")
    humidity = current.get("relative_humidity_2m")
    wind = current.get("wind_speed_10m")
    weather_code = current.get("weather_code")
    units = weather.get("current_units", {})

    if imperial and temperature is not None:
        temperature = c_to_f(temperature)
        apparent = c_to_f(apparent) if apparent is not None else None
        temp_unit = "°F"
    else:
        temp_unit = units.get("temperature_2m", "°C")

    wind_unit = units.get("wind_speed_10m", "km/h")
    humidity_unit = units.get("relative_humidity_2m", "%")

    lines = [
        f"Weather for {location.name}, {location.country}",
        "-" * 40,
    ]

    def _fmt(value: Any, unit: str) -> str:
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return "N/A"
        return f"{value:.1f}{unit}"

    lines.append(f"Temperature:        {_fmt(temperature, temp_unit)}")
    lines.append(f"Feels like:         {_fmt(apparent, temp_unit)}")
    lines.append(f"Humidity:           {_fmt(humidity, humidity_unit)}")
    lines.append(f"Wind speed:         {_fmt(wind, wind_unit)}")
    lines.append(f"Weather code:       {weather_code if weather_code is not None else 'N/A'}")

    if hourly_preview > 0:
        hourly = weather.get("hourly", {})
        timestamps = hourly.get("time", [])
        temps = hourly.get("temperature_2m", [])
        preview_lines = ["\nNext hours:"]
        for ts, temp in list(zip(timestamps, temps))[:hourly_preview]:
            try:
                timestamp = datetime.fromisoformat(ts)
                stamp = timestamp.strftime("%a %H:%M")
            except ValueError:
                stamp = ts
            if imperial:
                temp = c_to_f(temp)
            preview_lines.append(f"  {stamp}: {temp:.1f}{temp_unit}")
        lines.extend(preview_lines)

    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch weather from Open-Meteo for a given city.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """Examples:
            weather.py London
            weather.py --country US \"New York\" --hourly 4 --imperial
            """
        ),
    )
    parser.add_argument(
        "city",
        nargs="*",
        help="City name to search for (use quotes for multi-word names).",
    )
    parser.add_argument(
        "--country",
        help="Restrict the search to a specific ISO country code (e.g. US, GB).",
    )
    parser.add_argument(
        "--hourly",
        type=int,
        default=0,
        help="Show an hourly temperature preview for the next N hours.",
    )
    parser.add_argument(
        "--imperial",
        action="store_true",
        help="Display temperatures in Fahrenheit instead of Celsius.",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable SSL certificate validation (not recommended).",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    city = " ".join(args.city).strip()
    if not city:
        city = input("Enter city name: ").strip()
    if not city:
        print("Error: city name is required.", file=sys.stderr)
        return 2
    context = None
    if args.insecure:
        context = ssl._create_unverified_context()
    try:
        location = resolve_location(city, args.country, context=context)
        weather = fetch_weather(location, context=context)
        report = format_report(
            location,
            weather,
            imperial=args.imperial,
            hourly_preview=max(0, args.hourly),
        )
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
