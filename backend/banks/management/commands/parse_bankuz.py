from django.core.management.base import BaseCommand

from banks.parser_bankuz import parse_bankuz
from banks.normalizer import normalize_item

from banks.models import (
    BankProduct,
    Bank,
    AggregatedProduct,
)


class Command(BaseCommand):

    help = "Parse bank.uz products (ETL pipeline)"

    def handle(self, *args, **options):

        self.stdout.write(self.style.WARNING("🚀 START ETL PIPELINE bank.uz"))

        try:

            # ==========================================
            # 🔥 PARSE RAW DATA
            # ==========================================
            raw_data = parse_bankuz()

            if not raw_data:

                self.stdout.write(self.style.ERROR("⚠️ No data returned"))

                return

            # ==========================================
            # 🔥 FLATTEN ALL SECTIONS
            # ==========================================
            raw_items = []

            for section_name, section_items in raw_data.items():

                if not section_items:
                    continue

                self.stdout.write(f"📦 {section_name}: " f"{len(section_items)}")

                raw_items.extend(section_items)

            self.stdout.write(
                self.style.SUCCESS(f"✅ TOTAL RAW ITEMS: " f"{len(raw_items)}")
            )

            # ==========================================
            # 🔥 COUNTERS
            # ==========================================
            created = 0
            updated = 0
            skipped = 0

            # ==========================================
            # 🔥 PROCESS ITEMS
            # ==========================================
            for item in raw_items:

                try:

                    # ==================================
                    # NORMALIZE
                    # ==================================
                    normalized = normalize_item(item)

                    if not normalized:

                        skipped += 1

                        continue

                    # ==================================
                    # BANK
                    # ==================================
                    bank, _ = Bank.objects.get_or_create(name=normalized["bank"])

                    # ==================================
                    # AGGREGATED PRODUCT
                    # ==================================
                    agg, _ = AggregatedProduct.objects.get_or_create(
                        normalized_name=normalized["name"].lower(),
                        product_type=normalized["product_type"],
                        defaults={"name": normalized["name"]},
                    )

                    # ==================================
                    # FIND EXISTING
                    # ==================================
                    existing = BankProduct.objects.filter(
                        source_url=normalized.get("source_url")
                    ).first()

                    # ==================================
                    # UPDATE EXISTING
                    # ==================================
                    if existing:

                        existing.bank = bank

                        existing.bank_name = bank.name

                        existing.aggregated_product = agg

                        existing.name = normalized["name"]

                        existing.normalized_name = normalized["normalized_name"]

                        existing.interest_rate = normalized.get("rate")

                        existing.min_rate = normalized.get("min_rate")

                        existing.max_rate = normalized.get("max_rate")

                        existing.has_rate = normalized.get("has_rate")

                        existing.max_amount = normalized.get("max_amount")

                        existing.term = normalized.get("term")

                        existing.description = normalized.get("description")

                        existing.source_url = normalized.get("source_url")

                        existing.bank_url = normalized.get("bank_url")

                        existing.product_type = normalized.get("product_type")

                        existing.source_name = "bank.uz"

                        existing.parse_success = True

                        existing.save()

                        updated += 1

                    # ==================================
                    # CREATE NEW
                    # ==================================
                    else:

                        obj = BankProduct.objects.create(
                            bank=bank,
                            bank_name=bank.name,
                            aggregated_product=agg,
                            name=normalized["name"],
                            normalized_name=normalized["normalized_name"],
                            interest_rate=normalized.get("rate"),
                            min_rate=normalized.get("min_rate"),
                            max_rate=normalized.get("max_rate"),
                            has_rate=normalized.get("has_rate"),
                            max_amount=normalized.get("max_amount"),
                            term=normalized.get("term"),
                            description=normalized.get("description"),
                            source_url=normalized.get("source_url"),
                            bank_url=normalized.get("bank_url"),
                            product_type=normalized.get("product_type"),
                            source_name="bank.uz",
                            parse_success=True,
                        )

                        created += 1

                        self.stdout.write(
                            self.style.SUCCESS(f"✅ CREATED: " f"{obj.name}")
                        )

                except Exception as item_error:

                    skipped += 1

                    self.stdout.write(
                        self.style.ERROR(f"⚠️ ITEM FAILED: " f"{item_error}")
                    )

            # ==========================================
            # 🔥 RESULT
            # ==========================================
            self.stdout.write(self.style.SUCCESS(f"""
🎉 ETL DONE
--------------------------------
Created : {created}
Updated : {updated}
Skipped : {skipped}
Total   : {len(raw_items)}
--------------------------------
"""))

        except Exception as e:

            self.stdout.write(self.style.ERROR(f"❌ ETL FAILED: {str(e)}"))
