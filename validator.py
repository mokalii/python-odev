import math
import re
from datetime import datetime


def load_airports(path: str) -> set[str]:
    airports = set()
    with open(path, encoding="utf-8") as file:
        for line in file:
            code = line.strip()
            if code and not code.startswith("#"):
                airports.add(code)
    return airports


def valid_datetime(value: str) -> bool:
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}", value):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False


def validate_row(fields: list[str], airports: set[str]) -> str | None:
    if len(fields) != 6:
        return "WRONG_FIELD_COUNT"

    flight_id, origin, destination, departure, arrival, price = [f.strip() for f in fields]
    if not all([flight_id, origin, destination, departure, arrival, price]):
        return "MISSING_FIELD"
    if not re.fullmatch(r"[A-Za-z0-9]{2,8}", flight_id):
        return "INVALID_FLIGHT_ID"
    if not re.fullmatch(r"[A-Z]{3}", origin) or origin not in airports:
        return "INVALID_ORIGIN"
    if not re.fullmatch(r"[A-Z]{3}", destination) or destination not in airports:
        return "INVALID_DESTINATION"
    if origin == destination:
        return "SAME_ORIGIN_DESTINATION"
    if not valid_datetime(departure):
        return "INVALID_DEPARTURE"
    if not valid_datetime(arrival):
        return "INVALID_ARRIVAL"

    start = datetime.strptime(departure, "%Y-%m-%d %H:%M")
    end = datetime.strptime(arrival, "%Y-%m-%d %H:%M")
    if end <= start:
        return "ARRIVAL_NOT_AFTER_DEPARTURE"

    try:
        number = float(price)
    except (ValueError, OverflowError):
        return "INVALID_PRICE"
    if not math.isfinite(number):
        return "INVALID_PRICE"
    if number <= 0:
        return "NON_POSITIVE_PRICE"
    return None


def to_record(fields: list[str]) -> dict:
    flight_id, origin, destination, departure, arrival, price = [f.strip() for f in fields]
    return {
        "flight_id": flight_id,
        "origin": origin,
        "destination": destination,
        "departure_datetime": departure,
        "arrival_datetime": arrival,
        "price": float(price)
    }
