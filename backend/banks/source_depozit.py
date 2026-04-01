import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time


BASE_URL = "https://depozit.uz"

URLS = [
    "/ru/credits",
    "/ru/credits/auto",
    "/ru/credits/microcredit",
    "/ru/credits/mortgage",
    "/ru/credits/consumer",
    "/ru/credits/education",
    "/ru/credits/overdraft",
]


def get_soup(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        print(f"❌ Ошибка: {url} -> {e}")
        return None


def parse_list(url):
    soup = get_soup(url)
    if not soup:
        return []

    cards = soup.select(".single-item-credit")
    print(f"📦 {url} → {len(cards)} карточек")

    results = []

    for card in cards:
        name_tag = card.select_one(".credit-name a")

        name = name_tag.text.strip() if name_tag else None
        link = urljoin(BASE_URL, name_tag["href"]) if name_tag else None

        if name and link:
            results.append({
                "name": name,
                "link": link
            })

    return results


def parse_detail(url):
    soup = get_soup(url)
    if not soup:
        return {}

    data = {}

    try:
        items = soup.select(".credit-single__info li")

        for item in items:
            label = item.select_one(".name")
            value = item.select_one(".value")

            if label and value:
                key = label.text.strip().lower()
                val = value.text.strip()
                data[key] = val

    except:
        pass

    return data


def parse_depozit():
    print("🚀 FULL parsing depozit 💣")

    all_credits = []
    seen_links = set()

    # =========================
    # СОБИРАЕМ ВСЕ КАРТОЧКИ
    # =========================

    for path in URLS:
        full_url = BASE_URL + path
        credits = parse_list(full_url)

        for c in credits:
            if c["link"] not in seen_links:
                seen_links.add(c["link"])
                all_credits.append(c)

    print(f"\n📊 Уникальных кредитов: {len(all_credits)}")

    # =========================
    # DETAIL ПАРСИНГ
    # =========================

    final_results = []

    for i, credit in enumerate(all_credits, 1):
        print(f"🔎 [{i}/{len(all_credits)}] {credit['name']}")

        detail = parse_detail(credit["link"])

        result = {
            "name": credit["name"],
            "link": credit["link"],
            "rate": detail.get("ставка"),
            "amount": detail.get("сумма кредита"),
            "term": detail.get("срок"),
        }

        final_results.append(result)

        time.sleep(0.4)

    print(f"\n✅ ГОТОВО: {len(final_results)}")

    return final_results