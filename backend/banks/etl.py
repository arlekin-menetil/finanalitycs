from banks.models import Bank, BankProduct
from banks.normalizer import normalize_bank_name

import re

# =========================
# 🧠 PARSERS (ИСПРАВЛЕНО)
# =========================

from banks.parser_bankuz import parse_bankuz as load_bankuz_data
from banks.parser_depozit import parse_depozit as load_depozit_data
from banks.source_bankxizmatlari import load_bankxizmatlari_data


# =========================
# 🧠 EXTRACT BANK FROM NAME
# =========================

def extract_bank_from_name(name):
    if not name:
        return None

    # 🔥 список ключевых банков (можешь расширять)
    known_banks = [
        "Ipak Yuli", "Ipak Yuli Bank",
        "Asakabank",
        "Aloqabank",
        "Hamkorbank",
        "Agrobank",
        "Trastbank",
        "Kapitalbank",
        "Davr Bank",
        "Orient Finans Bank",
        "Asia Alliance",
        "Turon Bank",
        "Xalq Banki",
        "National Bank", "Национальный банк",
        "Узпромстройбанк",
        "BRB",
        "MKBank",
        "Garant bank",
    ]

    for bank in known_banks:
        if bank.lower() in name.lower():
            return bank

    return None


# =========================
# 🏦 GET OR CREATE BANK
# =========================

def get_or_create_bank(name, fallback_name=None):
    # 🔥 если банк не пришел — пробуем вытащить из name
    if not name:
        name = extract_bank_from_name(fallback_name)

    if not name:
        name = "Unknown Bank"

    normalized = normalize_bank_name(name)

    bank, _ = Bank.objects.get_or_create(
        normalized_name=normalized,
        defaults={
            "name": name,
            "short_name": name[:100],
        }
    )

    return bank


# =========================
# 💣 SAVE PRODUCTS
# =========================

def save_products(data):
    created = 0
    updated = 0
    skipped = 0

    for item in data:
        try:
            if not isinstance(item, dict):
                skipped += 1
                continue

            # 🔥 ВАЖНО: передаем name как fallback
            bank = get_or_create_bank(
                item.get("bank"),
                fallback_name=item.get("name")
            )

            if not bank:
                skipped += 1
                continue

            obj, is_created = BankProduct.objects.update_or_create(
                unique_key=item.get("unique_key"),
                defaults={
                    "bank": bank,
                    "name": item.get("name", "Unknown"),
                    "normalized_name": item.get("normalized_name"),

                    "aggregated_key": item.get("aggregated_key"),

                    "interest_rate": item.get("interest_rate"),
                    "max_amount": item.get("max_amount"),
                    "term": item.get("term"),

                    "description": item.get("description"),
                    "source_url": item.get("source_url"),

                    "is_online": item.get("is_online", False),
                    "is_active": True,
                }
            )

            if is_created:
                created += 1
                print(f"🆕 {obj.name} | {bank.name}")
            else:
                updated += 1

        except Exception as e:
            print("⚠️ SAVE ERROR:", e)
            skipped += 1

    print("\n📊 ETL SUMMARY:")
    print(f"🆕 CREATED: {created}")
    print(f"🔁 UPDATED: {updated}")
    print(f"⏭ SKIPPED: {skipped}")


# =========================
# 🚀 MAIN ETL
# =========================

def run_etl():
    print("\n🚀 START ETL PIPELINE\n")

    data = []

    # =========================
    # 💣 BANK.UZ
    # =========================
    try:
        bankuz_data = load_bankuz_data()
        if bankuz_data:
            data += bankuz_data
    except Exception as e:
        print("❌ bankuz failed:", e)

    # =========================
    # 💣 DEPOZIT
    # =========================
    try:
        depozit_data = load_depozit_data()
        if depozit_data:
            data += depozit_data
    except Exception as e:
        print("❌ depozit failed:", e)

    # =========================
    # 💣 BANKXIZMATLARI
    # =========================
    try:
        bx_data = load_bankxizmatlari_data()
        if bx_data:
            data += bx_data
    except Exception as e:
        print("❌ bankxizmatlari failed:", e)

    print(f"\n📦 TOTAL RAW: {len(data)}")

    # =========================
    # 💣 SAVE
    # =========================
    save_products(data)

    print("\n🎉 ETL DONE\n")