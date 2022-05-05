import csv
import gzip
import os
import time

import brotli
from django.conf import settings
from django.core.management.base import BaseCommand
from school_app.models import SchoolV2, SchoolV2Session


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Generating CSV...")
        now = time.time()
        try:
            os.mkdir("csv")
        except FileExistsError:
            # Folder already exists
            pass
        # Write new files next to the old ones, then atomically replace
        with open("csv/schools.csv.tmp", "w", encoding="utf-8-sig") as f:
            school_field_names = [
                str(field).split(".")[-1] for field in SchoolV2._meta.fields
            ]
            session_field_names = [
                "sessions__" + str(field).split(".")[-1]
                for field in SchoolV2Session._meta.fields
            ]
            field_names = school_field_names + session_field_names
            field_names.remove("sessions__id")
            field_names.remove("sessions__school")
            query = SchoolV2.objects.all().select_related("school").values(*field_names)
            writer = csv.DictWriter(f, field_names)
            writer.writeheader()
            count = 0
            for obj in query:
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
            # brotli takes a long time, don't bother when testing
            if not settings.DEBUG:
                self.stdout.write("Compressing with brotli...")
                now = time.time()
                with open("csv/schools.csv.br.tmp", "wb") as b:
                    b.write(brotli.compress(data, mode=brotli.MODE_TEXT))
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Finished in {round(time.time()-now, 3)} seconds"
                    )
                )
            else:
                self.stdout.write("Skipping brotli...")
        # Replace
        os.replace("csv/schools.csv.tmp", "csv/schools.csv")
        os.replace("csv/schools.csv.gz.tmp", "csv/schools.csv.gz")
        if not settings.DEBUG:
            os.replace("csv/schools.csv.br.tmp", "csv/schools.csv.br")
