import gzip
import os
import time

import brotli
import simplejson as json
from django.core.management.base import BaseCommand
from school_app.models import School


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
        with open("json/coords.geojson.tmp", "w", encoding="utf-8") as f:
            records = (
                School.objects.filter(lat__isnull=False, lon__isnull=False)
                .values("id", "lat", "lon")
                .iterator()
            )
            features = [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [record["lon"], record["lat"]],
                    },
                    "properties": {"id": record["id"]},
                }
                for record in records
            ]
            count = len(features)
            feature_collection = {"type": "FeatureCollection", "features": features}
            json.dump(feature_collection, f, separators=(",", ":"))
        self.stdout.write(
            self.style.SUCCESS(
                f"Wrote {count} records in {round(time.time()-now, 3)} seconds"
            )
        )
        # Generate compressed versions
        with open("json/coords.geojson.tmp", "rb") as f:
            data = f.read()
            # gzip
            self.stdout.write("Compressing with gzip...")
            now = time.time()
            with gzip.open("json/coords.geojson.gz.tmp", "wb") as g:
                g.write(data)
            self.stdout.write(
                self.style.SUCCESS(f"Finished in {round(time.time()-now, 3)} seconds")
            )
            # brotli
            self.stdout.write("Compressing with brotli...")
            now = time.time()
            with open("json/coords.geojson.br.tmp", "wb") as b:
                b.write(brotli.compress(data, mode=brotli.MODE_TEXT))
            self.stdout.write(
                self.style.SUCCESS(f"Finished in {round(time.time()-now, 3)} seconds")
            )
        # Replace
        os.replace("json/coords.geojson.tmp", "json/coords.geojson")
        os.replace("json/coords.geojson.gz.tmp", "json/coords.geojson.gz")
        os.replace("json/coords.geojson.br.tmp", "json/coords.geojson.br")
