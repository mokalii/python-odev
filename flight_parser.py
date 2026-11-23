import argparse
import json
import logging
import os
import sys
from datetime import datetime
from csv_loader import parse_files
from query import run_queries
from validator import load_airports


STUDENT_ID= "251ADB185"
FIRST_NAME= "AliBerk"
LAST_NAME= "Cetin"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Flight query program")
    sources = parser.add_mutually_exclusive_group(required=True)
    sources.add_argument("-i", metavar="FILE")
    sources.add_argument("-d", metavar="FOLDER")
    sources.add_argument("-j", metavar="FILE")
    parser.add_argument("-a", metavar="FILE")
    parser.add_argument("-o", metavar="FILE")
    parser.add_argument("-q", metavar="FILE")
    parser.add_argument("-r", metavar="FOLDER", default=".")

    try:
        args = parser.parse_args(argv)
        if (args.i or args.d) and not args.a:
            parser.error("-a is required with -i or -d")
        if args.j and args.o is not None:
            parser.error("-o cannot be used with -j")
    except SystemExit as error:
        return error.code

    logger = logging.getLogger("flight_parser")
    logger.setLevel(logging.INFO)
    handler = None

    try:
        if args.j:
            with open(args.j, encoding="utf-8") as file:
                db = json.load(file)
            if not isinstance(db, list) or not all(isinstance(row, dict) for row in db):
                raise ValueError("JSON database must be a list of objects")
        else:
            airports= load_airports(args.a)
            if args.i:
                paths =[args.i]
            else:
                paths =[]
                for name in sorted(os.listdir(args.d)):
                    path= os.path.join(args.d, name)
                    if name.endswith(".csv") and os.path.isfile(path):
                        paths.append(path)
                if not paths:
                    raise ValueError("No CSV files found")

            db_path= args.o if args.o is not None else "db.json"
            log_path =os.path.join(os.path.dirname(db_path) or ".", "errors.log")
            handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
            handler.setFormatter(logging.Formatter(
                "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            ))
            logger.addHandler(handler)

            db, errors =parse_files(paths, airports)
            with open(db_path, "w", encoding="utf-8") as file:
                json.dump(db, file, indent=2)
            for error in errors:
                logger.warning(error)

        if args.q:
            with open(args.q, encoding="utf-8") as file:
                queries = json.load(file)
            if not isinstance(queries, (dict, list)):
                raise ValueError("Queries must be an object or list")
            if isinstance(queries, list) and not all(isinstance(q, dict) for q in queries):
                raise ValueError("Every query must be an object")

            results = run_queries(db, queries)
            date= datetime.now().strftime("%Y%m%d_%H%M")
            name =f"response_{STUDENT_ID}_{FIRST_NAME}_{LAST_NAME}_{date}.json"
            with open(os.path.join(args.r, name), "w", encoding="utf-8") as file:
                json.dump(results, file, indent=2, allow_nan=False)
        return 0

    except (OSError, UnicodeError, ValueError, TypeError, OverflowError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    finally:
        if handler is not None:
            logger.removeHandler(handler)
            handler.close()


if __name__ == "__main__":
    sys.exit(main())
