from django.core.management.base import BaseCommand
from school_app.models import SchoolV2, SchoolV2Session
import csv

# Example management command to add a single record to the database
# Run with `python manage.py uploadexample`

# Sample record to insert:
# Year: 2000
# SchoolID: TEST001
# Country: Imaginaryland
# SchoolName: Test School Please Ignore
# Latitude: 90
# Longitude: 0
# Session: Morning
# Enrollment: 1
# TestScore: 50


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("filename")

    def handle(self, *args, **options):
        csv_object = import_csv(options["filename"])


def import_csv(filename):
    with open(filename, "r", encoding="utf-8") as fil:
        reader = csv.reader(fil, delimiter=",")
        line_count = 0
        # initialize a dictionary with column names as keys
        headers = []
        headers = next(reader)
        header_dict = {}
        for header in headers:
            header_dict[header] = None
        print(header_dict)
        # get country name since every entry will be from the same country's csv
        for char in range(0, len(filename) - 1):
            if filename[char] == "/" or filename[char] == "\\":
                # get the index of the last slash in the path
                last_slash_idx = char
        # slice the filename string to get name of file apart from the file type (ex: .csv)
        country = filename[(last_slash_idx + 1) : len(filename) - 4]
        for row in reader:
            results = header_dict
            counter = 0
            for result in results:
                if len(row[counter]) == 0:
                    results[result] = None
                else:
                    results[result] = row[counter]
                counter += 1
            line_count += 1
            print(results)
            try:
                # Get the school object if it already exists
                # SchoolID is not globally unique but is unique within a country
                school = SchoolV2.objects.get(
                    country=country, school_id=results["SchoolID"]
                )
            except SchoolV2.DoesNotExist:
                # Create the school object if it doesn't exist
                school = SchoolV2(
                    country=country,
                    school_id=results["SchoolID"],
                    school_name=results["SchoolName"],
                    municipality=results["Municipality"],
                    lat=results["Latitude"],
                    lon=results["Longitude"],
                )
                # Write object from memory to the database
                school.save()

            session = SchoolV2Session(
                school=school,
                data_year=results["year"],
                session=results["Session"],
                total_enrollment=int(float(results["No.StudentsEval"])),
                test_score=results["total_score"],
            )
            # Write object from memory to the database
            session.save()

        print(f"Processed {line_count} lines.")

    return results
