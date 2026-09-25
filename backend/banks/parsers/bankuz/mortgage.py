from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

from banks.models import BankBranch
from banks.normalizer import (
    normalize_bank_name,
    normalize_product_name,
)

from .branches import parse_branches
from .details import parse_product_detail
from .additional import parse_additional_fields

from .shared.logger import log
from .shared.browser import safe_goto

from .shared.normalization import (
    clean_text,
    normalize_text,
    extract_bank_from_name,
)

from .shared.parsing import (
    parse_rate,
    parse_amount,
    parse_term,
)

from .shared.keys import build_product_key


# ==========================================
# MAIN PARSER
# ==========================================
def parse_mortgage():

    log("🚀 START MORTGAGE PARSER")

    results = []

    seen_keys = set()

    cached_branch_banks = set(
        BankBranch.objects.values_list(
            "bank__name",
            flat=True,
        )
    )

    branch_cache = {}

    # ==========================================
    # FIXED PAGINATION
    # ==========================================
    section = {
        "name": "mortgage",
        "url": "https://bank.uz/ipoteka?PAGEN_4={page}",
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

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            locale="ru-RU",
            viewport={
                "width": 1440,
                "height": 900,
            },
            java_script_enabled=True,
        )

        page = context.new_page()
        detail_page = context.new_page()
        add_page = context.new_page()
        branch_page = context.new_page()

        for p_ in [
            page,
            detail_page,
            add_page,
            branch_page,
        ]:
            p_.set_default_timeout(30000)

        page_num = 1
        empty_pages = 0

        while True:

            log(f"\n📄 PAGE {page_num}")

            if page_num > 20:

                log("🛑 safety stop")

                break

            url = section["url"].format(page=page_num)

            log(f"🌐 OPEN: {url}")

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
                page.wait_for_selector(
                    ".table-card-offers-bottom",
                    timeout=10000,
                )
            except:
                pass

            page.wait_for_timeout(2500)

            html = page.content()

            if not html:
                break

            soup = BeautifulSoup(html, "html.parser")

            cards = soup.select(".table-card-offers-bottom")

            count = len(cards)

            log(f"🔍 CARDS FOUND: {count}")

            if count == 0:
                break

            page_new = 0
            page_duplicates = 0

            for card in cards:

                try:

                    card_text = clean_text(card.get_text(" ", strip=True))

                    # ==========================================
                    # BANK
                    # ==========================================
                    bank_raw = None

                    try:

                        bank_el = card.select_one(
                            ".table-card-offers-block1-text span.medium-text"
                        )

                        if bank_el:
                            bank_raw = clean_text(bank_el.get_text(strip=True))

                    except:
                        pass

                    # ==========================================
                    # NAME
                    # ==========================================
                    raw_name = None

                    try:

                        name_el = card.select_one(".table-card-offers-block1-text a")

                        if name_el:
                            raw_name = clean_text(name_el.get_text(strip=True))

                    except:
                        pass

                    if not raw_name:
                        continue

                    # ==========================================
                    # DESCRIPTION
                    # ==========================================
                    short_description = None

                    try:

                        desc_elements = card.select(
                            ".table-card-offers-block1-text span.medium-text"
                        )

                        if len(desc_elements) >= 2:

                            desc_candidate = clean_text(
                                desc_elements[-1].get_text(strip=True)
                            )

                            if desc_candidate and desc_candidate != bank_raw:
                                short_description = desc_candidate

                    except:
                        pass

                    # ==========================================
                    # URL
                    # ==========================================
                    source_url = None

                    links = card.select("a")

                    for link in links:

                        try:

                            href = link.get("href")

                            if not href:
                                continue

                            href = str(href).strip()

                            if "/ipoteki/" in href.lower():

                                source_url = (
                                    href
                                    if href.startswith("http")
                                    else "https://bank.uz" + href
                                )

                                break

                        except:
                            pass

                    if not source_url:
                        continue

                    log(f"🌐 DETAIL: {source_url}")

                    # ==========================================
                    # DETAIL PAGE
                    # ==========================================
                    if not safe_goto(
                        detail_page,
                        source_url,
                    ):
                        continue

                    detail_page.wait_for_timeout(2500)

                    detail = (
                        parse_product_detail(
                            detail_page,
                            source_url,
                        )
                        or {}
                    )

                    additional = parse_additional_fields(
                        add_page,
                        source_url,
                    )

                    # ==========================================
                    # MERGED TEXT
                    # ==========================================
                    merged_text = " ".join(
                        filter(
                            None,
                            [
                                raw_name,
                                short_description,
                                detail.get("description"),
                                card_text,
                            ],
                        )
                    )

                    # ==========================================
                    # BANK RESOLUTION
                    # ==========================================
                    bank_candidates = [
                        (detail.get("bank_name"), 1.0),
                        (bank_raw, 0.9),
                        (
                            extract_bank_from_name(raw_name),
                            0.6,
                        ),
                        (
                            extract_bank_from_name(merged_text),
                            0.5,
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
                    # PRODUCT NAME
                    # ==========================================
                    name = detail.get("name") or raw_name

                    normalized_name = normalize_product_name(name) or normalize_text(
                        name
                    )

                    # ==========================================
                    # RATE
                    # ==========================================
                    rate = detail.get(
                        "structured",
                        {},
                    ).get(
                        "rate_min"
                    ) or parse_rate(merged_text)

                    # ==========================================
                    # TERM
                    # ==========================================
                    term = detail.get(
                        "structured",
                        {},
                    ).get(
                        "term"
                    ) or parse_term(merged_text)

                    # ==========================================
                    # AMOUNT
                    # ==========================================
                    max_amount = detail.get(
                        "structured",
                        {},
                    ).get(
                        "amount_max"
                    ) or parse_amount(merged_text)

                    # ==========================================
                    # CATEGORY
                    # ==========================================
                    category = "mortgage"

                    try:

                        onclick = ""

                        first_link = card.select_one("a")

                        if first_link:

                            onclick = str(first_link.get("onclick", ""))

                        onclick_lower = onclick.lower()

                        if "вторичный рынок" in onclick_lower:
                            category = "secondary"

                        elif "новостройки" in onclick_lower:
                            category = "new_building"

                    except:
                        pass

                    # ==========================================
                    # BRANCHES
                    # ==========================================
                    branches = []

                    if detail.get("branch_url"):

                        if normalized_bank in branch_cache:

                            branches = branch_cache[normalized_bank]

                        elif normalized_bank not in cached_branch_banks:

                            branches = parse_branches(
                                branch_page,
                                detail["branch_url"],
                            )

                            branch_cache[normalized_bank] = branches

                    # ==========================================
                    # DEDUP
                    # ==========================================
                    stable_key = normalize_text(
                        f"{normalized_bank}|" f"{normalized_name}|" f"{source_url}"
                    )

                    if stable_key in seen_keys:

                        page_duplicates += 1

                        log(f"♻️ duplicate: " f"{normalized_name}")

                        continue

                    seen_keys.add(stable_key)

                    # ==========================================
                    # ONLINE
                    # ==========================================
                    text_blob = merged_text.lower()

                    online = (
                        bool(additional.get("real_online")) or "онлайн" in text_blob
                    )

                    # ==========================================
                    # DESCRIPTION
                    # ==========================================
                    final_description = (
                        detail.get("description") or short_description or card_text
                    )

                    # ==========================================
                    # RESULT
                    # ==========================================
                    result_item = {
                        "bank": normalized_bank,
                        "name": name,
                        "normalized_name": normalized_name,
                        # ==========================================
                        # 💣 PRODUCT TYPES
                        # ==========================================
                        "category": category,
                        "product_type": "mortgage",
                        "loan_type": "mortgage",
                        "source_type": "mortgage",
                        # ==========================================
                        # 💣 MAIN DATA
                        # ==========================================
                        "interest_rate": rate,
                        "term": term,
                        "max_amount": max_amount,
                        "currency": detail.get(
                            "structured",
                            {},
                        ).get("currency"),
                        # ==========================================
                        # 💣 STRUCTURED
                        # ==========================================
                        "structured": {
                            "rate_min": rate,
                            "rate_max": rate,
                            "amount_min": None,
                            "amount_max": max_amount,
                            "term": term,
                            "currency": detail.get(
                                "structured",
                                {},
                            ).get("currency"),
                        },
                        # ==========================================
                        # 💣 ONLINE
                        # ==========================================
                        "online": online,
                        # ==========================================
                        # 💣 DESCRIPTION
                        # ==========================================
                        "description": final_description,
                        # ==========================================
                        # 💣 EXTRA
                        # ==========================================
                        "payment_type": detail.get(
                            "structured",
                            {},
                        ).get("payment_type"),
                        "collateral": detail.get(
                            "structured",
                            {},
                        ).get("collateral"),
                        "requirements": (
                            detail.get(
                                "structured",
                                {},
                            ).get("requirements")
                            or additional.get("requirements")
                        ),
                        "fee": additional.get("fee"),
                        # ==========================================
                        # 💣 BANK INFO
                        # ==========================================
                        "bank_url": detail.get("bank_url"),
                        "bank_address": detail.get("bank_address"),
                        "bank_phone": detail.get("bank_phone"),
                        # ==========================================
                        # 💣 BRANCHES
                        # ==========================================
                        "branches": branches,
                        # ==========================================
                        # 💣 SOURCE
                        # ==========================================
                        "source_url": source_url,
                        "source_name": "bankuz",
                        # ==========================================
                        # 💣 UNIQUE
                        # ==========================================
                        "unique_key": build_product_key(
                            {
                                "bank": normalized_bank,
                                "name": name,
                                "source_url": source_url,
                            }
                        ),
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

                    log(
                        f"✅ {normalized_bank} | "
                        f"{name} | "
                        f"type=mortgage | "
                        f"{rate}"
                    )

                except Exception as e:

                    log(f"⚠️ parse error: {e}")

            log(f"📊 page stats: " f"new={page_new}, " f"duplicates={page_duplicates}")

            if page_duplicates >= count:

                log("🛑 only duplicates on page")

                break

            if page_new == 0:

                empty_pages += 1

            else:

                empty_pages = 0

            if empty_pages >= 2:

                log("🛑 no new data")

                break

            page_num += 1

        browser.close()

    log(f"\n💣 TOTAL PARSED: {len(results)}")

    for bank, count in sorted(
        debug_banks.items(),
        key=lambda x: -x[1],
    ):
        log(f"{bank}: {count}")

    log("🎉 DONE")

    return results
