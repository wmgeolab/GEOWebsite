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
        parser.add_argument('filename')

    def handle(self, *args, **options):
        try:
            # Get the school object if it already exists
            # SchoolID is not globally unique but is unique within a country
            school = SchoolV2.objects.get(country="Imaginaryland", school_id="TEST001")
        except SchoolV2.DoesNotExist:
            # Create the school object if it doesn't exist
            school = SchoolV2(
                country="Imaginaryland",
                school_id="TEST001",
                school_name="Test School Please Ignore",
                lat=90,
                lon=0,
            )
            # Write object from memory to the database
            school.save()

        print(options['filename'])
        # Create the session under the school
        session = SchoolV2Session(
            school=school,
            data_year=2000,
            session="Morning",
            total_enrollment=1,
            test_score=50,
        )
        # Write object from memory to the database
        session.save()

        import_csv(options['filename'])

    
def import_csv(filename):
    with open(filename, "r", encoding="utf-8") as fil:
        reader = csv.reader(fil, delimiter=',')
        line_count = 0
        for row in reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t{row[0]}, {row[1]}, {row[2]}.')
                line_count += 1
        print(f'Processed {line_count} lines.')

