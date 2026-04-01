from django.core.management.base import BaseCommand
from banks.models import Bank, BankBranch
import random


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        # координаты Ташкента
        base_lat = 41.3111
        base_lng = 69.2797

        created = 0

        for bank in Bank.objects.filter(is_active=True):

            for i in range(3):

                lat = base_lat + random.uniform(-0.05, 0.05)
                lng = base_lng + random.uniform(-0.05, 0.05)

                BankBranch.objects.create(
                    bank=bank,
                    name=f"{bank.short_name} Branch {i+1}",
                    address="Tashkent",
                    latitude=lat,
                    longitude=lng
                )

                created += 1

        print(f"Created branches: {created}")
