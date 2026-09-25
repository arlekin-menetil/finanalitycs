from banks.models import Bank, BankProduct
from banks.normalizer import normalize_item, normalize_bank_name


# =========================
# 💣 BANK KEY NORMALIZATION
# =========================

def get_bank_key(name: str) -> str:
    if not name:
        return ""

    name = name.lower()
    name = name.replace("bank", "")
    name = name.replace("банк", "")
    name = name.replace("o‘z", "")
    name = name.replace("uz", "")
    name = name.replace("-", "")
    name = name.replace(" ", "")

    return name.strip()


# =========================
# 💣 UNIQUE KEY (СТАБИЛЬНЫЙ)
# =========================

def generate_unique_key(bank, name, rate=None):
    bank = (bank or "").strip().lower()
    name = (name or "").strip().lower()

    if not bank or not name:
        return None

    key = f"{bank}|{name}"

    if rate is not None:
        key += f"|{rate}"

    return key[:255]


# =========================
# 💣 BANK SEED
# =========================

BANKS_SEED = [
    "O‘zmilliybank",
    "SQB",
    "Mikrokreditbank",
    "Asia Alliance Bank",
    "Octobank",
    "Uzum Bank",
    "AVO Bank",
    "Open Bank",
    "Apex Bank",
    "Hayot Bank",
]


def seed_banks():
    print("🌱 Seeding banks...")

    created = 0

    for bank_name in BANKS_SEED:
        try:
            bank_key = get_bank_key(bank_name)

            _, created_flag = Bank.objects.get_or_create(
                normalized_name=bank_key,
                defaults={
                    "name": bank_name,
                    "short_name": bank_name,
                }
            )

            if created_flag:
                created += 1

        except Exception as e:
            print("❌ seed error:", e)

    print(f"🌱 Seeded banks: {created}")


# =========================
# 💣 STATIC PARSER
# =========================

def parse_static():
    """
    💣 Static dataset loader (for testing + fallback)
    """

    print("🚀 Loading static data 💣")

    # seed banks first
    seed_banks()

    data = [
        {"bank": "Ipak Yo‘li", "name": "Потребительский кредит", "rate": 24},
        {"bank": "Agrobank", "name": "Автокредит", "rate": 26},
        {"bank": "Asakabank", "name": "Кредит наличными", "rate": 28},
        {"bank": "Ipoteka-bank", "name": "Ипотека", "rate": 22},
    ]

    created = 0
    updated = 0
    skipped = 0

    for raw in data:
        try:
            # =========================
            # NORMALIZE INPUT
            # =========================
            item = normalize_item(raw)

            bank_name = normalize_bank_name(item.get("bank"))
            product_name = item.get("name")
            rate = item.get("rate")

            # =========================
            # VALIDATION
            # =========================
            if not bank_name or not product_name:
                skipped += 1
                continue

            try:
                rate = float(rate) if rate is not None else None
            except:
                rate = None

            if rate is None or rate <= 0 or rate > 100:
                skipped += 1
                continue

            # =========================
            # BANK KEY
            # =========================
            bank_key = get_bank_key(bank_name)

            bank, _ = Bank.objects.get_or_create(
                normalized_name=bank_key,
                defaults={
                    "name": bank_name,
                    "short_name": bank_name,
                }
            )

            # =========================
            # UNIQUE KEY (FIXED)
            # =========================
            unique_key = generate_unique_key(
                bank_name,
                product_name,
                rate
            )

            if not unique_key:
                skipped += 1
                continue

            # =========================
            # SAVE PRODUCT
            # =========================
            obj, created_flag = BankProduct.objects.update_or_create(
                unique_key=unique_key,
                defaults={
                    "bank": bank,
                    "name": product_name.strip(),
                    "interest_rate": rate,
                    "is_active": True,
                    "source_url": "static",
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
            skipped += 1

    print("\n🎉 DONE STATIC LOAD")
    print(f"🆕 Created: {created}")
    print(f"♻️ Updated: {updated}")
    print(f"⏭ Skipped: {skipped}")

    return created + updated