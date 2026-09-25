from django.core.management.base import BaseCommand
from banks.models import Bank, BankProduct


# 💣 ЧЁТКОЕ СООТВЕТСТВИЕ
BANK_MAP = {
    # Asaka
    "Асака": "Asakabank",

    # Aloqa
    "Алока": "Aloqabank",

    # Ipak
    "Ипак Йули": "Ipak Yuli Bank",

    # Ipoteka
    "Ипотека": "Ipoteka Bank",

    # Kapital
    "Капитал": "Kapitalbank",

    # TBC
    "Тибиси": "TBC Bank",

    # Turon
    "Турон": "Turon Bank",

    # Trast
    "Траст": "Trastbank",

    # Agro
    "Агро": "Agrobank",

    # Halk
    "Халк И": "Halk Bank",

    # Orient
    "Ориент Финанс": "Orient Finans Bank",

    # KDB
    "Кдб Узбекистан": "KDB Bank",

    # Mikrokredit
    "Микрокредит": "Mikrokredit",
}


class Command(BaseCommand):
    help = "💣 Clean duplicate banks (STRICT MODE)"

    def handle(self, *args, **kwargs):

        print("🚀 CLEANING BANKS (STRICT)")

        for old_name, new_name in BANK_MAP.items():

            try:
                main_bank = Bank.objects.filter(name=new_name).first()
                duplicate = Bank.objects.filter(name=old_name).first()

                if not main_bank or not duplicate:
                    continue

                if main_bank.id == duplicate.id:
                    continue

                print(f"🔁 MERGE: {old_name} → {new_name}")

                # перенос продуктов
                BankProduct.objects.filter(bank=duplicate).update(bank=main_bank)

                duplicate.delete()

            except Exception as e:
                print("❌ ERROR:", e)

        print("✅ DONE")