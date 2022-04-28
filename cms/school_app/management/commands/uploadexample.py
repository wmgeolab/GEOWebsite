from django.core.management.base import BaseCommand
from school_app.models import SchoolV2, SchoolV2Session

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
