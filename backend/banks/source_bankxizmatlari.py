import requests
from bs4 import BeautifulSoup
import re

from banks.models import Bank, BankProduct


URLS = [
    "https://bankxizmatlari.uz/oz/loans/avto/",
    "https://bankxizmatlari.uz/oz/loans/ipoteka/",
    "https://bankxizmatlari.uz/oz/loans/microloan/",
    "https://bankxizmatlari.uz/oz/loans/educational/",
    "https://bankxizmatlari.uz/oz/loans/consumer-loan/",
]


# =========================
# 🧠 HELPERS
# =========================

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


def extract_rate(text):
    match = re.search(r"(\d+[.,]?\d*)\s*%", text)
    if match:
        return float(match.group(1).replace(",", "."))
    return None


def extract_term(text):
    match = re.search(r"\d+\s*(год|года|лет|месяц|месяцев)", text.lower())
    return match.group(0) if match else None


def extract_bank_name(text):
    words = text.split()

    blacklist = ["kredit", "ставка", "%", "сум", "loan"]

    for w in words[:5]:
        if all(b not in w.lower() for b in blacklist):
            return w

    return words[0] if words else "Unknown"


# =========================
# 💣 MAIN
# =========================

def parse_bankxizmatlari():
    print("🚀 Parsing bankxizmatlari (categories) 💣")

    results = []

    for url in URLS:
        print(f"🌐 {url}")

        try:
            res = requests.get(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15
            )

            soup = BeautifulSoup(res.text, "html.parser")

            cards = soup.find_all("div")

            for card in cards:
                try:
                    text = clean_text(card.get_text(" ", strip=True))

                    if len(text) < 40:
                        continue

                    if "%" not in text:
                        continue

                    rate = extract_rate(text)
                    if not rate:
                        continue

                    term = extract_term(text)
                    bank = extract_bank_name(text)
                    name = " ".join(text.split()[:6])

                    results.append({
                        "bank": bank[:50],
                        "name": name[:200],
                        "rate": rate,
                        "term": term,
                        "source": url,
                    })

                except:
                    continue

        except Exception as e:
            print("❌ error:", e)

    print(f"\n📦 TOTAL: {len(results)}")

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
                bank=bank,
                name=item["name"],
                defaults={
                    "interest_rate": item["rate"],
                    "term": item["term"],
                    "source_url": item["source"],
                    "is_active": True,
                }
            )

            if created_flag:
                created += 1
            else:
                updated += 1

        except Exception as e:
            print("❌ save error:", e)

    print("🎉 DONE")
    print(f"🆕 Created: {created}")
    print(f"♻️ Updated: {updated}")

    return {
        "created": created,
        "updated": updated,
        "total": len(results)
    }