from banks.models import BankProduct
from banks.normalizer import normalize_item


def rebuild_bank_products():
    updated = 0
    skipped = 0

    for obj in BankProduct.objects.all():

        item = {
            "name": obj.name,
            "bank": obj.bank.name if obj.bank else None,
            "rate": obj.interest_rate,
            "description": obj.description,
            "max_amount": obj.max_amount,
            "term": obj.term,
            "source_url": obj.source_url,
            "bank_url": obj.bank_url,
        }

        normalized = normalize_item(item)

        if not normalized:
            skipped += 1
            continue

        obj.min_rate = normalized["min_rate"]
        obj.max_rate = normalized["max_rate"]
        obj.has_rate = normalized["has_rate"]

        obj.product_type = normalized["product_type"]
        obj.loan_type = normalized["product_type"]

        obj.normalized_name = normalized["normalized_name"]

        obj.save()
        updated += 1

    return {
        "updated": updated,
        "skipped": skipped
    }