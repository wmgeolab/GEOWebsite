import csv

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


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("filename", help="path to the CSV to upload")
        parser.add_argument("country", help="name of the country")

    def handle(self, *args, **options):
        with open(options["filename"], "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            country = options["country"]

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
            SchoolV2.objects.bulk_create(schoolList, ignore_conflicts=True)

            file.seek(0)  # Return to beginning of file
            next(reader)  # Skip the header row

            sessionList = [
                SchoolV2Session(
                    school=SchoolV2.objects.get(
                        country=country,
                        school_id=row["school_id"],
                    ),
                    session=row["session"] if "session" in row else "",
                    data_year=row["data_year"]
                    if "data_year" in row and row["data_year"]
                    else None,
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
                for row in reader
            ]
            inserted = SchoolV2Session.objects.bulk_create(
                sessionList, ignore_conflicts=True
            )
            self.stdout.write(f"Processed {len(inserted)} records.")
