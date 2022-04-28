import csv

from django.core.management.base import BaseCommand
from school_app.models import SchoolV2, SchoolV2Session

# Example management command to add a single record to the database
# Run with `python manage.py uploadexample <filename>`


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("filename")

    def handle(self, *args, **options):
        with open(options["filename"], "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            line_count = 0
            country = "Mexico"  # Hardcode for now
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
