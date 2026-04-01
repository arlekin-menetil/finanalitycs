from django.core.management.base import BaseCommand
from banks.parser_bankuz import parse_bankuz


class Command(BaseCommand):

    help = "Parse bank.uz credits"

    def handle(self, *args, **options):

        self.stdout.write(self.style.WARNING("🚀 Start parsing bank.uz..."))

        try:
            created = parse_bankuz()

            # если функция ничего не возвращает — ок
            if created is None:
                self.stdout.write(self.style.SUCCESS("🎉 Parsing finished"))
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"🎉 Done. Created: {created}")
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error: {str(e)}")
            )