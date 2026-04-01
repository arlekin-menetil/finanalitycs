from django.core.management.base import BaseCommand
from decimal import Decimal
import random

from banks.models import Bank, BankProduct


PRODUCT_TEMPLATES = [

    {
        "name": "Consumer Loan",
        "min_score": 450,
        "max_dti": Decimal("0.65"),
        "min_income": Decimal("2000000"),
        "interest_rate": Decimal("22.5"),
        "max_amount": Decimal("100000000")
    },

    {
        "name": "Mortgage",
        "min_score": 500,
        "max_dti": Decimal("0.60"),
        "min_income": Decimal("4000000"),
        "interest_rate": Decimal("18.0"),
        "max_amount": Decimal("800000000")
    },

    {
        "name": "Auto Loan",
        "min_score": 470,
        "max_dti": Decimal("0.62"),
        "min_income": Decimal("3000000"),
        "interest_rate": Decimal("20.0"),
        "max_amount": Decimal("250000000")
    }

]


class Command(BaseCommand):

    help = "Seed bank products"

    def handle(self, *args, **kwargs):

        banks = Bank.objects.filter(is_active=True)

        created = 0

        for bank in banks:

            for template in PRODUCT_TEMPLATES:

                # ====================================
                # Variations per bank
                # ====================================

                rate_variation = Decimal(str(random.uniform(-1.2, 1.2)))
                score_variation = random.randint(-30, 30)
                income_variation = random.randint(-800000, 800000)

                interest_rate = max(
                    Decimal("10"),
                    template["interest_rate"] + rate_variation
                )

                min_score = max(
                    350,
                    template["min_score"] + score_variation
                )

                min_income = max(
                    Decimal("1000000"),
                    template["min_income"] + Decimal(income_variation)
                )

                product, was_created = BankProduct.objects.update_or_create(

                    bank=bank,
                    name=template["name"],

                    defaults={

                        "min_score": min_score,
                        "max_dti": template["max_dti"],
                        "min_income": min_income,
                        "interest_rate": interest_rate,
                        "max_amount": template["max_amount"],
                        "is_active": True
                    }
                )

                if was_created:
                    created += 1
                    print(f"✔ Created {bank.short_name} — {template['name']}")

        print("")
        print("===================================")
        print(f"Products created: {created}")
        print("Seeding products completed")