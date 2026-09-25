from playwright.sync_api import sync_playwright
import re
import time

from django.utils.text import slugify

from banks.normalizer import normalize_bank_name
from banks.models import normalize_name


URL = "https://depozit.uz/ru/credits"


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
# SAFE LOAD
# =========================

def safe_load(page):
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(4000)

    # scroll (ленивая подгрузка)
    for _ in range(15):
        page.mouse.wheel(0, 6000)
        page.wait_for_timeout(300)


# =========================
# MAIN
# =========================

def load_depozit_data():
    print("🚀 Parsing depozit (ETL PRO 💣)")

    results = []
    seen = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        page = browser.new_page()
        page.set_default_timeout(6000)

        safe_load(page)

        print("✅ Page loaded")

        cards = page.locator(".content-row.mainContent")
        total = cards.count()

        print(f"📦 CARDS FOUND: {total}")

        for i in range(total):
            try:
                card = cards.nth(i)

                # =========================
                # 🏦 BANK
                # =========================
                raw_bank = None
                imgs = card.locator("img[alt]")

                for j in range(imgs.count()):
                    alt = imgs.nth(j).get_attribute("alt")
                    if alt and len(alt.strip()) > 2:
                        raw_bank = alt.strip()
                        break

                if not raw_bank:
                    continue

                bank = normalize_bank_name(raw_bank)

                if bank == "Unknown Bank":
                    continue

                # =========================
                # 📛 NAME
                # =========================
                name = None
                name_links = card.locator(".credit-name a")

                for j in range(name_links.count()):
                    txt = name_links.nth(j).text_content()
                    if txt and len(txt.strip()) > 2:
                        name = clean_text(txt).replace('"', '')
                        break

                if not name:
                    continue

                # =========================
                # 💣 KEYS
                # =========================
                unique_key = build_unique_key(bank, name, None)
                aggregated_key = build_aggregated_key(name)

                if unique_key in seen:
                    continue

                seen.add(unique_key)

                # =========================
                # 💰 DATA
                # =========================
                rate = None
                max_amount = None
                term = None

                blocks = card.locator(".content")

                for j in range(blocks.count()):
                    try:
                        title = blocks.nth(j).locator(".title").text_content()
                        value = blocks.nth(j).locator(".value").text_content()

                        if not title or not value:
                            continue

                        title = clean_text(title)
                        value = clean_text(value)

                        if "Ставка" in title:
                            rate = extract_rate(value)

                        elif "Сумма" in title:
                            max_amount = extract_amount(value)

                        elif "Срок" in title:
                            term = extract_term(value)

                    except:
                        continue

                # =========================
                # 🔗 LINK
                # =========================
                link = None
                try:
                    href = card.locator(".credit-name a").first.get_attribute("href")
                    if href:
                        link = "https://depozit.uz" + href
                except:
                    pass

                # =========================
                # 📦 RESULT
                # =========================
                results.append({
                    "bank": bank[:100],
                    "name": name[:255],

                    "normalized_name": normalize_name(name),

                    "unique_key": unique_key,
                    "aggregated_key": aggregated_key,

                    "interest_rate": rate,  # может быть None
                    "max_amount": max_amount,
                    "term": term,

                    "description": f"{name} от {bank}",

                    "is_online": True,

                    "source_url": link,
                    "source": "depozit",
                })

                if i % 20 == 0:
                    print(f"⚡ parsed: {i}/{total}")

            except Exception as e:
                print("⚠️ parse error:", e)
                continue

        browser.close()

    print(f"📊 CLEAN RESULTS: {len(results)}")

    return results