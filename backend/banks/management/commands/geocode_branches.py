import time
import requests

from django.core.management.base import BaseCommand

from banks.models import BankBranch


class Command(BaseCommand):

    help = "Geocode bank branches via OpenStreetMap Nominatim"

    def handle(self, *args, **kwargs):

        # ======================================
        # 🔥 LARGE BATCH
        # ======================================
        branches = BankBranch.objects.filter(latitude__isnull=True)[:1000]

        total = branches.count()

        self.stdout.write(self.style.SUCCESS(f"Found {total} branches"))

        headers = {
            "User-Agent": ("BankAnalytics/1.0 " "(contact: admin@bankanalytics.local)")
        }

        success = 0
        failed = 0

        # ======================================
        # 🔥 CITY MAP
        # ======================================
        city_map = {
            "ташкент": "Tashkent",
            "самарканд": "Samarkand",
            "бухара": "Bukhara",
            "андижан": "Andijan",
            "фергана": "Fergana",
            "наманган": "Namangan",
            "карши": "Karshi",
            "термез": "Termez",
            "нукус": "Nukus",
            "джизак": "Jizzakh",
            "гулистан": "Gulistan",
            "навои": "Navoi",
            "ургенч": "Urgench",
            "коканд": "Kokand",
            "ахангаран": "Ahangaran",
            "янгиюль": "Yangiyul",
            "чиназ": "Chinaz",
            "бекабад": "Bekabad",
        }

        for index, branch in enumerate(branches, start=1):

            try:

                if not branch.address:

                    self.stdout.write(
                        self.style.WARNING(f"[{index}/{total}] Empty address")
                    )

                    failed += 1
                    continue

                # ======================================
                # 🔥 CITY-ONLY GEOCODE
                # ======================================
                raw = branch.address.lower()

                found_city = None

                for ru, en in city_map.items():

                    if ru in raw:

                        found_city = en
                        break

                if found_city:

                    query = f"{found_city}, Uzbekistan"

                else:

                    query = "Uzbekistan"

                # ======================================
                # 🔥 REQUEST
                # ======================================
                url = "https://nominatim.openstreetmap.org/search"

                params = {
                    "q": query,
                    "format": "jsonv2",
                    "limit": 1,
                    "addressdetails": 1,
                }

                r = requests.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=20,
                )

                # ======================================
                # 🔥 AUTO RETRY ON 429
                # ======================================
                while r.status_code == 429:

                    self.stdout.write(
                        self.style.WARNING(
                            f"[{index}/{total}] " f"Rate limit reached. Sleeping 60s..."
                        )
                    )

                    time.sleep(60)

                    r = requests.get(
                        url,
                        params=params,
                        headers=headers,
                        timeout=20,
                    )

                # ======================================
                # 🔥 STATUS CHECK
                # ======================================
                if r.status_code != 200:

                    self.stdout.write(
                        self.style.ERROR(
                            f"[{index}/{total}] "
                            f"HTTP {r.status_code}: "
                            f"{branch.address}"
                        )
                    )

                    failed += 1
                    continue

                data = r.json()

                # ======================================
                # 🔥 NO DATA
                # ======================================
                if not data:

                    self.stdout.write(
                        self.style.WARNING(
                            f"[{index}/{total}] " f"No coords: {branch.address}"
                        )
                    )

                    failed += 1
                    continue

                first = data[0]

                lat = float(first["lat"])
                lon = float(first["lon"])

                # ======================================
                # 🔥 SAVE
                # ======================================
                branch.latitude = lat
                branch.longitude = lon

                branch.geocoded = True
                branch.geocode_provider = "nominatim"

                branch.save(
                    update_fields=[
                        "latitude",
                        "longitude",
                        "geocoded",
                        "geocode_provider",
                    ]
                )

                success += 1

                self.stdout.write(
                    self.style.SUCCESS(f"[{index}/{total}] " f"OK: {branch.address}")
                )

                # ======================================
                # 🔥 SAFE RATE LIMIT
                # ======================================
                time.sleep(10)

            except Exception as e:

                failed += 1

                self.stdout.write(
                    self.style.ERROR(
                        f"[{index}/{total}] " f"ERROR: {branch.address} | {e}"
                    )
                )

        # ======================================
        # 🔥 SUMMARY
        # ======================================
        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                f"Geocoding finished. " f"Success: {success}, " f"Failed: {failed}"
            )
        )
