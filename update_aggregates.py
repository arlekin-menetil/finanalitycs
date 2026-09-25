from banks.models import AggregatedProduct

for agg in AggregatedProduct.objects.all():
    offers = agg.offers.filter(
        is_active=True,
        interest_rate__isnull=False
    )

    if not offers.exists():
        continue

    rates = [o.interest_rate for o in offers]

    agg.min_rate = min(rates)
    agg.max_rate = max(rates)
    agg.best_rate = min(rates)
    agg.offers_count = offers.count()
    agg.is_online = offers.filter(is_online=True).exists()

    agg.save()

print("🔥 Aggregates updated")