from banks.parser_static import parse_static
from banks.source_depozit import load_depozit_data
from banks.source_bankxizmatlari import load_bankxizmatlari_data

from banks.models import Bank, BankProduct
from banks.normalizer import normalize_item


def save_products(data, source="external"):
    """
    💣 Сохранение данных с нормализацией
    """

    created = 0
    updated = 0

    for raw in data:
        try:
            # 💣 НОРМАЛИЗАЦИЯ
            item = normalize_item(raw)

            bank_name = item.get("bank")
            name = item.get("name")
            rate = item.get("rate")

            if not name or rate is None:
                continue

            bank, _ = Bank.objects.get_or_create(
                short_name=bank_name,
                defaults={"name": bank_name}
            )

            obj, created_flag = BankProduct.objects.update_or_create(
                bank=bank,
                name=name,
                defaults={
                    "interest_rate": rate,
                    "is_active": True,
                    "source_url": source
                }
            )

            if created_flag:
                created += 1
                print(f"🆕 CREATED: {bank_name} — {name} ({rate}%)")
            else:
                updated += 1
                print(f"♻️ UPDATED: {bank_name} — {name} ({rate}%)")

        except Exception as e:
            print("❌ save error:", e)

    print(f"\n📊 {source.upper()} SUMMARY:")
    print(f"🆕 Created: {created}")
    print(f"♻️ Updated: {updated}")

    return created + updated


def load_all_sources():
    """
    💣 Главная точка загрузки всех источников
    """

    print("🚀 DATA SOURCES LOADING")

    total = 0

    # ==================================================
    # 🧱 STATIC (база)
    # ==================================================

    print("\n📦 Static source...")
    total += parse_static()

    # ==================================================
    # 🌐 DEPOZIT
    # ==================================================

    print("\n🌐 depozit.uz...")
    depozit_data = load_depozit_data()
    total += save_products(depozit_data, "depozit")

    # ==================================================
    # 🌐 BANKXIZMATLARI
    # ==================================================

    print("\n🌐 bankxizmatlari.uz...")
    bankx_data = load_bankxizmatlari_data()
    total += save_products(bankx_data, "bankxizmatlari")

    # ==================================================

    print(f"\n💣 TOTAL PROCESSED: {total}")

    return total