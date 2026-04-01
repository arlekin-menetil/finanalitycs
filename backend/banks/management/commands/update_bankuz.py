from django.core.management.base import BaseCommand
from banks.parser_bankuz import parse_bankuz


class Command(BaseCommand):
    help = "Update bank.uz data"

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Updating bank.uz...")
        result = parse_bankuz()
        self.stdout.write(f"✅ Done: {result}")