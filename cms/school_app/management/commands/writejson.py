import decimal
import gzip
import json
import os
import time

import brotli
from django.core.management.base import BaseCommand
from school_app.models import School

# Make Decimals JSON-serializable
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Generating JSON...")
        now = time.time()
        try:
            os.mkdir("json")
        except FileExistsError:
            # Folder already exists
            pass
        # Write new files next to the old ones, then atomically replace
        with open("json/coords.json.tmp", "w", encoding="utf-8") as f:
            records = list(
                School.objects.filter(lat__isnull=False, lon__isnull=False)
                .values("id", "lat", "lon")
                .iterator()
            )
            count = len(records)
            f.write(DecimalEncoder(separators=(",", ":")).encode(records))
        self.stdout.write(
            self.style.SUCCESS(
                f"Wrote {count} records in {round(time.time()-now, 3)} seconds"
            )
        )
        # Generate compressed versions
        with open("json/coords.json.tmp", "rb") as f:
            data = f.read()
            # gzip
            self.stdout.write("Compressing with gzip...")
            now = time.time()
            with gzip.open("json/coords.json.gz.tmp", "wb") as g:
                g.write(data)
            self.stdout.write(
                self.style.SUCCESS(f"Finished in {round(time.time()-now, 3)} seconds")
            )
            # brotli
            self.stdout.write("Compressing with brotli...")
            now = time.time()
            with open("json/coords.json.br.tmp", "wb") as b:
                b.write(brotli.compress(data, mode=brotli.MODE_TEXT))
            self.stdout.write(
                self.style.SUCCESS(f"Finished in {round(time.time()-now, 3)} seconds")
            )
        # Replace
        os.replace("json/coords.json.tmp", "json/coords.json")
        os.replace("json/coords.json.gz.tmp", "json/coords.json.gz")
        os.replace("json/coords.json.br.tmp", "json/coords.json.br")
