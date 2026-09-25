from collections import defaultdict

from banks.models import (
    BankProduct,
)


# ==========================================
# 💣 CATEGORY DETECTION
# ==========================================
def detect_category(
    product,
) -> str:

    name = str(product.name or "").lower()

    product_type = str(product.product_type or "").lower()

    loan_type = str(product.loan_type or "").lower()

    # ==========================================
    # 💣 AUTO
    # ==========================================
    if "авто" in name or product_type == "auto":

        return "Автокредит"

    # ==========================================
    # 💣 MORTGAGE
    # ==========================================
    if "ипотек" in name or product_type == "mortgage":

        return "Ипотека"

    # ==========================================
    # 💣 MICRO
    # ==========================================
    if "микро" in name or product_type == "micro":

        return "Микрозайм"

    # ==========================================
    # 💣 OVERDRAFT
    # ==========================================
    if "овердрафт" in name or product_type == "overdraft":

        return "Овердрафт"

    # ==========================================
    # 💣 EDUCATION
    # ==========================================
    if "образ" in name or product_type == "education":

        return "Образовательный кредит"

    # ==========================================
    # 💣 CARD
    # ==========================================
    if product_type == "card":

        return "Банковская карта"

    # ==========================================
    # 💣 CONSUMER
    # ==========================================
    if "потреб" in name or "налич" in name or product_type == "loan":

        return "Потребительский кредит"

    return "Кредит"


# ==========================================
# 💣 NORMALIZE BANK
# ==========================================
def normalize_bank(
    bank,
):

    if not bank:

        return "Unknown Bank"

    return bank.short_name or bank.name or "Unknown Bank"


# ==========================================
# 💣 PRODUCT TITLE
# ==========================================
def build_product_title(
    product,
):

    candidates = [
        product.name,
        product.normalized_name,
        product.slug,
    ]

    for candidate in candidates:

        if candidate:

            candidate = str(candidate).strip()

            if len(candidate) > 2:

                return candidate

    return detect_category(product)


# ==========================================
# 💣 BUILD GROUPS
# ==========================================
def build_merge_groups():

    groups = defaultdict(list)

    products = (
        BankProduct.objects.filter(
            is_active=True,
            interest_rate__isnull=False,
        )
        .select_related("bank")
        .order_by("interest_rate")
    )

    for product in products:

        category = detect_category(product)

        groups[category].append(product)

    return groups


# ==========================================
# 💣 MERGE GROUP
# ==========================================
def merge_group(
    products,
):

    offers_map = {}

    representative = None

    for product in products:

        if not product.interest_rate:
            continue

        try:

            rate = float(product.interest_rate)

        except:

            continue

        # ==========================================
        # 💣 INVALID RATE
        # ==========================================
        if rate < 1 or rate > 60:
            continue

        # ==========================================
        # 💣 REPRESENTATIVE
        # ==========================================
        if representative is None:

            representative = product

        bank_name = normalize_bank(product.bank)

        existing = offers_map.get(bank_name)

        if existing is None or rate < existing["rate"]:

            offers_map[bank_name] = {
                "bank": bank_name,
                "rate": rate,
                "max_amount": product.max_amount,
                "term": product.term,
                "is_online": product.is_online,
                "product_name": build_product_title(product),
                "product_type": product.product_type,
                "bank_name": bank_name,
            }
            # ==========================================
    # 💣 EMPTY
    # ==========================================
    if not offers_map:

        return None

    # ==========================================
    # 💣 SORT OFFERS
    # ==========================================
    offers = sorted(offers_map.values(), key=lambda x: (x["rate"]))

    rates = [o["rate"] for o in offers]

    best_offer = offers[0]

    # ==========================================
    # 💣 REPRESENTATIVE PRODUCT
    # ==========================================
    representative_name = (
        build_product_title(representative) if representative else "Bank Product"
    )

    representative_type = representative.product_type if representative else "loan"

    representative_bank = (
        normalize_bank(representative.bank)
        if representative and representative.bank
        else best_offer["bank"]
    )

    # ==========================================
    # 💣 FINAL OBJECT
    # ==========================================
    return {
        # ==========================================
        # 💣 PRODUCT
        # ==========================================
        "name": representative_name,
        "normalized_name": representative_name,
        "bank_name": representative_bank,
        "product_type": representative_type,
        "category": detect_category(representative) if representative else "Кредит",
        # ==========================================
        # 💣 STATS
        # ==========================================
        "offers_count": len(offers),
        "banks_count": len(offers),
        "min_rate": min(rates),
        "max_rate": max(rates),
        "best_rate": best_offer["rate"],
        "best_bank": best_offer["bank"],
        # ==========================================
        # 💣 FLAGS
        # ==========================================
        "is_online": any(o["is_online"] for o in offers),
        "is_partner": False,
        # ==========================================
        # 💣 LIMITS
        # ==========================================
        "max_amount": best_offer.get("max_amount"),
        "term": best_offer.get("term"),
        # ==========================================
        # 💣 OFFERS
        # ==========================================
        "offers": offers[:10],
    }


# ==========================================
# 💣 MAIN MERGE ENGINE
# ==========================================
def run_merge():

    print("\n🚀 SMART MERGE ENGINE")

    print("=" * 60)

    groups = build_merge_groups()

    result = []

    for category, items in groups.items():

        merged = merge_group(items)

        if not merged:
            continue

        result.append(merged)

    # ==========================================
    # 💣 SORT
    # ==========================================
    result.sort(key=lambda x: (x.get("best_rate") or 999))

    print(f"💣 FINAL GROUPS: " f"{len(result)}")

    # ==========================================
    # 💣 DEBUG OUTPUT
    # ==========================================
    for item in result:

        print(
            f"{item['name']} | "
            f"{item['category']} | "
            f"banks={item['banks_count']} | "
            f"best={item['best_bank']} "
            f"({item['best_rate']}%)"
        )

    print("=" * 60)

    return result
