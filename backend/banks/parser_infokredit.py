from playwright.sync_api import sync_playwright
from banks.models import Bank, BankProduct
import re

URL = "https://infokredit.uz/"


def normalize_bank_name(name: str):
    return (name or "Unknown").strip()


def extract_rate(text: str):
    match = re.search(r"(\d+[.,]?\d*)\s*%", text)
    if match:
        return float(match.group(1).replace(",", "."))
    return None


def parse_infokredit():

    print("🚀 Parsing infokredit (FULL SCAN MODE) 💣")

    data = []
    seen = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL, timeout=60000)

        # 💣 просто ждём загрузку
        page.wait_for_timeout(8000)

        blocks = page.locator("div").all()

        print(f"🔍 Total blocks: {len(blocks)}")

        for block in blocks:
            try:
                text = block.inner_text().strip()

                if len(text) < 30:
                    continue

                if "кредит" not in text.lower():
                    continue

                if "%" not in text:
                    continue

                rate = extract_rate(text)
                if not rate:
                    continue

                lines = [l.strip() for l in text.split("\n") if l.strip()]

                if len(lines) < 2:
                    continue

                name = lines[0]
                bank = lines[1] if len(lines) > 1 else "Unknown"

                key = f"{bank}-{name}-{rate}"
                if key in seen:
                    continue

                seen.add(key)

                data.append({
                    "bank": normalize_bank_name(bank),
                    "name": name,
                    "rate": rate
                })

                print(f"🔍 FOUND: {bank} — {name} ({rate}%)")

            except:
                continue

        browser.close()

    print(f"\n📦 Parsed: {len(data)}")

    created = 0

    for item in data:
        try:
            bank, _ = Bank.objects.get_or_create(
                short_name=item["bank"],
                defaults={"name": item["bank"]}
            )

            obj, created_flag = BankProduct.objects.update_or_create(
                bank=bank,
                name=item["name"],
                defaults={
                    "interest_rate": item["rate"],
                    "source_url": URL,
                    "is_active": True,
                }
            )

            if created_flag:
                created += 1
                print(f"✅ {item['bank']} — {item['name']} ({item['rate']}%)")

        except Exception as e:
            print("❌ save error:", e)

    print(f"\n🎉 Done. Created: {created}")
    return created