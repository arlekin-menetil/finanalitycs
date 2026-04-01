from decimal import Decimal
from django.db.models import Avg, Count
from banks.models import Bank


def clamp(value, min_value=Decimal("0"), max_value=Decimal("1")):
    return max(min(value, max_value), min_value)


def get_market_rating():
    banks = (
        Bank.objects
        .filter(is_active=True)
        .prefetch_related("products")
    )

    if not banks.exists():
        return []

    # ===== Считаем агрегаты =====
    bank_data = []

    all_avg_rates = []
    all_product_counts = []
    all_priority = []

    for bank in banks:
        products = bank.products.filter(is_active=True)

        if not products.exists():
            continue

        avg_rate = products.aggregate(avg=Avg("interest_rate"))["avg"]
        product_count = products.count()
        priority = bank.priority_weight

        bank_data.append({
            "bank": bank,
            "avg_rate": avg_rate,
            "product_count": product_count,
            "priority": priority,
        })

        all_avg_rates.append(avg_rate)
        all_product_counts.append(product_count)
        all_priority.append(priority)

    if not bank_data:
        return []

    min_rate = min(all_avg_rates)
    max_rate = max(all_avg_rates)
    max_products = max(all_product_counts)
    max_priority = max(all_priority) or 1

    results = []

    for item in bank_data:
        bank = item["bank"]

        # 1️⃣ Rate competitiveness
        if max_rate > min_rate:
            rate_component = (max_rate - item["avg_rate"]) / (max_rate - min_rate)
        else:
            rate_component = Decimal("0")

        rate_component = clamp(rate_component)

        # 2️⃣ Product diversity
        product_component = clamp(
            Decimal(item["product_count"]) / Decimal(max_products)
        )

        # 3️⃣ Priority
        priority_component = clamp(
            Decimal(item["priority"]) / Decimal(max_priority)
        )

        # 4️⃣ Featured bonus
        featured_component = Decimal("1") if bank.is_featured else Decimal("0")

        # ===== Итог =====
        market_score = (
            rate_component * Decimal("0.40") +
            product_component * Decimal("0.25") +
            priority_component * Decimal("0.25") +
            featured_component * Decimal("0.10")
        )

        market_score = clamp(market_score)

        results.append({
            "bank_id": bank.id,
            "bank_name": bank.short_name,
            "website": bank.website,
            "market_score": float(round(market_score, 4)),
            "avg_interest_rate": float(round(item["avg_rate"], 2)),
            "active_products": item["product_count"],
            "priority_weight": bank.priority_weight,
            "is_featured": bank.is_featured,
        })

    results.sort(key=lambda x: x["market_score"], reverse=True)

    return results