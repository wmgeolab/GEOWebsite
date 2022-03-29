import os
import csv
import time
import gzip
import brotli
from django.core.management.base import BaseCommand
from school_app.models import School


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Generating CSV...")
        now = time.time()
        count = 0
        try:
            os.mkdir("csv")
        except FileExistsError:
            # Folder already exists
            pass
        # Write new files next to the old ones, then atomically replace
        with open("csv/schools.csv.tmp", "w", encoding="utf-8-sig") as f:
            field_names = School._meta.fields
            field_names = [str(field).split(".")[-1] for field in field_names]
            writer = csv.DictWriter(f, field_names)
            writer.writeheader()
            for obj in School.objects.all().values().iterator():
                writer.writerow(obj)
                count += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"Wrote {count} records in {round(time.time()-now, 3)} seconds"
            )
        )
        # Generate compressed versions
        with open("csv/schools.csv.tmp", "rb") as f:
            data = f.read()
            # gzip
            self.stdout.write("Compressing with gzip...")
            now = time.time()
            with gzip.open("csv/schools.csv.gz.tmp", "wb") as g:
                g.write(data)
            self.stdout.write(
                self.style.SUCCESS(f"Finished in {round(time.time()-now, 3)} seconds")
            )
            # brotli
            self.stdout.write("Compressing with brotli...")
            now = time.time()
            with open("csv/schools.csv.br.tmp", "wb") as b:
                b.write(brotli.compress(data, mode=brotli.MODE_TEXT))
            self.stdout.write(
                self.style.SUCCESS(f"Finished in {round(time.time()-now, 3)} seconds")
            )
        # Replace
        os.replace("csv/schools.csv.tmp", "csv/schools.csv")
        os.replace("csv/schools.csv.gz.tmp", "csv/schools.csv.gz")
        os.replace("csv/schools.csv.br.tmp", "csv/schools.csv.br")
