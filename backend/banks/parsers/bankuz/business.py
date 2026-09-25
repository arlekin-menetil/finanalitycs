from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from typing import Any
import re

from banks.models import (
    BankBranch,
)

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
# 🔥 TYPE MAP
# ==========================================
TYPE_MAP = {
    "corp_credits": "business_credit",
    "corp_deposits": "business_deposit",
    "corp_rko": "rko",
    "corp_factoring": "factoring",
}


# ==========================================
# 💣 SAFE AMOUNT
# ==========================================
def safe_amount(x):

    v = parse_amount(x)

    if not v:

        return None

    if 1900 <= v <= 2100:

        return None

    return v


# ==========================================
# 💣 MAIN PARSER
# ==========================================
def parse_business():

    log("🚀 START BUSINESS PARSER")

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

    SECTIONS = [
        {
            "name": "corp_credits",
            "url": "https://bank.uz/corp-credits?page={page}",
            "product_type": "business_credit",
        },
        {
            "name": "corp_deposits",
            "url": "https://bank.uz/corp-deposits?page={page}",
            "product_type": "business_deposit",
        },
        {
            "name": "corp_rko",
            "url": "https://bank.uz/corp-rko?page={page}",
            "product_type": "rko",
        },
        {
            "name": "corp_factoring",
            "url": "https://bank.uz/corp-factoring?page={page}",
            "product_type": "factoring",
        },
    ]

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

        add_page = browser.new_page()

        branch_page = browser.new_page()

        page = browser.new_page()

        for section in SECTIONS:

            log(f"🏢 SECTION: " f"{section['name']}")

            page_num = 1

            empty_pages = 0

            while True:

                log(f"🌐 " f"{section['name']} " f"PAGE {page_num}")

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

                page.wait_for_timeout(3000)

                cards = page.locator(".table-card-offers-bottom")

                count = cards.count()

                log(f"🔍 BUSINESS PRODUCTS FOUND: " f"{count}")

                if count == 0:

                    log("🛑 no cards → stop")

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
                        # 💣 ADS SKIP
                        # ==========================================
                        try:

                            hrefs = card.locator("a").all()

                            if any(
                                "ads.bank.uz" in (h.get_attribute("href") or "")
                                for h in hrefs
                            ):

                                continue

                        except:

                            pass

                        # ==========================================
                        # 💣 BANK RAW
                        # ==========================================
                        try:

                            bank_el = card.locator(
                                ".table-card-offers-block1-text span.medium-text"
                            ).first

                            bank_raw = (
                                clean_text(bank_el.inner_text(timeout=1000))
                                if bank_el.count() > 0
                                else None
                            )

                        except:

                            bank_raw = None

                        # ==========================================
                        # 💣 PRODUCT NAME
                        # ==========================================
                        try:

                            name_el = card.locator(
                                ".table-card-offers-block1-text a"
                            ).first

                            raw_name = (
                                clean_text(name_el.inner_text(timeout=1500))
                                if name_el.count() > 0
                                else None
                            )

                        except:

                            raw_name = None

                        if not raw_name:

                            try:

                                raw_name = clean_text(
                                    card.inner_text(timeout=3000)[:120]
                                )

                            except:

                                continue

                        if not raw_name:

                            continue

                        # ==========================================
                        # 💣 SOURCE URL
                        # ==========================================
                        source_url = None

                        links = card.locator("a")

                        for j in range(links.count()):

                            href = links.nth(j).get_attribute("href")

                            if href and (
                                "/corp-credits/" in href
                                or "/corp-deposits/" in href
                                or "/corp-rko/" in href
                                or "/corp-factoring/" in href
                            ):

                                source_url = "https://bank.uz" + str(href)

                                break

                        if not source_url:

                            continue

                        # ==========================================
                        # 💣 DETAIL PAGE
                        # ==========================================
                        try:

                            detail_page.goto(
                                source_url,
                                wait_until="domcontentloaded",
                                timeout=15000,
                            )

                            detail_page.wait_for_selector(
                                "body",
                                timeout=7000,
                            )

                            detail_page.wait_for_timeout(300)

                        except:

                            log(f"⚠️ detail load failed: " f"{source_url}")

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
                        # 💣 HTML
                        # ==========================================
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

                        except Exception as e:

                            log(f"⚠️ lxml failed " f"→ fallback html.parser ({e})")

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
                        # 💣 BUSINESS TABLE
                        # ==========================================
                        business_table = {}

                        try:

                            tables = soup.select(
                                ".organization-bottom-block table, "
                                ".credit-single-table table, "
                                ".bank-info table, "
                                "table"
                            )

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

                                    if len(key) > 120:

                                        continue

                                    if len(raw_val) > 3000:

                                        continue

                                    business_table[key] = raw_val

                        except Exception as e:

                            log(f"⚠️ table parse failed: {e}")
                            # ==========================================
                        # 💣 STRUCTURED MAPPING
                        # ==========================================
                        mapped_business: dict[
                            str,
                            Any,
                        ] = {
                            "currency": None,
                            "payment_type": None,
                            "collateral": None,
                            "requirements": None,
                            "grace_period": None,
                            "updated_at": None,
                        }

                        for k, v in business_table.items():

                            key = normalize_text(k)

                            # ==========================================
                            # 💣 PAYMENT TYPE
                            # ==========================================
                            if any(
                                x in key
                                for x in [
                                    "уплата процентов",
                                    "погашение",
                                    "платеж",
                                    "выплата",
                                ]
                            ):

                                mapped_business["payment_type"] = v

                            # ==========================================
                            # 💣 COLLATERAL
                            # ==========================================
                            elif any(
                                x in key
                                for x in [
                                    "обеспечение",
                                    "залог",
                                ]
                            ):

                                mapped_business["collateral"] = v

                            # ==========================================
                            # 💣 REQUIREMENTS
                            # ==========================================
                            elif any(
                                x in key
                                for x in [
                                    "документ",
                                    "необходимые документы",
                                    "требования",
                                ]
                            ):

                                mapped_business["requirements"] = v

                            # ==========================================
                            # 💣 GRACE PERIOD
                            # ==========================================
                            elif any(
                                x in key
                                for x in [
                                    "льготный период",
                                    "grace",
                                ]
                            ):

                                mapped_business["grace_period"] = v

                            # ==========================================
                            # 💣 UPDATED
                            # ==========================================
                            elif any(
                                x in key
                                for x in [
                                    "обновлено",
                                    "последнее обновление",
                                    "дата обновления",
                                ]
                            ):

                                mapped_business["updated_at"] = v

                            # ==========================================
                            # 💣 CURRENCY
                            # ==========================================
                            if "сум" in v.lower() or "uzs" in v.lower():

                                mapped_business["currency"] = "UZS"

                            elif (
                                "доллар" in v.lower() or "usd" in v.lower() or "$" in v
                            ):

                                mapped_business["currency"] = "USD"

                            elif "евро" in v.lower() or "eur" in v.lower() or "€" in v:

                                mapped_business["currency"] = "EUR"

                        # ==========================================
                        # 💣 DESCRIPTION ENRICH
                        # ==========================================
                        try:

                            if (
                                not detail.get("description")
                                or len(detail.get("description") or "") < 100
                            ):

                                full_text = clean_text(soup.get_text(" "))

                                if "о кредите" in full_text.lower():

                                    idx = full_text.lower().find("о кредите")

                                    detail["description"] = full_text[idx : idx + 8000]

                                else:

                                    detail["description"] = full_text[:8000]

                        except Exception as e:

                            log(f"⚠️ description enrich failed: {e}")

                        # ==========================================
                        # 💣 TEXT MERGE
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
                        # 💣 PRODUCT NAME
                        # ==========================================
                        name = (
                            detail.get("name")
                            or detail.get("title")
                            or raw_name
                            or "Unknown Product"
                        )

                        normalized_name = normalize_product_name(
                            name
                        ) or normalize_text(name)

                        # ==========================================
                        # 💣 RATE
                        # ==========================================
                        rate = (
                            parse_rate(detail.get("interest_rate"))
                            or parse_rate(detail.get("description"))
                            or parse_rate(raw_name)
                            or parse_rate(card_text)
                        )

                        # ==========================================
                        # 💣 TERM
                        # ==========================================
                        term = (
                            parse_term(detail.get("term"))
                            or parse_term(detail.get("description"))
                            or parse_term(card_text)
                        )

                        # ==========================================
                        # 💣 AMOUNT
                        # ==========================================
                        amount_el = card.locator(
                            ".table-card-offers-block4 span.medium-text"
                        ).first

                        card_amount_raw = (
                            clean_text(amount_el.inner_text(timeout=1000))
                            if amount_el.count() > 0
                            else None
                        )

                        max_amount = (
                            safe_amount(card_amount_raw)
                            or safe_amount(detail.get("max_amount"))
                            or safe_amount(detail.get("description"))
                            or safe_amount(merged_text)
                            or safe_amount(raw_name)
                            or safe_amount(card_text)
                        )

                        # ==========================================
                        # 💣 ADDITIONAL
                        # ==========================================
                        additional = parse_additional_fields(
                            add_page,
                            source_url,
                        )

                        # ==========================================
                        # 💣 BRANCHES
                        # ==========================================
                        branches = []

                        if detail.get("branch_url"):

                            if normalized_bank in branch_cache:

                                log(f"⏭ branches memory cached: " f"{normalized_bank}")

                                branches = branch_cache[normalized_bank]

                            elif normalized_bank in cached_branch_banks:

                                log(f"⏭ branches db cached: " f"{normalized_bank}")

                                parsed_branches_banks.add(normalized_bank)

                            else:

                                log(f"🏦 parsing branches: " f"{normalized_bank}")

                                branches = parse_branches(
                                    branch_page,
                                    detail["branch_url"],
                                )

                                log(f"🏦 branches parsed: " f"{len(branches)}")

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
                        # 💣 CATEGORY
                        # ==========================================
                        text_blob = (detail.get("description") or merged_text).lower()

                        if "овердрафт" in text_blob:

                            category = "business_overdraft"

                        elif "фактор" in text_blob:

                            category = "factoring"

                        elif "рко" in text_blob:

                            category = "rko"

                        elif "депозит" in text_blob:

                            category = "business_deposit"

                        elif "оборот" in text_blob:

                            category = "working_capital"

                        elif "строитель" in text_blob:

                            category = "project_financing"

                        elif "бизнес старт" in text_blob:

                            category = "startup"

                        else:

                            category = section["product_type"]

                        # ==========================================
                        # 💣 ONLINE
                        # ==========================================
                        online = False

                        # ==========================================
                        # 💣 CONFIDENCE
                        # ==========================================
                        confidence = 0.6

                        if detail.get("bank_name"):

                            confidence += 0.2

                        if rate:

                            confidence += 0.1

                        if term:

                            confidence += 0.05

                        if max_amount:

                            confidence += 0.05

                        confidence = round(
                            min(
                                confidence,
                                1.0,
                            ),
                            2,
                        )

                        # ==========================================
                        # 💣 RESULT
                        # ==========================================
                        result_item = {
                            "bank": normalized_bank,
                            "name": name,
                            "normalized_name": normalized_name,
                            "interest_rate": rate,
                            "term": term,
                            "max_amount": max_amount,
                            "source_url": source_url,
                            "category": category,
                            "product_type": section["product_type"],
                            "is_business": True,
                            "online": online,
                            "description": (detail.get("description") or None),
                            "bank_url": (detail.get("bank_url") or None),
                            "bank_address": detail.get("bank_address"),
                            "bank_phone": detail.get("bank_phone"),
                            "currency": mapped_business.get("currency"),
                            "payment_type": mapped_business.get("payment_type"),
                            "collateral": mapped_business.get("collateral"),
                            "requirements": mapped_business.get("requirements"),
                            "grace_period": mapped_business.get("grace_period"),
                            "fee": additional.get("fee"),
                            "branches": branches,
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

                        log(f"⚠️ parse error: {e}")

                # ==========================================
                # 💣 PAGE STATS
                # ==========================================
                log(
                    f"📊 page stats: "
                    f"new={page_new}, "
                    f"duplicates={page_duplicates}"
                )

                if page_new == 0:

                    empty_pages += 1

                else:

                    empty_pages = 0

                if empty_pages >= 3:

                    log("🛑 no new data → stop")

                    break

                page_num += 1

        browser.close()

    # ==========================================
    # 💣 FINAL STATS
    # ==========================================
    log(f"\n💣 TOTAL BUSINESS PRODUCTS: " f"{len(results)}")

    for bank, count in sorted(
        debug_banks.items(),
        key=lambda x: -x[1],
    ):

        log(f"{bank}: {count}")

    log("🎉 BUSINESS DONE")

    return results
