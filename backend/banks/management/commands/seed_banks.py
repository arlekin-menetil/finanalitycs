from django.core.management.base import BaseCommand
from banks.models import Bank


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

    ("Ipak Yuli", "https://ipakyulibank.uz"),
    ("Ziraat Bank", "https://ziraatbank.uz"),
    ("Trustbank", "https://trustbank.uz"),
    ("Aloqabank", "https://aloqabank.uz"),
    ("Ipoteka Bank", "https://ipotekabank.uz"),

    ("KDB Bank", "https://kdb.uz"),
    ("Universal Bank", "https://universalbank.uz"),
    ("Kapitalbank", "https://kapitalbank.uz"),
    ("Octobank", "https://octobank.uz"),
    ("Davr Bank", "https://davrbank.uz"),

    ("InFinBank", "https://infinbank.com"),
    ("Asia Alliance", "https://aab.uz"),
    ("Orient Finans", "https://ofb.uz"),
    ("AVO Bank", "https://avo.uz"),
    ("Poytaxt Bank", "https://poytaxtbank.uz"),

    ("Tenge Bank", "https://tengebank.uz"),
    ("TBC Bank", "https://tbcbank.uz"),
    ("Anor Bank", "https://anorbank.uz"),
    ("Uzum Bank", "https://uzumbank.uz"),
    ("Open Bank", "https://openbank.uz"),

    ("Apex Bank", "https://apexbank.uz"),
    ("Hayot Bank", "https://hayotbank.uz"),
]


FEATURED = ["Hamkorbank", "Aloqabank"]


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        created = 0

        for short_name, website in BANKS:

            is_featured = short_name in FEATURED

            priority = 1.3 if short_name == "Hamkorbank" else 1.25 if short_name == "Aloqabank" else 1

            bank, was_created = Bank.objects.update_or_create(

                short_name=short_name,

                defaults={
                    "website": website,
                    "is_active": True,
                    "is_featured": is_featured,
                    "priority_weight": priority
                }
            )

            if was_created:
                created += 1
                print(f"✔ Created: {short_name}")

        print("")
        print(f"Created banks: {created}")
        print("Seed finished")