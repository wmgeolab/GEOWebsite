import os
import csv
import time
from django.core.management.base import BaseCommand
from school_app.models import School


class Command(BaseCommand):
    def handle(self, *args, **options):
        now = time.time()
        count = 0
        try:
            os.mkdir('csv')
        except OSError:
            # Folder already exists
            pass
        with open('csv/schools.csv', 'w', encoding='utf-8-sig') as f:
            field_names = School._meta.fields
            field_names = [str(field).split('.')[-1] for field in field_names]
            writer = csv.DictWriter(f, field_names)
            writer.writeheader()
            for obj in School.objects.all().values().iterator():
                writer.writerow(obj)
                count += 1
        self.stdout.write(self.style.SUCCESS(
            f'Wrote {count} records in {round(time.time()-now, 3)} seconds'))
