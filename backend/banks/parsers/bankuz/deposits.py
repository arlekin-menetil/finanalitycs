from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from typing import Any
from datetime import datetime

import random
import time

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

from .shared.parsing import (
    parse_rate,
    parse_amount,
    parse_term,
)

from .shared.keys import build_product_key


# ==========================================
# 💣 SAFE AMOUNT
# ==========================================
def safe_amount(x):

    v = parse_amount(x)

    if not v:
        return None

    if v < 50000:
        return None

    return v


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
# 💣 EXTRACT DESCRIPTION
# ==========================================
def extract_description(soup):

    selectors = [
        ".organization-bottom-block",
        ".news-cat-content",
        ".bank-data",
        ".container",
    ]

    for selector in selectors:

        try:

            blocks = soup.select(selector)

            if not blocks:
                continue

            text = clean_text(
                " ".join(
                    x.get_text(
                        " ",
                        strip=True,
                    )
                    for x in blocks
                )
            )

            if len(text) > 200:

                return text[:12000]

        except:

            pass

    return clean_text(soup.get_text(" "))[:12000]


# ==========================================
# 💣 STEALTH PAGE
# ==========================================
def apply_stealth(page):

    try:

        page.add_init_script("""
            Object.defineProperty(
                navigator,
                'webdriver',
                {
                    get: () => undefined
                }
            );

            window.chrome = {
                runtime: {}
            };

            Object.defineProperty(
                navigator,
                'plugins',
                {
                    get: () => [1, 2, 3, 4, 5]
                }
            );

            Object.defineProperty(
                navigator,
                'languages',
                {
                    get: () => ['ru-RU', 'ru']
                }
            );

            Object.defineProperty(
                navigator,
                'platform',
                {
                    get: () => 'MacIntel'
                }
            );
            """)

    except Exception as e:

        log(f"⚠️ stealth init failed: " f"{e}")


# ==========================================
# 💣 MAIN PARSER
# ==========================================
def parse_deposits():

    log("🚀 START DEPOSITS PARSER")

    results = []

    seen_keys = set()

    seen_page_hashes = set()

    parsed_branches_banks = set()

    branch_cache = {}

    cached_branch_banks = set(
        BankBranch.objects.values_list(
            "bank__name",
            flat=True,
        )
    )

    section = {
        "name": "deposits",
        "url": "https://bank.uz/deposits?PAGEN_4={page}",
    }

    debug_banks = {}

    with sync_playwright() as p:

        # ==========================================
        # 💣 PERSISTENT CONTEXT
        # ==========================================
        context = p.chromium.launch_persistent_context(
            user_data_dir="/tmp/playwright_bankuz",
            headless=True,
            slow_mo=random.randint(
                150,
                450,
            ),
            user_agent=(
                "Mozilla/5.0 "
                "(Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            viewport={
                "width": 1440,
                "height": 900,
            },
            locale="ru-RU",
            timezone_id="Asia/Tashkent",
            geolocation={
                "longitude": 69.2401,
                "latitude": 41.2995,
            },
            permissions=["geolocation"],
            extra_http_headers={
                "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
            },
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-web-security",
                "--disable-features=IsolateOrigins,site-per-process",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )

        # ==========================================
        # 💣 PAGES
        # ==========================================
        page = context.new_page()

        detail_page = context.new_page()

        branch_page = context.new_page()

        # ==========================================
        # 💣 STEALTH
        # ==========================================
        for ppp in [
            page,
            detail_page,
            branch_page,
        ]:

            apply_stealth(ppp)

        page_num = 1

        empty_pages = 0

        while True:

            log(f"🌐 DEPOSITS PAGE " f"{page_num}")

            # ==========================================
            # 💣 MEMORY REFRESH
            # ==========================================
            if page_num % 20 == 0:

                try:

                    page.close()

                except:

                    pass

                page = context.new_page()

                apply_stealth(page)

            # ==========================================
            # 💣 SAFETY STOP
            # ==========================================
            if page_num > 100:

                log("🛑 safety stop")

                break

            url = section["url"].format(page=page_num)

            # ==========================================
            # 💣 HUMAN DELAY
            # ==========================================
            time.sleep(
                random.uniform(
                    1.0,
                    3.0,
                )
            )

            if not safe_goto(
                page,
                url,
            ):

                break

            try:

                page.wait_for_load_state(
                    "networkidle",
                    timeout=12000,
                )

            except:

                pass

            page.wait_for_timeout(
                random.randint(
                    1500,
                    3000,
                )
            )

            # ==========================================
            # 💣 PAGE HTML
            # ==========================================
            try:

                html_raw = page.content()

                html = html_raw.lower()

                if any(
                    x in html
                    for x in [
                        "ничего не найдено",
                        "no results",
                    ]
                ):

                    log("🛑 empty page")

                    break

                cards = page.locator(".table-card-offers-bottom")

                count = min(
                    cards.count(),
                    200,
                )

                page_links = []

                for i in range(min(count, 30)):

                    try:

                        card = cards.nth(i)

                        href = card.locator("a").first.get_attribute("href")

                        if href:

                            page_links.append(href)

                    except:

                        pass

                log(f"\n🔥 PAGE {page_num} LINKS")

                for x in page_links[:20]:

                    log(x)

                log("🔥 END LINKS\n")

                page_hash = "|".join(sorted(page_links))

                if not page_links:

                    log("⚠️ no page links found")

                    break

                if page_hash in seen_page_hashes:

                    log("🛑 repeated page")

                    break

                seen_page_hashes.add(page_hash)

            except Exception as e:

                log(f"⚠️ page parse failed: " f"{e}")

                break

            if count == 0:

                break

            page_new = 0

            page_duplicates = 0

            for i in range(count):

                try:

                    card = cards.nth(i)

                    try:

                        card_text = clean_text(card.inner_text(timeout=3000))

                    except:

                        card_text = ""

                    # ==========================================
                    # 💣 ONLINE
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

                        bank_raw = clean_text(bank_el.inner_text(timeout=1500))

                    except:

                        pass

                    # ==========================================
                    # 💣 NAME
                    # ==========================================
                    raw_name = None

                    try:

                        name_el = card.locator(".table-card-offers-block1-text a").first

                        raw_name = clean_text(name_el.inner_text(timeout=2000))

                    except:

                        pass

                    if not raw_name:

                        continue

                    # ==========================================
                    # 💣 DETAIL URL
                    # ==========================================
                    source_url = None

                    try:

                        href = name_el.get_attribute("href")

                        if href:

                            if href.startswith("/"):

                                source_url = "https://bank.uz" + href

                            else:

                                source_url = href

                            # ==========================================
                            # 💣 URL CLEANUP
                            # ==========================================
                            source_url = (
                                source_url.replace("%2F", "").rstrip("/").strip()
                            )

                    except Exception as e:

                        log(f"⚠️ href parse failed: {e}")

                    if not source_url:

                        continue

                    # ==========================================
                    # 💣 INVALID URL PROTECTION
                    # ==========================================
                    if "javascript:" in source_url.lower() or "#" == source_url:

                        continue

                    # ==========================================
                    # 💣 DETAIL PARSER
                    # ==========================================
                    detail = {}

                    html_detail = ""

                    soup = None

                    for attempt in range(1):

                        try:

                            time.sleep(
                                random.uniform(
                                    2.5,
                                    5.5,
                                )
                            )

                            detail = (
                                parse_product_detail(
                                    detail_page,
                                    source_url,
                                )
                                or {}
                            )

                            structured = detail.get("structured") or {}

                            html_detail = detail.get("_html") or ""

                            if not html_detail:

                                html_detail = detail_page.content()

                            # ==========================================
                            # 💣 HTML VALIDATION
                            # ==========================================
                            if not html_detail:

                                log("⚠️ empty detail html")

                                detail = {}

                                continue

                            # ==========================================
                            # 💣 SOUP
                            # ==========================================
                            soup = BeautifulSoup(
                                html_detail,
                                "html.parser",
                            )

                            break

                        except Exception as e:

                            log(f"⚠️ detail parse failed: {e}")

                            detail = {}

                    if not soup:

                        continue

                    # ==========================================
                    # 💣 CLEAN HTML
                    # ==========================================
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
                    # 💣 DESCRIPTION
                    # ==========================================
                    try:

                        detail_description = detail.get("description") or ""

                        if not detail_description or len(detail_description) < 100:

                            detail_description = extract_description(soup)

                    except:

                        detail_description = ""

                    # ==========================================
                    # 💣 MERGED TEXT
                    # ==========================================
                    merged_text = " ".join(
                        filter(
                            None,
                            [
                                raw_name,
                                detail_description,
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
                    # 💣 PRODUCT NAME
                    # ==========================================
                    name = detail.get("name") or raw_name

                    normalized_name = normalize_product_name(name) or normalize_text(
                        name
                    )

                    # ==========================================
                    # 💣 RATE
                    # ==========================================
                    rate = (
                        structured.get("rate_min")
                        or parse_rate(detail.get("interest_rate"))
                        or parse_rate(merged_text)
                    )

                    if rate and rate > 60:

                        rate = None

                    # ==========================================
                    # 💣 TERM
                    # ==========================================
                    term = (
                        structured.get("term")
                        or parse_term(detail.get("term"))
                        or parse_term(merged_text)
                    )

                    if term and term > 600:

                        term = None

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
                    # 💣 RESULT
                    # ==========================================
                    result_item = {
                        "bank": normalized_bank,
                        "name": name,
                        "normalized_name": normalized_name,
                        "category": "deposit",
                        "product_type": "deposit",
                        "loan_type": "deposit",
                        "interest_rate": rate,
                        "term": term,
                        "currency": structured.get("currency"),
                        "raw_data": {
                            "currency": structured.get("currency"),
                            "updated_at": structured.get("updated_at"),
                            "payment_type": structured.get("payment_type"),
                            "amount_min": structured.get("amount_min"),
                            "amount_max": structured.get("amount_max"),
                        },
                        "description": (
                            clean_text(detail_description or merged_text)[:12000]
                        ),
                        "source_url": source_url,
                        "source_name": "bankuz",
                        "unique_key": (
                            build_product_key(
                                {
                                    "bank": normalized_bank,
                                    "name": name,
                                    "source_url": source_url,
                                }
                            )
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

                except Exception as e:

                    log(f"⚠️ deposit parse error: " f"{e}")

            # ==========================================
            # 💣 PAGE STATS
            # ==========================================
            log(
                f"📊 deposits stats: "
                f"new={page_new}, "
                f"duplicates={page_duplicates}"
            )

            if page_duplicates >= count:

                log("🛑 only duplicates")

                break

            if page_new == 0:

                empty_pages += 1

            else:

                empty_pages = 0

            if empty_pages >= 2:

                log("🛑 no new deposits")

                break

            page_num += 1

        # ==========================================
        # 💣 CLOSE CONTEXT
        # ==========================================
        context.close()

    # ==========================================
    # 💣 SUMMARY
    # ==========================================
    log(f"\n💣 TOTAL DEPOSITS: " f"{len(results)}")

    for bank, count in sorted(
        debug_banks.items(),
        key=lambda x: -x[1],
    ):

        log(f"{bank}: {count}")

    log("🎉 DEPOSITS DONE")

    return results
