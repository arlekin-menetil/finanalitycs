import re
import unicodedata


# =========================
# 💣 TEXT NORMALIZATION
# =========================

def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = unicodedata.normalize("NFKD", str(text))
    text = "".join([c for c in text if not unicodedata.combining(c)])
    text = text.lower().strip()

    # 🔥 FIX: unify Cyrillic variants early (global consistency layer)
    text = text.replace("й", "и")
    text = text.replace("ё", "е")

    return text


def normalize_key(text: str) -> str:
    if not text:
        return ""

    text = normalize_text(text)

    # 🔥 FIX: keep letters consistent but avoid breaking Cyrillic/Latin mix
    text = re.sub(r"[^\w\sа-яa-z0-9]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================
# 💣 ALIAS SAFE NORMALIZATION
# =========================

def normalize_alias_key(text: str) -> str:
    if not text:
        return ""

    text = normalize_text(text)

    # 🔥 extra safety: collapse spacing + unify variants
    text = re.sub(r"\s+", " ", text).strip()

    return text


# =========================
# 💣 RATE PARSER
# =========================

def extract_rate_from_text(text: str):
    if not text:
        return None, None, False

    text = normalize_text(text).replace(",", ".")

    try:
        if "0%" in text or "беспроцент" in text:
            return 0.0, 0.0, True

        match_range = re.findall(r"(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)\s*%", text)
        if match_range:
            return float(match_range[0][0]), float(match_range[0][1]), True

        match_min = re.findall(r"от\s*(\d+\.?\d*)\s*%", text)
        if match_min:
            val = float(match_min[0])
            return val, val, True

        match_max = re.findall(r"до\s*(\d+\.?\d*)\s*%", text)
        if match_max:
            val = float(match_max[0])
            return val, val, True

        match_single = re.findall(r"(\d+\.?\d*)\s*%", text)
        if match_single:
            val = float(match_single[0])
            return val, val, True

    except Exception:
        pass

    return None, None, False


def normalize_rate(rate):
    if rate is None:
        return None, None, False

    try:
        text = normalize_text(str(rate)).replace(",", ".")

        numbers = re.findall(r"\d+\.?\d*", text)
        numbers = [float(n) for n in numbers if 0 < float(n) < 200]

        if not numbers:
            return None, None, False

        min_rate = min(numbers)
        max_rate = max(numbers)

        # 🔥 FIX: safer detection of monthly rates
        if any(x in text for x in ["в месяц", "/мес", "per month"]):
            min_rate *= 12
            max_rate *= 12

        return round(min_rate, 2), round(max_rate, 2), True

    except Exception:
        return None, None, False


# =========================
# 💣 PRODUCT NAME
# =========================

def normalize_product_name(name: str) -> str:
    if not name:
        return None

    name = normalize_text(name)

    name = re.sub(r"\b(кредит|loan|credit|банк|bank)\b", "", name)
    name = re.sub(r"[^\w\s%а-яa-z0-9]", " ", name)
    name = re.sub(r"\s+", " ", name)

    return name.strip()


# =========================
# 💣 BANK ALIASES (FIXED CORE)
# =========================

BANK_ALIASES = {
    # 🔥 SQB — CANONICAL
    "sqb": "SQB",
    "uzpsb": "SQB",
    "uzprom": "SQB",
    "uzpromstroy": "SQB",
    "uzpromstroybank": "SQB",
    "узпромстройбанк": "SQB",

    # 🔥 TOP BANKS
    "hamkor": "Hamkorbank",
    "aloqa": "Aloqabank",
    "tbc": "TBC Bank",
    "kapital": "Kapitalbank",
    "ipak yuli": "Ipak Yuli Bank",
    "ipakyuli": "Ipak Yuli Bank",
    "ipoteka": "Ipoteka Bank",
    "asaka": "Asakabank",
    "agro": "Agrobank",
    "orient": "Orient Finans Bank",
    "davr": "Davr Bank",
    "infin": "Infinbank",
    "anor": "Anor Bank",
    "tenge": "Tenge Bank",
    "saderat": "Saderat Bank",
    "ziraat": "Ziraat Bank",
    "kdb": "KDB Bank",
    "poytaxt": "Poytaxt Bank",
    "trast": "Trastbank",
    "turon": "Turon Bank",
    "universal": "Universal Bank",

    # 🔥 PROBLEM BANKS
    "xalq banki": "Xalq Banki",
    "xalq": "Xalq Banki",

    "mikrokreditbank": "Mikrokreditbank",
    "mikrokredit": "Mikrokreditbank",

    "mybank": "MyBank",

    "apexbank": "APEXBANK",
    "apex": "APEXBANK",

    "asia alliance bank": "Asia Alliance Bank",
    "asia alliance": "Asia Alliance Bank",

    # 🔥 NBU
    "nbu": "NBU",
    "национальный банк узбекистана": "NBU",
    "национальный банк": "NBU",

    # 🔥 OTHERS
    "uzum": "Uzum Bank",
    "octo": "Octobank",
    "brb": "BRB",
    "garant": "Garant Bank",
}


INVALID_BANK_VALUES = {
    "img", "logo", "bank", "none", "null", "",
    "onlayn", "online"
}


def clean_bank_raw(name: str) -> str:
    if not name:
        return ""

    name = normalize_text(name)

    name = re.sub(r"[\"'«»]", "", name)
    name = re.sub(r"\b(банк|bank|logo|логотип|ao|ooo|akb)\b", "", name)
    name = re.sub(r"[^a-zа-я0-9\s]", " ", name)
    name = re.sub(r"\s+", " ", name)

    return name.strip()


# =========================
# 💣 FIXED BANK NORMALIZER (FINAL)
# =========================

def normalize_bank_name(name: str) -> str:
    if not name:
        return None

    raw = normalize_alias_key(name)
    raw_key = normalize_key(raw)

    # 🔥 1. DIRECT ALIAS MATCH (STRICT MATCH, FIXED)
    for key, value in BANK_ALIASES.items():
        key_norm = normalize_alias_key(key)

        # FIX: avoid substring false positives
        if raw_key == normalize_key(key_norm):
            return value

    clean = clean_bank_raw(name)

    if clean in INVALID_BANK_VALUES or len(clean) < 2:
        return None

    if clean in BANK_ALIASES:
        return BANK_ALIASES[clean]

    words = clean.split()

    if len("".join(words)) < 4:
        return None

    return " ".join([w.capitalize() for w in words])


# =========================
# 💣 TYPE DETECTOR
# =========================

def detect_product_type(name: str, item: dict = None) -> str:
    if not name:
        return "loan"

    n = normalize_text(name)

    if "рассроч" in n:
        return "installment"

    if any(x in n for x in ["займ", "micro", "mini", "express"]):
        return "micro"

    if any(x in n for x in ["авто", "kia", "byd", "toyota", "haval", "changan"]):
        return "auto"

    if "ипотек" in n:
        return "mortgage"

    if any(x in n for x in ["business", "biznes", "tadbirkor"]):
        return "business"

    return "loan"


def detect_category(name: str) -> str:
    if not name:
        return "loan"

    n = normalize_text(name)

    if "ипотек" in n:
        return "mortgage"

    if "авто" in n:
        return "auto"

    if "микро" in n or "займ" in n:
        return "micro"

    return "loan"


# =========================
# 💣 MAIN NORMALIZER
# =========================

def normalize_item(item: dict) -> dict:

    raw_name = item.get("name")

    if not raw_name or len(str(raw_name).strip()) < 2:
        return None

    # =========================
    # 🏦 BANK
    # =========================
    bank_raw = item.get("bank")
    bank = normalize_bank_name(bank_raw)

    if not bank:
        bank = normalize_bank_name(raw_name)

    if not bank:
        return None  # 🔥 FIX: avoid fake "Unknown Bank" pollution

    # =========================
    # 🏷 NAME
    # =========================
    name = re.sub(r"\s+", " ", raw_name.strip())

    # =========================
    # 💰 RATE
    # =========================
    raw_rate = item.get("rate") or item.get("interest_rate")
    min_rate, max_rate, has_rate = normalize_rate(raw_rate)

    if not has_rate:
        text_block = f"{raw_name or ''} {item.get('description') or ''}"
        min_rate, max_rate, has_rate = extract_rate_from_text(text_block)

    # =========================
    # 🧠 TYPE
    # =========================
    product_type = detect_product_type(raw_name, item)
    category = detect_category(raw_name)

    # =========================
    # 🔑 KEY
    # =========================
    normalized_name = normalize_key(
        f"{bank}_{normalize_product_name(raw_name)}"
    )

    return {
        "bank": bank,
        "name": name,

        "interest_rate": min_rate,
        "min_rate": min_rate,
        "max_rate": max_rate,
        "has_rate": has_rate,

        "product_type": product_type,
        "aggregated_key": category,
        "normalized_name": normalized_name,

        "max_amount": item.get("max_amount"),
        "term": item.get("term"),
        "description": item.get("description"),

        "source_url": item.get("source_url"),
        "bank_url": item.get("bank_url"),
    }