import math
from validator import valid_datetime


FIELDS = {"flight_id", "origin", "destination", "departure_datetime", "arrival_datetime", "price"}
ALLOWED = FIELDS | {"min_price", "sort_by", "order", "limit"}


def valid_query(query: dict) -> bool:
    if not isinstance(query, dict):
        return False

    for key, value in query.items():
        if key not in ALLOWED:
            return False
        if key in ("flight_id", "origin", "destination"):
            if not isinstance(value, str):
                return False
        elif key in ("departure_datetime", "arrival_datetime"):
            if not isinstance(value, str) or not valid_datetime(value):
                return False
        elif key in ("price", "min_price"):
            if type(value) not in (int, float):
                return False
            if type(value) is float and not math.isfinite(value):
                return False
        elif key == "sort_by":
            if not isinstance(value, str) or value not in FIELDS:
                return False
        elif key == "order":
            if value not in ("asc", "desc"):
                return False
        elif key == "limit":
            if type(value) is not int or value < 0:
                return False

    if "order" in query and "sort_by" not in query:
        return False
    return True


def run_query(db: list[dict], query: dict) -> dict:
    if not valid_query(query):
        return {"query": query, "error": "INVALID_QUERY", "matches": []}

    matches = []
    for flight in db:
        if "flight_id" in query and flight["flight_id"] != query["flight_id"]:
            continue
        if "origin" in query and flight["origin"] != query["origin"]:
            continue
        if "destination" in query and flight["destination"] != query["destination"]:
            continue
        if "departure_datetime" in query and flight["departure_datetime"] < query["departure_datetime"]:
            continue
        if "arrival_datetime" in query and flight["arrival_datetime"] > query["arrival_datetime"]:
            continue
        if "price" in query and flight["price"] > query["price"]:
            continue
        if "min_price" in query and flight["price"] < query["min_price"]:
            continue
        matches.append(flight)

    if "sort_by" in query:
        matches.sort(key=lambda flight: flight[query["sort_by"]], reverse=query.get("order") == "desc")
    if "limit" in query:
        matches = matches[:query["limit"]]
    return {"query": query, "matches": matches}


def run_queries(db: list[dict], queries: dict | list) -> list[dict]:
    if isinstance(queries, dict):
        queries = [queries]
    results = []
    for query in queries:
        results.append(run_query(db, query))
    return results
