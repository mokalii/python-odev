# Flight Query Tool

This is a simple Python program for checking flight CSV files and finding flights from a JSON database.

Needs Python 3.13. No extra libraries.

## Commands

```bash
python3 flight_parser.py -i data/db.csv -a data/airports.txt -q data/query.json
python3 flight_parser.py -d data -a data/airports.txt
python3 flight_parser.py -j db.json -q data/query.json
```

The program saves correct flights in `db.json` and wrong rows in `errors.log`.
Queries are saved in a `response_...json` file.

Before submitting: put your student ID in `flight_parser.py`, add your ChatGPT conversation link in `AI_USAGE.md`, and check the results. Push all required files to GitHub.
