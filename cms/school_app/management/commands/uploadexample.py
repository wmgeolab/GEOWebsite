import csv

from django.core.management.base import BaseCommand
from school_app.models import SchoolV2, SchoolV2Session

# Example management command to add a single record to the database
# Run with `python manage.py uploadexample <filename>`

# Inserting records one-by-one creates a new transaction for each record, which
# gets very slow for 1,000+ records.
# Solution: First, loop through and add every School to a list and insert into the
# database in a single transaction with buik_create(). The database enforces uniqueness
# so we can just catch IntegrityError and pass.
# Then, do a second pass to add each Session. School lookups are fast because they are
# indexed and cached. Insert with bulk_create().


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("filename")

    def handle(self, *args, **options):
        with open(options["filename"], "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            country = "Mexico"  # Hardcode for now

            schoolList = [
                SchoolV2(
                    country=country,
                    school_id=row["SchoolID"],
                    school_name=row["SchoolName"],
                    municipality=row["Municipality"],
                    lat=row["Latitude"]
                    if row["Latitude"] and row["Longitude"]
                    else None,
                    lon=row["Longitude"]
                    if row["Latitude"] and row["Longitude"]
                    else None,
                )
                for row in reader
            ]
            SchoolV2.objects.bulk_create(schoolList, ignore_conflicts=True)

            file.seek(0)

            """
            for row in reader:
                if row["Latitude"] == "" or row["Longitude"] == "":
                    row["Latitude"] = None
                    row["Longitude"] = None

                school, _ = SchoolV2.objects.get_or_create(
                    country=country,
                    school_id=row["SchoolID"],
                    defaults={
                        "school_name": row["SchoolName"],
                        "municipality": row["Municipality"],
                        "lat": row["Latitude"],
                        "lon": row["Longitude"],
                    },
                )

                _, created = SchoolV2Session.objects.get_or_create(
                    school=school,
                    data_year=row["year"],
                    session=row["Session"],
                    total_enrollment=int(float(row["No.StudentsEval"])),
                    test_score=row["total_score"],
                )

                if created:
                    line_count += 1
            self.stdout.write(f"Processed {line_count} new lines.")
            """
