from bs4 import BeautifulSoup
import re

from .shared.browser import safe_goto
from .shared.normalization import (
    clean_text,
    normalize_text,
)
from .shared.logger import log


# ==========================================
# 🔥 BRANCH PARSER
# ==========================================
def parse_branches(page, url):

    branches = []

    seen_addresses = set()

    seen_page_hashes = set()

    try:

        log("🏦 parsing branches")

        page_num = 1

        duplicate_pages = 0

        while True:

            # ==========================================
            # 💣 SAFETY LIMIT
            # ==========================================
            if page_num > 30:

                log("🛑 branch safety limit")

                break

            paged_url = f"{url}?PAGEN_1={page_num}"

            log(f"🏦 branch page: {page_num}")

            # ==========================================
            # 💣 OPEN PAGE
            # ==========================================
            if not safe_goto(page, paged_url):

                break

            try:

                page.wait_for_load_state(
                    "domcontentloaded",
                    timeout=7000,
                )

            except:

                log("⚠️ load timeout")

            try:

                page.wait_for_selector(
                    "body",
                    timeout=7000,
                )

            except:

                pass

            try:

                page.wait_for_timeout(1000)

            except:

                pass

            # ==========================================
            # 💣 HTML
            # ==========================================
            html_raw = page.content()

            html = html_raw.lower()

            # ==========================================
            # 💣 CAPTCHA DETECT
            # ==========================================
            captcha_detected = any(
                x in html
                for x in [
                    "captcha",
                    "cloudflare",
                    "verify you are human",
                    "cf-challenge",
                ]
            )

            if captcha_detected:

                log("🚫 captcha branch page")

            # ==========================================
            # 💣 PAGE HASH DEDUP
            # ==========================================
            try:

                page_hash = normalize_text(
                    BeautifulSoup(
                        html_raw,
                        "html.parser",
                    ).get_text(" ")
                )[:2500]

                if page_hash in seen_page_hashes:

                    log("🛑 repeated branch page")

                    break

                seen_page_hashes.add(page_hash)

            except Exception as e:

                log(f"⚠️ branch hash failed: " f"{e}")

            soup = BeautifulSoup(
                html_raw,
                "html.parser",
            )

            # ==========================================
            # 💣 REAL BRANCH BLOCKS
            # ==========================================
            branch_blocks = soup.select(".predloj-bank-bloks .items")

            # fallback
            if not branch_blocks:

                branch_blocks = soup.select(".predloj-bank-bloks")

            if not branch_blocks:

                log("🛑 no branch blocks")

                break

            added = 0

            new_page_addresses = set()

            # ==========================================
            # 💣 PARSE BLOCKS
            # ==========================================
            for block in branch_blocks:

                try:

                    # ==========================================
                    # 💣 FULL BLOCK TEXT
                    # ==========================================
                    block_text = clean_text(
                        block.get_text(
                            " ",
                            strip=True,
                        )
                    )

                    # ==========================================
                    # 💣 INVALID BLOCKS
                    # ==========================================
                    if "Адрес" not in block_text:

                        continue

                    if "Банкомат" in block_text:

                        continue

                    if len(block_text) < 20:

                        continue

                    # ==========================================
                    # 💣 BRANCH NAME
                    # ==========================================
                    branch_name = None

                    title = block.select_one(".predloj-bank-top a span")

                    if title:

                        branch_name = clean_text(
                            title.get_text(
                                " ",
                                strip=True,
                            )
                        )

                    # ==========================================
                    # 💣 DEFAULT VALUES
                    # ==========================================
                    address = None
                    city = None
                    phone = None

                    # ==========================================
                    # 💣 INFO BLOCKS
                    # ==========================================
                    info_blocks = block.select(".predloj-bank-text")

                    for info in info_blocks:

                        spans = info.select("span")

                        if len(spans) < 2:

                            continue

                        label = clean_text(
                            spans[0].get_text(
                                " ",
                                strip=True,
                            )
                        ).lower()

                        value = clean_text(
                            spans[1].get_text(
                                " ",
                                strip=True,
                            )
                        )

                        if not value:

                            continue

                        # ==========================================
                        # 💣 ADDRESS
                        # ==========================================
                        if "адрес" in label:

                            address = value

                        # ==========================================
                        # 💣 CITY
                        # ==========================================
                        elif "город" in label:

                            city = value

                        # ==========================================
                        # 💣 PHONE
                        # ==========================================
                        elif "телефон" in label or "контакт" in label:

                            phone = value

                    # ==========================================
                    # 💣 FALLBACK ADDRESS
                    # ==========================================
                    if not address:

                        match = re.search(
                            r"(г\..+)",
                            block_text,
                            re.IGNORECASE,
                        )

                        if match:

                            address = clean_text(match.group(1))

                    # ==========================================
                    # 💣 VALIDATION
                    # ==========================================
                    if not address:

                        continue

                    if len(address) < 8:

                        continue

                    # ==========================================
                    # 💣 HARD NORMALIZE
                    # ==========================================
                    key = normalize_text(address)

                    if not key:

                        continue

                    # ==========================================
                    # 💣 GLOBAL DEDUP
                    # ==========================================
                    if key in seen_addresses:

                        continue

                    seen_addresses.add(key)

                    new_page_addresses.add(key)

                    # ==========================================
                    # 💣 GEO PLACEHOLDER
                    # ==========================================
                    lat = None
                    lng = None

                    branches.append(
                        {
                            "name": branch_name,
                            "address": address,
                            "city": city,
                            "phone": phone,
                            "lat": lat,
                            "lng": lng,
                        }
                    )

                    added += 1

                except Exception as e:

                    log(f"⚠️ branch block error: " f"{e}")

            log(f"🏦 found on page: {added}")

            # ==========================================
            # 💣 DUPLICATE PAGE STOP
            # ==========================================
            if len(new_page_addresses) == 0:

                duplicate_pages += 1

                log("🛑 duplicate branch page")

            else:

                duplicate_pages = 0

            if duplicate_pages >= 1:

                break

            # ==========================================
            # 💣 PAGINATION
            # ==========================================
            pagination = soup.select_one(".pagination")

            if not pagination:

                log("🛑 no pagination")

                break

            next_btn = None

            for a in pagination.find_all(
                "a",
                href=True,
            ):

                txt = clean_text(
                    a.get_text(
                        " ",
                        strip=True,
                    )
                ).lower()

                href = str(a.get("href") or "")

                # ==========================================
                # 💣 REAL NEXT BUTTON
                # ==========================================
                if "вперед" in txt or "next" in txt:

                    next_btn = href

                    break

            # ==========================================
            # 💣 NO NEXT PAGE
            # ==========================================
            if not next_btn:

                log("🛑 last branch page")

                break

            page_num += 1

        log(f"🏦 branches parsed: " f"{len(branches)}")

    except Exception as e:

        log(f"⚠️ branch parse error: {e}")

    return branches
