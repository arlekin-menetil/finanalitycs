from django.core.management.base import BaseCommand
from banks.models import Bank, normalize_name


BANKS = [

    ("NBU", "https://nbu.uz"),
    ("SQB", "https://sqb.uz"),
    ("Agrobank", "https://agrobank.uz"),
    ("Mikrokreditbank", "https://mkbank.uz"),
    ("Xalq Bank", "https://xb.uz"),

    ("Garant Bank", "https://garantbank.uz"),
    ("BRB", "https://brb.uz"),
    ("Turonbank", "https://turonbank.uz"),
    ("Hamkorbank", "https://hamkorbank.uz"),
    ("Asakabank", "https://asakabank.uz"),

    ("Ipak Yuli Bank", "https://ipakyulibank.uz"),
    ("Ziraat Bank", "https://ziraatbank.uz"),
    ("Trastbank", "https://trustbank.uz"),
    ("Aloqabank", "https://aloqabank.uz"),
    ("Ipoteka Bank", "https://ipotekabank.uz"),

    ("KDB Bank", "https://kdb.uz"),
    ("Universal Bank", "https://universalbank.uz"),
    ("Kapitalbank", "https://kapitalbank.uz"),
    ("Octobank", "https://octobank.uz"),
    ("Davr Bank", "https://davrbank.uz"),

    ("Infinbank", "https://infinbank.com"),
    ("Asia Alliance Bank", "https://aab.uz"),
    ("Orient Finans Bank", "https://ofb.uz"),
    ("AVO Bank", "https://avo.uz"),
    ("Poytaxt Bank", "https://poytaxtbank.uz"),

    ("Tenge Bank", "https://tengebank.uz"),
    ("TBC Bank", "https://tbcbank.uz"),
    ("Anor Bank", "https://anorbank.uz"),
    ("Uzum Bank", "https://uzumbank.uz"),
    ("Open Bank", "https://openbank.uz"),

    ("Apex Bank", "https://apexbank.uz"),
    ("Hayot Bank", "https://hayotbank.uz"),

    # 🔥 ДОБАВИЛИ
    ("Mybank", "https://mybank.uz"),
]


FEATURED = ["Hamkorbank", "Aloqabank"]


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        created = 0
        updated = 0

        for name, website in BANKS:

            is_featured = name in FEATURED

            priority = (
                1.3 if name == "Hamkorbank"
                else 1.25 if name == "Aloqabank"
                else 1
            )

            normalized = normalize_name(name)

            bank, was_created = Bank.objects.update_or_create(
                normalized_name=normalized,
                defaults={
                    "name": name,
                    "short_name": name,
                    "website": website,
                    "is_active": True,
                    "is_featured": is_featured,
                    "priority_weight": priority
                }
            )

            if was_created:
                created += 1
                print(f"✔ Created: {name}")
            else:
                updated += 1
                print(f"♻️ Updated: {name}")

        print("")
        print(f"🆕 Created banks: {created}")
        print(f"♻️ Updated banks: {updated}")
        print("✅ Seed finished")