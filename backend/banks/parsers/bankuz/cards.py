from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from typing import Any
from datetime import datetime
import re

from banks.models import BankBranch

from banks.normalizer import (
    normalize_bank_name,
    normalize_product_name,
)

from .branches import parse_branches
from .details import parse_product_detail

from .shared.logger import log
from .shared.browser import safe_goto

from .shared.normalization import (
    clean_text,
    normalize_text,
    extract_bank_from_name,
)

from .shared.keys import build_product_key


# ==========================================
# 💣 DATE PARSER
# ==========================================
def parse_updated_date(text):

    if not text:
        return None

    text = clean_text(text)

    patterns = [
        "%d.%m.%Y",
        "%d-%m-%Y",
    ]

    for pattern in patterns:

        try:

            return datetime.strptime(
                text,
                pattern,
            ).date()

        except:

            pass

    return None


# ==========================================
# 💣 MAIN PARSER
# ==========================================
def parse_cards():

    log("🚀 START CARDS PARSER")

    results = []

    seen_keys = set()

    parsed_branches_banks = set()

    branch_cache = {}

    cached_branch_banks = set(
        BankBranch.objects.values_list(
            "bank__name",
            flat=True,
        )
    )

    section = {
        "name": "cards",
        "url": "https://bank.uz/cards?page={page}&PAGEN_4={page}",
    }

    debug_banks = {}

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )

        detail_page = browser.new_page()

        branch_page = browser.new_page()

        page = browser.new_page()

        page_num = 1

        empty_pages = 0

        while True:

            log(f"🌐 CARDS PAGE {page_num}")

            if page_num > 100:

                log("🛑 safety stop")

                break

            url = section["url"].format(page=page_num)

            if not safe_goto(page, url):

                break

            try:

                page.wait_for_load_state(
                    "domcontentloaded",
                    timeout=7000,
                )

            except:

                pass

            try:

                html = page.content().lower()

                if "ничего не найдено" in html or "no results" in html:

                    log("🛑 empty page → stop")

                    break

            except:

                pass

            page.wait_for_timeout(2500)

            cards = page.locator(".table-card-offers-bottom")

            count = cards.count()

            log(f"🔍 CARD PRODUCTS FOUND: {count}")

            if count == 0:

                break

            page_new = 0

            page_duplicates = 0

            for i in range(count):

                try:

                    card = cards.nth(i)

                    try:

                        card_text = clean_text(card.inner_text(timeout=2000))

                    except:

                        card_text = ""

                    # ==========================================
                    # 💣 ONLINE FLAGS
                    # ==========================================
                    online_text = ""

                    try:

                        online_el = card.locator(".online_btn")

                        if online_el.count() > 0:

                            online_text = clean_text(online_el.first.inner_text())

                    except:

                        pass

                    has_online = "онлайн" in online_text.lower()

                    has_branch = "банк" in online_text.lower() or not has_online

                    open_methods = []

                    if has_online:

                        open_methods.append("online")

                    if has_branch:

                        open_methods.append("branch")

                    # ==========================================
                    # 💣 BANK
                    # ==========================================
                    bank_raw = None

                    try:

                        bank_el = card.locator(
                            ".table-card-offers-block1-text span.medium-text"
                        ).first

                        if bank_el.count() > 0:

                            bank_raw = clean_text(bank_el.inner_text(timeout=1000))

                    except:

                        pass

                    # ==========================================
                    # 💣 CARD NAME
                    # ==========================================
                    raw_name = None

                    try:

                        name_el = card.locator(".table-card-offers-block1-text a").first

                        if name_el.count() > 0:

                            raw_name = clean_text(name_el.inner_text(timeout=1500))

                    except:

                        pass

                    if not raw_name:

                        continue

                    # ==========================================
                    # 💣 SOURCE URL
                    # ==========================================
                    source_url = None

                    links = card.locator("a")

                    for j in range(links.count()):

                        href = links.nth(j).get_attribute("href")

                        if href and ("/card/" in href or "/cards/" in href):

                            source_url = "https://bank.uz" + str(href)

                            break

                    if not source_url:

                        continue
                    # ==========================================
                    # 💣 DETAIL HTML
                    # ==========================================
                    try:

                        if not safe_goto(
                            detail_page,
                            source_url,
                        ):

                            continue

                        detail_page.wait_for_timeout(500)

                    except:

                        continue

                    # ==========================================
                    # 💣 DETAIL PARSER
                    # ==========================================
                    try:

                        detail = (
                            parse_product_detail(
                                detail_page,
                                source_url,
                            )
                            or {}
                        )

                    except Exception as e:

                        log(f"⚠️ detail parse error: {e}")

                        detail = {}

                    # ==========================================
                    # 💣 STRUCTURED FROM DETAILS
                    # ==========================================
                    detail_structured = (
                        detail.get("structured")
                        or {}
                    )

                    html_detail = detail_page.content()

                    html_detail = re.sub(
                        r"<script.*?>.*?</script>",
                        "",
                        html_detail,
                        flags=re.S | re.I,
                    )

                    html_detail = re.sub(
                        r"<style.*?>.*?</style>",
                        "",
                        html_detail,
                        flags=re.S | re.I,
                    )

                    try:

                        soup = BeautifulSoup(
                            html_detail,
                            "lxml",
                        )

                    except:

                        soup = BeautifulSoup(
                            html_detail,
                            "html.parser",
                        )

                    for tag in soup(
                        [
                            "script",
                            "style",
                            "noscript",
                            "svg",
                        ]
                    ):

                        tag.decompose()
                    # ==========================================
                    # 💣 CARD TABLE
                    # ==========================================
                    card_table = {}

                    try:

                        tables = soup.select(".organization-bottom-block table, table")

                        for table in tables:

                            rows = table.select("tr")

                            for row in rows:

                                cells = row.select("td")

                                if len(cells) < 2:

                                    continue

                                raw_key = clean_text(cells[0].get_text(" "))

                                raw_val = clean_text(cells[1].get_text(" "))

                                if not raw_key or not raw_val:

                                    continue

                                key = normalize_text(raw_key)

                                card_table[key] = raw_val

                    except Exception as e:

                        log(f"⚠️ card table parse failed: {e}")
                    # ==========================================
                    # 💣 IMAGE PARSER
                    # ==========================================
                    image_url = None

                    try:

                        img = soup.select_one("img")

                        if img:

                            raw_src = img.get("src")

                            if raw_src:

                                src = str(raw_src).strip()

                                if src.startswith("//"):

                                    src = "https:" + src

                                elif src.startswith("/"):

                                    src = "https://bank.uz" + src

                                if src.startswith("http"):

                                    image_url = src

                    except Exception as e:

                        log(f"⚠️ image parse failed: {e}")
                    # ==========================================
                    # 💣 STRUCTURED CARD MAPPING
                    # ==========================================
                    mapped_card: dict[str, Any] = {
                        "currency": None,
                        "card_system": None,
                        "issue_cost": None,
                        "service_cost": None,
                        "validity_period": None,
                        "documents_required": None,
                        "updated_at": None,
                    }

                    # ==========================================
                    # 💣 PREFILL FROM DETAILS
                    # ==========================================
                    mapped_card["currency"] = (
                        detail_structured.get("currency")
                    )

                    mapped_card["card_system"] = (
                        detail_structured.get("card_system")
                    )

                    mapped_card["issue_cost"] = (
                        detail_structured.get("issue_cost")
                    )

                    mapped_card["service_cost"] = (
                        detail_structured.get("service_cost")
                    )

                    mapped_card["validity_period"] = (
                        detail_structured.get("validity_period")
                    )

                    mapped_card["documents_required"] = (
                        detail_structured.get("documents_required")
                    )

                    mapped_card["updated_at"] = (
                        detail_structured.get("updated_at")
                    )

                    for k, v in card_table.items():

                        key = normalize_text(k)



                        # ==========================================
                        # 💣 CARD SYSTEM
                        # ==========================================
                        if any(
                            x in key
                            for x in [
                                "система",
                                "платежная система",
                            ]
                        ):

                            mapped_card["card_system"] = v

                        # ==========================================
                        # 💣 ISSUE COST
                        # ==========================================
                        elif any(
                            x in key
                            for x in [
                                "стоимость выпуска",
                                "выпуск",
                            ]
                        ):

                            mapped_card["issue_cost"] = v

                        # ==========================================
                        # 💣 SERVICE COST
                        # ==========================================
                        elif any(
                            x in key
                            for x in [
                                "обслуживание",
                                "стоимость обслуживания",
                            ]
                        ):

                            mapped_card["service_cost"] = v

                        # ==========================================
                        # 💣 VALIDITY
                        # ==========================================
                        elif any(
                            x in key
                            for x in [
                                "срок",
                                "срок действия",
                            ]
                        ):

                            mapped_card["validity_period"] = v

                        # ==========================================
                        # 💣 DOCUMENTS
                        # ==========================================
                        elif any(
                            x in key
                            for x in [
                                "документы",
                                "необходимые документы",
                            ]
                        ):

                            mapped_card["documents_required"] = v

                        # ==========================================
                        # 💣 UPDATED
                        # ==========================================
                        elif any(
                            x in key
                            for x in [
                                "обновлено",
                                "последнее обновление",
                            ]
                        ):

                            mapped_card["updated_at"] = v

                          # ==========================================
                        # 💣 CURRENCY DETECTOR
                        # ==========================================
                        value_lower = v.lower()

                        if any(
                            x in value_lower
                            for x in [
                                "сум",
                                "uzs",
                            ]
                        ):

                            mapped_card["currency"] = "UZS"

                        elif any(
                            x in value_lower
                            for x in [
                                "долл",
                                "доллар",
                                "usd",
                                "$",
                            ]
                        ):

                            mapped_card["currency"] = "USD"

                        elif any(
                            x in value_lower
                            for x in [
                                "евро",
                                "eur",
                                "€",
                            ]
                        ):

                            mapped_card["currency"] = "EUR"

                    # ==========================================
                    # 💣 MERGED TEXT
                    # ==========================================
                    merged_text = " ".join(
                        filter(
                            None,
                            [
                                raw_name,
                                detail.get("description") or "",
                                card_text,
                            ],
                        )
                    )

                    # ==========================================
                    # 💣 BANK RESOLUTION
                    # ==========================================
                    bank_candidates = [
                        (
                            detail.get("bank_name"),
                            1.0,
                        ),
                        (
                            bank_raw,
                            0.8,
                        ),
                        (
                            extract_bank_from_name(raw_name),
                            0.6,
                        ),
                    ]

                    bank_name = None

                    best_score = 0

                    for b, s in bank_candidates:

                        if b and s > best_score:

                            bank_name = b

                            best_score = s

                    normalized_bank = (
                        normalize_bank_name(str(bank_name or "")) or "Unknown Bank"
                    )

                    # ==========================================
                    # 💣 CARD NAME
                    # ==========================================
                    name = detail.get("name") or raw_name

                    normalized_name = normalize_product_name(name) or normalize_text(
                        name
                    )

                    # ==========================================
                    # 💣 CARD SYSTEM DETECTOR
                    # ==========================================
                    card_system = mapped_card.get("card_system") or ""

                    lower_text = merged_text.lower()

                    if not card_system:

                        if "visa" in lower_text:

                            card_system = "VISA"

                        elif "mastercard" in lower_text:

                            card_system = "MASTERCARD"

                        elif "humo" in lower_text:

                            card_system = "HUMO"

                        elif "uzcard" in lower_text:

                            card_system = "UZCARD"

                    # ==========================================
                    # 💣 CARD TYPE DETECTOR
                    # ==========================================
                    card_type = None

                    if "virtual" in lower_text or "виртуал" in lower_text:

                        card_type = "virtual"

                    elif (
                        "premium" in lower_text
                        or "gold" in lower_text
                        or "platinum" in lower_text
                    ):

                        card_type = "premium"

                    elif "salary" in lower_text or "зарплат" in lower_text:

                        card_type = "salary"

                    else:

                        card_type = "standard"

                    # ==========================================
                    # 💣 BRANCHES
                    # ==========================================
                    branches = []

                    if detail.get("branch_url"):

                        if normalized_bank in branch_cache:

                            branches = branch_cache[normalized_bank]

                        elif normalized_bank in cached_branch_banks:

                            parsed_branches_banks.add(normalized_bank)

                        else:

                            branches = parse_branches(
                                branch_page,
                                detail["branch_url"],
                            )

                            branch_cache[normalized_bank] = branches

                            parsed_branches_banks.add(normalized_bank)

                    # ==========================================
                    # 💣 DEDUP
                    # ==========================================
                    stable_key = normalize_text(
                        f"{normalized_bank}|" f"{normalized_name}|" f"{source_url}"
                    )

                    if stable_key in seen_keys:

                        page_duplicates += 1

                        continue

                    seen_keys.add(stable_key)

                    # ==========================================
                    # 💣 CONFIDENCE
                    # ==========================================
                    confidence = 0.7

                    if card_system:

                        confidence += 0.1

                    if mapped_card.get("currency"):

                        confidence += 0.1

                    if image_url:

                        confidence += 0.1

                    confidence = min(
                        confidence,
                        1.0,
                    )

                    # ==========================================
                    # 💣 RESULT ITEM
                    # ==========================================
                    result_item = {
                        "bank": normalized_bank,
                        "name": name,
                        "normalized_name": normalized_name,
                        "source_url": source_url,
                        "category": "card",
                        "product_type": "card",
                        "real_online": has_online,
                        "is_online": has_online,
                        "has_branch": has_branch,
                        "open_methods": open_methods,
                        "description": (detail.get("description") or None),
                        "bank_url": (detail.get("bank_url") or None),
                        "bank_address": detail.get("bank_address"),
                        "bank_phone": detail.get("bank_phone"),
                        "currency": mapped_card.get("currency"),
                        "card_system": card_system,
                        "card_type": card_type,
                        "issue_cost": mapped_card.get("issue_cost"),
                        "service_cost": mapped_card.get("service_cost"),
                        "validity_period": mapped_card.get("validity_period"),
                        "documents_required": mapped_card.get("documents_required"),
                        "image_url": image_url,
                        "updated_from_source": parse_updated_date(
                            mapped_card.get("updated_at")
                        ),
                        "branches": branches,
                        "structured": {
                            "currency": mapped_card.get("currency"),
                            "card_system": card_system,
                            "issue_cost": mapped_card.get("issue_cost"),
                            "service_cost": mapped_card.get("service_cost"),
                            "validity_period": mapped_card.get("validity_period"),
                            "documents_required": mapped_card.get("documents_required"),
                            "updated_at": mapped_card.get("updated_at"),
                        },
                        "unique_key": build_product_key(
                            {
                                "bank": normalized_bank,
                                "name": name,
                                "source_url": source_url,
                            }
                        ),
                        "entity_resolution": {
                            "bank_raw": bank_candidates,
                            "bank_final": normalized_bank,
                            "product_normalized": normalized_name,
                            "confidence": confidence,
                        },
                    }

                    results.append(result_item)

                    debug_banks[normalized_bank] = (
                        debug_banks.get(
                            normalized_bank,
                            0,
                        )
                        + 1
                    )

                    page_new += 1

                except Exception as e:

                    log(f"⚠️ card parse error: {e}")

            # ==========================================
            # 💣 PAGE STATS
            # ==========================================
            log(f"📊 cards stats: " f"new={page_new}, " f"duplicates={page_duplicates}")

            if page_new == 0:

                empty_pages += 1

            else:

                empty_pages = 0

            if empty_pages >= 3:

                log("🛑 no new cards")

                break

            page_num += 1

        browser.close()

    # ==========================================
    # 💣 FINAL STATS
    # ==========================================
    log(f"\n💣 TOTAL CARDS: {len(results)}")

    for bank, count in sorted(
        debug_banks.items(),
        key=lambda x: -x[1],
    ):

        log(f"{bank}: {count}")

    log("🎉 CARDS DONE")

    return results
