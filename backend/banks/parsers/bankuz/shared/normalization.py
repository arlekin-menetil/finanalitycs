import re


def clean_text(text):

    return re.sub(
        r"\s+",
        " ",
        text or "",
    ).strip()


def normalize_text(val):

    if not val:
        return ""

    return re.sub(
        r"\s+",
        " ",
        val.strip().lower(),
    )


def extract_bank_from_name(text):

    if not text:
        return None

    text = text.lower()

    BANK_KEYWORDS = {
        "tbc": "TBC Bank",
        "ipak yuli": "Ipak Yuli Bank",
        "kapital": "Kapitalbank",
        "asaka": "Asakabank",
        "agro": "Agrobank",
        "davr": "Davr Bank",
        "orient": "Orient Finans Bank",
        "hamkor": "Hamkorbank",
        "aloqa": "Aloqabank",
        "xalq": "Xalq Banki",
        "mikrokredit": "Mikrokreditbank",
        "infin": "Infinbank",
        "trast": "Trastbank",
        "uzprom": "Uzpromstroybank",
        "ipoteka": "Ipoteka Bank",
        "nbu": "National Bank of Uzbekistan",
        "turon": "Turon Bank",
        "asia alliance": "Asia Alliance Bank",
        "apex": "Apex Bank",
        "universal": "Universal Bank",
        "tenge": "Tenge Bank",
    }

    for key, value in BANK_KEYWORDS.items():

        if key in text:
            return value

    return None
