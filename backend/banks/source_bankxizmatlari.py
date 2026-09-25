from playwright.sync_api import sync_playwright
import re
import time

from django.utils.text import slugify

from banks.normalizer import normalize_bank_name
from banks.models import normalize_name


URLS = [
    "https://bankxizmatlari.uz/ru/loans/avto/",
    "https://bankxizmatlari.uz/ru/loans/ipoteka/",
    "https://bankxizmatlari.uz/ru/loans/microloan/",
    "https://bankxizmatlari.uz/ru/loans/educational/",
    "https://bankxizmatlari.uz/ru/loans/consumer-loan/",
]


# =========================
# UTILS
# =========================

def clean_text(text):
    return re.sub(r"\s+", " ", text or "").strip()


def extract_rate(text):
    if not text:
        return None

    match = re.search(r"\d+[.,]?\d*", text)
    if not match:
        return None

    try:
        return float(match.group(0).replace(",", "."))
    except:
        return None


def extract_amount(text):
    if not text:
        return None

    text = text.replace(" ", "")

    match = re.search(r"(\d+)", text)
    if not match:
        return None

    try:
        value = int(match.group(1))
        return value * 1_000_000 if value < 1000 else value
    except:
        return None


def extract_term(text):
    if not text:
        return None

    match = re.search(r"(\d+)", text)
    return int(match.group(1)) if match else None


# =========================
# KEY BUILDERS
# =========================

def build_unique_key(bank, name, url):
    base = f"{bank}_{name}_{url or ''}"
    return slugify(base)[:255]


def build_aggregated_key(name):
    normalized = normalize_name(name)
    return slugify(normalized)[:255]


# =========================
# MAIN
# =========================

def load_bankxizmatlari_data():
    print("🚀 Parsing bankxizmatlari (ETL PRO 💣)")

    results = []
    seen = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        page = browser.new_page()
        page.set_default_timeout(6000)

        for URL in URLS:
            print(f"\n🌐 {URL}")

            try:
                page.goto(URL, wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(3000)
            except:
                print("⚠️ load error")
                continue

            prev_count = 0

            # =========================
            # 💣 LOAD MORE LOOP
            # =========================
            while True:
                cards = page.locator(".item")
                current_count = cards.count()

                print(f"📊 current cards: {current_count}")

                if current_count == prev_count:
                    print("🛑 no more new items")
                    break

                prev_count = current_count

                try:
                    btn = page.locator("button.js-btn-load-else")

                    if btn.count() == 0:
                        break

                    btn.first.click()
                    page.wait_for_timeout(1500)

                except:
                    break

            print("🔄 full list loaded")

            cards = page.locator(".item")
            total = cards.count()

            print(f"📦 FINAL CARDS FOUND: {total}")

            for i in range(total):
                try:
                    card = cards.nth(i)

                    # =========================
                    # 🏦 BANK
                    # =========================
                    bank_raw = card.locator(".item__header--bank").text_content()
                    if not bank_raw:
                        continue

                    bank = normalize_bank_name(clean_text(bank_raw))

                    if bank == "Unknown Bank":
                        continue

                    # =========================
                    # 📛 NAME
                    # =========================
                    name_raw = card.locator(".item__header--name").text_content()
                    if not name_raw:
                        continue

                    name = clean_text(name_raw).replace('"', '')

                    # =========================
                    # 💣 KEYS
                    # =========================
                    link = None
                    try:
                        href = card.locator("a").first.get_attribute("href")
                        if href:
                            link = "https://bankxizmatlari.uz" + href
                    except:
                        pass

                    unique_key = build_unique_key(bank, name, link)
                    aggregated_key = build_aggregated_key(name)

                    if unique_key in seen:
                        continue

                    seen.add(unique_key)

                    # =========================
                    # 💰 DATA
                    # =========================
                    params = card.locator(".item__params--value")

                    rate = None
                    max_amount = None
                    term = None

                    for j in range(params.count()):
                        try:
                            value = clean_text(params.nth(j).text_content())

                            if rate is None:
                                r = extract_rate(value)
                                if r:
                                    rate = r

                            if max_amount is None:
                                a = extract_amount(value)
                                if a:
                                    max_amount = a

                            if term is None:
                                t = extract_term(value)
                                if t:
                                    term = t

                        except:
                            continue

                    # =========================
                    # 📦 RESULT
                    # =========================
                    results.append({
                        "bank": bank[:100],
                        "name": name[:255],

                        "normalized_name": normalize_name(name),

                        "unique_key": unique_key,
                        "aggregated_key": aggregated_key,

                        "interest_rate": rate,
                        "max_amount": max_amount,
                        "term": term,

                        "description": f"{name} от {bank}",

                        "is_online": True,

                        "source_url": link,
                        "source": "bankxizmatlari",
                    })

                    if i % 20 == 0:
                        print(f"⚡ parsed {i}/{total}")

                except Exception as e:
                    print("⚠️ parse error:", e)
                    continue

        browser.close()

    print(f"\n📊 CLEAN RESULTS: {len(results)}")

    return results