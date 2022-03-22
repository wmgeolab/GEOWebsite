import os
import csv
import time
import gzip
import brotli
from django.core.management.base import BaseCommand
from school_app.models import School


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Generating CSV...')
        now = time.time()
        count = 0
        try:
            os.mkdir('csv')
        except FileExistsError:
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
        # Generate compressed versions
        with open('csv/schools.csv', 'rb') as f:
            data = f.read()
            # gzip
            self.stdout.write('Compressing with gzip...')
            now = time.time()
            with gzip.open('csv/schools.csv.gz', 'wb') as g:
                g.write(data)
            self.stdout.write(self.style.SUCCESS(
                f'Finished in {round(time.time()-now, 3)} seconds'))
            # brotli
            self.stdout.write('Compressing with brotli...')
            now = time.time()
            with open('csv/schools.csv.br', 'wb') as b:
                b.write(brotli.compress(data, mode=brotli.MODE_TEXT))
            self.stdout.write(self.style.SUCCESS(
                f'Finished in {round(time.time()-now, 3)} seconds'))
