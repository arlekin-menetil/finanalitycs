from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import time

from banks.models import Bank, BankProduct


# =========================
# 🧠 HELPERS
# =========================

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


def parse_rate(text):
    if not text:
        return None

    match = re.search(r"\d+[.,]?\d*", text)
    if not match:
        return None

    return float(match.group(0).replace(",", "."))


def normalize_bank_name(text):
    text = text.lower()

    mapping = {
        "ипак": "Ipak Yuli Bank",
        "kapital": "Kapitalbank",
        "asaka": "Asaka Bank",
        "aloqa": "Aloqabank",
        "agro": "Agrobank",
    }

    for key, val in mapping.items():
        if key in text:
            return val

    return text.title()


# =========================
# 💣 MAIN PARSER (FINAL)
# =========================

def parse_bankuz():
    print("🚀 Parsing bank.uz FINAL 💣")

    results = []
    seen = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for page_num in range(1, 24):
            print(f"🌐 Page {page_num}")

            page = browser.new_page()
            url = f"https://bank.uz/credits?PAGEN_4={page_num}"

            page.goto(url, timeout=60000)

            # 💣 ЖДЁМ РЕАЛЬНЫЕ КАРТОЧКИ
            try:
                page.wait_for_selector(".table-card-offers-bottom", timeout=15000)
            except:
                print("⚠️ fallback wait...")
                page.wait_for_timeout(5000)

            soup = BeautifulSoup(page.content(), "html.parser")

            cards = soup.select(".table-card-offers-bottom")

            print(f"🔍 Found cards: {len(cards)}")

            for card in cards:
                try:
                    # =========================
                    # 🏦 БАНК
                    # =========================
                    bank_tag = card.select_one(".table-card-offers-block1-text span")
                    bank = clean_text(bank_tag.text) if bank_tag else "Unknown"
                    bank = normalize_bank_name(bank)

                    # =========================
                    # 📌 НАЗВАНИЕ
                    # =========================
                    name_tag = card.select_one(".table-card-offers-block1-text a")
                    name = clean_text(name_tag.text) if name_tag else "Unknown"

                    # =========================
                    # 💸 СТАВКА
                    # =========================
                    rate_tag = card.select_one(".table-card-offers-block2 span.medium-text")
                    rate = parse_rate(rate_tag.text if rate_tag else None)

                    if not rate:
                        continue

                    # =========================
                    # ⏳ СРОК
                    # =========================
                    term_tag = card.select_one(".table-card-offers-block3 span.medium-text")
                    term = clean_text(term_tag.text) if term_tag else None

                    # =========================
                    # 💰 СУММА
                    # =========================
                    amount_tag = card.select_one(".table-card-offers-block4 span.medium-text")
                    amount = clean_text(amount_tag.text) if amount_tag else None

                    # =========================
                    # 🔗 ССЫЛКА (ВАЖНО)
                    # =========================
                    link_tag = card.select_one("a[href]")
                    link = link_tag["href"] if link_tag else None

                    if not link:
                        continue

                    # 💣 уникальность
                    if link in seen:
                        continue

                    seen.add(link)

                    results.append({
                        "bank": bank[:100],
                        "name": name[:255],
                        "rate": rate,
                        "term": term,
                        "amount": amount,
                        "url": link,
                    })

                except Exception as e:
                    print("⚠️ parse error:", e)

            page.close()
            time.sleep(1)

        browser.close()

    print(f"\n📦 UNIQUE PARSED: {len(results)}")

    # =========================
    # 💾 SAVE
    # =========================

    created = 0
    updated = 0

    for item in results:
        try:
            bank, _ = Bank.objects.get_or_create(
                short_name=item["bank"],
                defaults={"name": item["bank"]}
            )

            obj, created_flag = BankProduct.objects.update_or_create(
                source_url=item["url"],  # 💣 ключ уникальности
                defaults={
                    "bank": bank,
                    "name": item["name"],
                    "interest_rate": item["rate"],
                    "term": item["term"],
                    "is_active": True,
                }
            )

            if created_flag:
                created += 1
            else:
                updated += 1

        except Exception as e:
            print("❌ save error:", e)

    print("\n🎉 DONE")
    print(f"🆕 Created: {created}")
    print(f"♻️ Updated: {updated}")

    return {
        "created": created,
        "updated": updated,
        "total": len(results)
    }