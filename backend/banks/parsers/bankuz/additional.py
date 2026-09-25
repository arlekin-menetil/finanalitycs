from bs4 import BeautifulSoup
from typing import Any
import re

from .shared.browser import safe_goto
from .shared.normalization import clean_text
from .shared.logger import log


# ==========================================
# 🔥 ADDITIONAL FIELDS
# ==========================================
def parse_additional_fields(page, url):

    data: dict[str, Any] = {
        "requirements": None,
        "fee": None,
        "loan_type": "mortgage",
        "real_online": False,
        "subtype": None,
        "government_program": False,
    }

    try:

        # ==========================================
        # 💣 SAFE OPEN
        # ==========================================
        if not safe_goto(page, url):

            return data

        try:

            page.wait_for_load_state(
                "domcontentloaded",
                timeout=7000,
            )

        except:

            log("⚠️ load timeout — continue")

        try:

            page.wait_for_selector(
                "body",
                timeout=7000,
            )

        except:

            pass

        # ==========================================
        # 💣 HTML
        # ==========================================
        html = page.content()

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

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
        # 💣 TEXT COLLECTION
        # ==========================================
        blocks = soup.select("div, p, li, span, td")

        texts = []

        for block in blocks:

            try:

                txt = clean_text(
                    block.get_text(
                        " ",
                        strip=True,
                    )
                )

                if not txt:
                    continue

                if len(txt) < 20:
                    continue

                if len(txt) > 500:
                    continue

                texts.append(txt)

            except:

                continue

        # ==========================================
        # 💣 FINAL TEXT
        # ==========================================
        text = " ".join(texts)

        text = clean_text(text)

        lower = text.lower()

        # ==========================================
        # 💣 CUT GARBAGE
        # ==========================================
        garbage_markers = [
            "мобильное приложение",
            "подписаться",
            "курсы валют",
            "p2p переводы",
            "все кредиты",
            "другие предложения",
            "bank.uz",
        ]

        for marker in garbage_markers:

            if marker in lower:

                lower = lower.split(marker)[0]

        # ==========================================
        # 💣 REQUIREMENTS
        # ==========================================
        requirement_patterns = [
            r"(необходимые документы[^.]{0,500})",
            r"(требования[^.]{0,500})",
            r"(для оформления[^.]{0,500})",
            r"(заемщик[^.]{0,500})",
        ]

        for pattern in requirement_patterns:

            match = re.search(
                pattern,
                lower,
                re.IGNORECASE,
            )

            if match:

                req = clean_text(match.group(1))

                if len(req) > 15:

                    data["requirements"] = req[:1000]

                    break

        # ==========================================
        # 💣 FEE
        # ==========================================
        fee_patterns = [
            r"(комиссия[^.]{0,150})",
            r"(единовременный платеж[^.]{0,150})",
            r"(плата за оформление[^.]{0,150})",
        ]

        for pattern in fee_patterns:

            match = re.search(
                pattern,
                lower,
                re.IGNORECASE,
            )

            if match:

                fee = clean_text(match.group(1))

                if len(fee) > 5:

                    data["fee"] = fee

                    break

        # ==========================================
        # 💣 SUBTYPE DETECTION
        # ==========================================
        if any(
            x in lower
            for x in [
                "новострой",
                "первичн",
                "new building",
            ]
        ):

            data["subtype"] = "new_building"

        elif any(
            x in lower
            for x in [
                "вторич",
                "secondary",
            ]
        ):

            data["subtype"] = "secondary_market"

        elif any(
            x in lower
            for x in [
                "семейн",
                "молодая семья",
                "young family",
            ]
        ):

            data["subtype"] = "family"

        elif any(
            x in lower
            for x in [
                "льгот",
                "субсид",
                "госпрограмм",
                "государствен",
            ]
        ):

            data["subtype"] = "subsidized"

            data["government_program"] = True

        # ==========================================
        # 💣 ONLINE
        # ==========================================
        online_keywords = [
            "онлайн",
            "оформить онлайн",
            "онлайн заявка",
            "заявка онлайн",
            "online application",
        ]

        data["real_online"] = any(x in lower for x in online_keywords)

    except Exception as e:

        log(f"⚠️ additional parse error: {e}")

    return data
