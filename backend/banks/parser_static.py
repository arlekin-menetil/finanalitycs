from banks.models import Bank, BankProduct


def parse_static():
    """
    💣 Статический источник данных (MVP)

    - добавляет базовые продукты
    - обновляет существующие
    """

    print("🚀 Loading static data 💣")

    data = [
        {"bank": "Ipak Yo‘li", "name": "Потребительский кредит", "rate": 24},
        {"bank": "Agrobank", "name": "Автокредит", "rate": 26},
        {"bank": "Asakabank", "name": "Кредит наличными", "rate": 28},
        {"bank": "Ipoteka-bank", "name": "Ипотека", "rate": 22},
    ]

    created = 0
    updated = 0

    for item in data:
        try:
            bank_name = item.get("bank")
            product_name = item.get("name")
            rate = item.get("rate")

            if not bank_name or not product_name or rate is None:
                continue

            bank, _ = Bank.objects.get_or_create(
                short_name=bank_name,
                defaults={"name": bank_name}
            )

            obj, created_flag = BankProduct.objects.update_or_create(
                bank=bank,
                name=product_name,
                defaults={
                    "interest_rate": rate,
                    "is_active": True,
                    "source_url": "static"
                }
            )

            if created_flag:
                created += 1
                print(f"🆕 CREATED: {bank_name} — {product_name} ({rate}%)")
            else:
                updated += 1
                print(f"♻️ UPDATED: {bank_name} — {product_name} ({rate}%)")

        except Exception as e:
            print("❌ error:", e)

    print("\n🎉 Done.")
    print(f"🆕 Created: {created}")
    print(f"♻️ Updated: {updated}")

    return created + updated