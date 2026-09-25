from banks.models import Bank, BankProduct
from collections import defaultdict

groups = defaultdict(list)

for bank in Bank.objects.all():
    groups[bank.name.strip()].append(bank)

for name, banks in groups.items():
    if len(banks) > 1:
        main = banks[0]

        for duplicate in banks[1:]:
            BankProduct.objects.filter(bank=duplicate).update(bank=main)
            duplicate.delete()

        print(f"✔ merged: {name}")

print("✅ DONE")