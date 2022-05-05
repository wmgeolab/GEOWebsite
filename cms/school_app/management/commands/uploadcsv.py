import csv
from concurrent.futures import ThreadPoolExecutor, wait

from django.db.models.query import QuerySet
from django.core.management.base import BaseCommand
from school_app.models import SchoolV2, SchoolV2Session

# Example management command to add a single record to the database
# Run with `python manage.py uploadexample <filename> <country>`

# Inserting records one-by-one creates a new transaction for each record, which
# gets very slow for 1,000+ records. It inserted 500 records in ~30 seconds.

# Solution: First, loop through and add every School to a list and insert into the
# database in a single transaction with bulk_create(). The database enforces uniqueness
# so we can just throw everything at it and let it figure it out.
# Then, do a second pass to add each Session. School lookups are fast because they are
# indexed and cached. Insert with bulk_create(). This inserts ~1000 records per second.

# ...until you actually try to insert to the MySQL database, and it bogs down to
# ~50 records per second. Wtf.

# Implemented multithreaded insert. SQLite hates it (set max_workers=1 for that), but
# increases MySQL performance to ~430 records per second.


def make_session(row: dict, schoolQuery: QuerySet, country: str) -> SchoolV2Session:
    return SchoolV2Session(
        school=schoolQuery.get(
            country=country,
            school_id=row["school_id"],
        ),
        session=row["session"] if "session" in row else "",
        data_year=row["data_year"] if "data_year" in row and row["data_year"] else None,
        total_enrollment=int(float(row["total_enrollment"]))
        if "total_enrollment" in row
        else None,
        test_score=row["test_score"]
        if "test_score" in row and row["test_score"]
        else None,
        gender_ratio=row["gender_ratio"]
        if "gender_ratio" in row and row["gender_ratio"]
        else None,
    )


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("filename", help="path to the CSV to upload")
        parser.add_argument("country", help="name of the country")

    def handle(self, *args, **options):
        with open(options["filename"], "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            country = options["country"]
            self.stdout.write("Creating School objects...")
            schoolList = [
                SchoolV2(
                    country=country,
                    school_id=row["school_id"],
                    school_name=row["school_name"],
                    sector=row["sector"] if "sector" in row else "",
                    school_level=row["school_level"] if "school_level" in row else "",
                    municipality=row["municipality"] if "municipality" in row else "",
                    department=row["department"] if "department" in row else "",
                    zone=row["zone"] if "zone" in row else "",
                    address=row["address"] if "address" in row else "",
                    lat=row["latitude"]
                    if "latitude" in row
                    and "longitude" in row
                    and row["latitude"]
                    and row["longitude"]
                    else None,
                    lon=row["longitude"]
                    if "latitude" in row
                    and "longitude" in row
                    and row["latitude"]
                    and row["longitude"]
                    else None,
                )
                for row in reader
            ]
            self.stdout.write("Uploading School objects...")
            SchoolV2.objects.bulk_create(schoolList, ignore_conflicts=True)

            schoolQuery = SchoolV2.objects.filter(country=country)

            file.seek(0)  # Return to beginning of file
            next(reader)  # Skip the header row
            self.stdout.write("Creating Session objects...")
            with ThreadPoolExecutor() as exec:
                futuresList = [
                    exec.submit(make_session, row, schoolQuery, country)
                    for row in reader
                ]
                doneFuturesSet, _ = wait(futuresList)
                sessionList = [future.result() for future in doneFuturesSet]

            self.stdout.write("Uploading Session objects...")
            inserted = SchoolV2Session.objects.bulk_create(
                sessionList, ignore_conflicts=True
            )
            self.stdout.write(self.style.SUCCESS(f"Processed {len(inserted)} records."))
