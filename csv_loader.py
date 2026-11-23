import csv
import os
from validator import validate_row, to_record


def parse_files(paths: list[str], airports: set[str]) -> tuple[list[dict], list[str]]:
    records = []
    errors = []
    used = set()

    for path in paths:
        with open(path, encoding="utf-8", newline="") as file:
            for line_number, line in enumerate(file, 1):
                if line_number == 1 or not line.strip() or line.lstrip().startswith("#"):
                    continue

                fields = next(csv.reader([line]))
                error = validate_row(fields, airports)
                if error is None:
                    flight = to_record(fields)
                    key = (flight["flight_id"], flight["departure_datetime"])
                    if key in used:
                        error = "DUPLICATE_FLIGHT"
                    else:
                        used.add(key)
                        records.append(flight)

                if error is not None:
                    name = os.path.basename(path)
                    original = line.rstrip("\r\n")
                    errors.append(f"{name}:{line_number}: {error} | {original}")

    return records, errors
