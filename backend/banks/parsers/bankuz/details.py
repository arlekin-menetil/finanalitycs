from bs4 import BeautifulSoup
import re

from .shared.normalization import (
    clean_text,
    normalize_text,
)

from .shared.parsing import (
    parse_rate,
    parse_amount,
    parse_term,
)

from .shared.logger import log


# ==========================================
# 💣 SAFE SELECT
# ==========================================
def safe_select_text(
    soup,
    selectors,
    min_length=0,
):

    for selector in selectors:

        try:

            el = soup.select_one(selector)

            if not el:
                continue

            text = clean_text(
                el.get_text(
                    " ",
                    strip=True,
                )
            )

            if len(text) < min_length:
                continue

            return text

        except Exception:

            pass

    return None


# ==========================================
# 💣 EXTRACT DESCRIPTION
# ==========================================
def extract_description(
    soup,
    title=None,
    short_info=None,
):

    description_selectors = [
        ".organization-bottom-block",
        ".credit-single-body",
        ".credit-main-info",
        ".news-detail",
        ".bank_page",
        ".bank-data",
        ".container",
    ]

    for selector in description_selectors:

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

            if len(text) < 200:
                continue

            # ==========================================
            # 💣 REMOVE TRASH
            # ==========================================
            trash_patterns = [
                "Все продукты",
                "Филиалы и Банкоматы",
                "Другие предложения",
                "Похожие продукты",
                "Читайте также",
                "Поделиться",
                "Реклама",
            ]

            for pattern in trash_patterns:

                idx = text.find(pattern)

                if idx != -1:

                    text = text[:idx]

            # ==========================================
            # 💣 CLEAN DESCRIPTION
            # ==========================================

            parts = []

            cleaned_text = text

            # ------------------------------------------
            # Убираем название кредита
            # ------------------------------------------
            if title:

                try:

                    cleaned_text = cleaned_text.replace(
                        title,
                        "",
                        1,
                    )

                except Exception:

                    pass

            # ------------------------------------------
            # Убираем краткую сводку
            # (Сумма, Ставка, Валюта и т.д.)
            # ------------------------------------------
            for item in short_info or []:

                try:

                    cleaned_text = cleaned_text.replace(
                        item,
                        "",
                        1,
                    )

                except Exception:

                    pass

            # ------------------------------------------
            # Удаляем лишние пробелы
            # ------------------------------------------
            cleaned_text = re.sub(
                r"[ \t]+",
                " ",
                cleaned_text,
            )

            cleaned_text = clean_text(cleaned_text)

            parts.append(cleaned_text)

            description = clean_text(
                "\n\n".join(
                    filter(
                        None,
                        parts,
                    )
                )
            )

            # ==========================================
            # 💣 FINAL CLEANUP
            # ==========================================

            description = re.sub(
                r"(О кредите)\s+\1",
                r"\1",
                description,
                flags=re.I,
            )

            description = re.sub(
                r"\s{2,}",
                " ",
                description,
            )

            description = description.strip()

            # слишком короткие описания пропускаем
            if len(description) < 100:

                continue

            # ограничиваем размер
            return description[:12000]

        except Exception as e:

            log(f"⚠️ description selector " f"failed: {e}")

    return None


# ==========================================
# 💣 SECTION EXTRACTOR
# ==========================================
def extract_section(
    text,
    labels,
):

    if isinstance(labels, str):

        labels = [labels]

    for label in labels:

        try:

            pattern = rf"{label}" rf"\s*[:\n]?\s*" rf"([\s\S]*?)" rf"(\n[A-ЯЁA-Z]|$)"

            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:

                value = clean_text(match.group(1))

                if value:

                    return value

        except Exception:

            pass

    return None


# ==========================================
# 💣 CAPTCHA DETECTOR
# ==========================================
def is_real_captcha(html):

    lower_html = html.lower()

    captcha_markers = [
        "verify you are human",
        "cf-challenge",
        "security check",
        "checking your browser",
        "please wait while we verify",
    ]

    hits = sum(1 for marker in captcha_markers if marker in lower_html)

    return hits >= 2


# ==========================================
# 💣 404 DETECTOR
# ==========================================
def is_real_404(
    html,
    title="",
):

    lower_html = html.lower()
    title_lower = title.lower()

    markers = [
        "страница не найдена",
        "page not found",
        "ошибка 404",
    ]

    return any(marker in lower_html or marker in title_lower for marker in markers)


# ==========================================
# 💣 MAIN DETAIL PARSER
# ==========================================
def parse_product_detail(
    page,
    url,
):

    data = {
        "_html": None,
        "_soup": None,
        "name": None,
        "description": None,
        "bank_name": None,
        "bank_url": None,
        "bank_address": None,
        "bank_phone": None,
        "branch_url": None,
        "branches": [],
        "image_url": None,
        "structured": {
            "rate_min": None,
            "rate_max": None,
            "amount_max": None,
            "amount_min": None,
            "term": None,
            "currency": None,
            "payment_type": None,
            "collateral": None,
            "requirements": None,
            "updated_at": None,
        },
    }

    try:

        # ==========================================
        # 💣 OPEN PAGE
        # ==========================================
        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000,
        )

        try:

            page.wait_for_load_state(
                "networkidle",
                timeout=10000,
            )

        except Exception:

            pass

        try:

            page.wait_for_timeout(1500)

        except Exception:

            pass

        # ==========================================
        # 💣 HTML
        # ==========================================
        html = page.content()

        data["_html"] = html

        # ==========================================
        # 💣 PAGE TITLE
        # ==========================================
        page_title = ""

        try:

            page_title = page.title() or ""

        except Exception:

            pass

        # ==========================================
        # 💣 CAPTCHA CHECK
        # ==========================================
        if is_real_captcha(html):

            log("🚫 REAL captcha detail page")

            return data

        # ==========================================
        # 💣 404 CHECK
        # ==========================================
        if is_real_404(
            html=html,
            title=page_title,
        ):

            log("⚠️ REAL 404 detail page")

            return data

        # ==========================================
        # 💣 SOUP
        # ==========================================
        try:

            soup = BeautifulSoup(
                html,
                "lxml",
            )

        except Exception:

            soup = BeautifulSoup(
                html,
                "html.parser",
            )

        data["_soup"] = soup

        # ==========================================
        # 💣 REMOVE TRASH
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
        # 💣 GLOBAL TEXT
        # ==========================================
        text = clean_text(soup.get_text(" "))

        lower = text.lower()

        # ==========================================
        # 💣 TITLE
        # ==========================================
        title = safe_select_text(
            soup,
            [
                "h1",
                ".credit-title",
                ".bank-title",
            ],
            min_length=2,
        )

        if title:

            data["name"] = title

        # ==========================================
        # 💣 SHORT INFO
        # ==========================================
        short_info = []
        short_info_dict = {}

        try:

            info_selectors = [
                ".credit-info",
                ".credit-short-info",
                ".table-card-offers",
            ]

            for selector in info_selectors:

                container = soup.select_one(selector)

                if not container:
                    continue

                info_blocks = container.select(".credit-info-text")

                for item in info_blocks:

                    spans = item.find_all("span")

                    if len(spans) < 2:
                        continue

                    key = clean_text(
                        spans[0].get_text(
                            " ",
                            strip=True,
                        )
                    )

                    value = clean_text(
                        spans[1].get_text(
                            " ",
                            strip=True,
                        )
                    )

                    if not key or not value:
                        continue

                    short_info.append(f"{key}: {value}")

                    short_info_dict[key.lower()] = value

                if short_info:
                    break

        except Exception as e:

            log(f"⚠️ short info error: {e}")

        log(f"SHORT INFO: {short_info}")
        log(f"SHORT INFO DICT: {short_info_dict}")

        # ==========================================
        # 💣 DESCRIPTION
        # ==========================================
        try:

            description = extract_description(
                soup=soup,
                title=title,
                short_info=short_info,
            )

            if description:

                data["description"] = description

                log("✅ description parsed")

            else:

                log("❌ description block " "not found")

        except Exception as e:

            log(f"⚠️ description parse " f"error: {e}")

        # ==========================================
        # 💣 BANK
        # ==========================================
        try:

            bank_link = None

            bank_selectors = [
                "a[href*='/organization/']",
                "a[href*='/org/']",
                "a[href*='/bank/']",
            ]

            for selector in bank_selectors:

                bank_link = soup.select_one(selector)

                if bank_link:
                    break

            if bank_link:

                bank_name = clean_text(
                    bank_link.get_text(
                        " ",
                        strip=True,
                    )
                )

                if bank_name:

                    data["bank_name"] = bank_name

                href = str(bank_link.get("href") or "").strip()

                if href:

                    if href.startswith("/"):

                        href = "https://bank.uz" + href

                    data["bank_url"] = href

        except Exception as e:

            log(f"⚠️ bank parse error: " f"{e}")

        # ==========================================
        # 💣 IMAGE
        # ==========================================
        try:

            image_selectors = [
                ".organization-logo img",
                ".bank-logo img",
                ".credit-main-img img",
                ".table-card-offers-block1-img img",
                ".bank-card img",
                ".credit-img img",
            ]

            for selector in image_selectors:

                img = soup.select_one(selector)

                if not img:
                    continue

                src = (
                    str(img.get("src") or "").strip()
                    or str(img.get("data-src") or "").strip()
                )

                if not src:
                    continue

                if "logo.png" in src:
                    continue

                if src.startswith("/"):

                    src = "https://bank.uz" + src

                if src.startswith("http"):

                    data["image_url"] = src

                    break

        except Exception as e:

            log(f"⚠️ image parse error: " f"{e}")

        # ==========================================
        # 💣 RATE
        # ==========================================

        rate_text = short_info_dict.get("ставка")

        if not rate_text:

            rate_text = extract_section(
                text,
                [
                    "Процентная ставка",
                    "Ставка",
                    "Мин. ставка",
                    "Годовая ставка",
                ],
            )

        if rate_text:

            rate = parse_rate(rate_text)

            if rate is not None:

                data["structured"]["rate_min"] = rate
                data["structured"]["rate_max"] = rate

                log(
                    f"RATE FOUND: {rate} "
                    f"(source: {'short_info' if short_info_dict.get('ставка') else 'text'})"
                )

        # ==========================================
        # 💣 AMOUNT
        # ==========================================

        amount_text = short_info_dict.get(
            "минимальная сумма"
        )

        if amount_text:

            amount = parse_amount(amount_text)

            if amount:

                data["structured"]["amount_min"] = amount

                log(
                    f"AMOUNT FOUND: {amount} "
                    f"(source: short_info)"
                )

        if not data["structured"]["amount_min"]:

            amount_patterns = [
                r"Мин\.\s*сумма\s*:\s*([^\n\.]{1,100})",
                r"Минимальная\s*сумма\s*:\s*([^\n\.]{1,100})",
                r"Минимальный\s*взнос\s*:\s*([^\n\.]{1,100})",
                r"Первоначальный\s*взнос\s*:\s*([^\n\.]{1,100})",
            ]

            for pattern in amount_patterns:

                match = re.search(
                    pattern,
                    text,
                    re.IGNORECASE,
                )

                if match:

                    amount_text = clean_text(
                        match.group(1)
                    )

                    amount = parse_amount(
                        amount_text
                    )

                    if amount:

                        data["structured"]["amount_min"] = amount

                        break

        max_amount_patterns = [
            r"Максимальная\s*сумма\s*:\s*([^\n\.]{1,100})",
            r"Макс\.\s*сумма\s*:\s*([^\n\.]{1,100})",
        ]

        for pattern in max_amount_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:

                amount_text = clean_text(
                    match.group(1)
                )

                amount = parse_amount(
                    amount_text
                )

                if amount:

                    data["structured"]["amount_max"] = amount

                    break

        log(
            f"AMOUNT MIN: "
            f"{data['structured']['amount_min']}"
        )

        log(
            f"AMOUNT MAX: "
            f"{data['structured']['amount_max']}"
        )
        # ==========================================
        # 💣 TERM
        # ==========================================
        term_text = extract_section(
            text,
            [
                "Срок",
                "Период",
            ],
        )

        if term_text:

            term = parse_term(term_text)

            if term:

                data["structured"]["term"] = term

         # ==========================================
        # 💣 CURRENCY
        # ==========================================

        currency_text = (
            short_info_dict.get("валюта")
            or ""
        ).lower()

        # Если в short_info валюты нет —
        # используем старую логику
        if not currency_text:

            currency_sources = [
                data.get("description") or "",
                text,
                " ".join(short_info),
            ]

            currency_text = (
                " ".join(currency_sources)
            ).lower()

        if any(
            x in currency_text
            for x in [
                "евро",
                " eur ",
                "eur",
                "€",
            ]
        ):

            data["structured"]["currency"] = "EUR"

        elif any(
            x in currency_text
            for x in [
                "долл",
                "доллар",
                " usd ",
                "usd",
                "$",
            ]
        ):

            data["structured"]["currency"] = "USD"

        elif any(
            x in currency_text
            for x in [
                "сум",
                " uzs ",
                "uzs",
                "uzbek sum",
            ]
        ):

            data["structured"]["currency"] = "UZS"

        log(
            f"CURRENCY FOUND: "
            f"{data['structured']['currency']} "
            f"(source: {'short_info' if short_info_dict.get('валюта') else 'fallback'})"
        )
        # ==========================================
        # 💣 PAYMENT TYPE
        # ==========================================
        payment_match = re.search(
            r"(?:Уплата процентов|Выплата процентов)\s*:\s*(.*?)\s*Валюта",
            text,
            re.IGNORECASE,
        )

        if payment_match:

            payment_value = clean_text(payment_match.group(1))

            if payment_value:

                data["structured"]["payment_type"] = payment_value
        # ==========================================
        # 💣 REQUIREMENTS
        # ==========================================
        requirements_text = extract_section(
            text,
            [
                "Необходимые документы",
                "Документы",
                "Требования",
            ],
        )

        if requirements_text:

            data["structured"]["requirements"] = requirements_text[:1500]

        # ==========================================
        # 💣 UPDATED DATE
        # ==========================================
        upd = re.search(
            r"(\d{2}\.\d{2}\.\d{4})",
            text,
        )

        if upd:

            data["structured"]["updated_at"] = upd.group(1)

    except Exception as e:

        log(f"⚠️ detail parse error: " f"{e}")

    log(f"DEBUG STRUCTURED: " f"{data['structured']}")

    return data
