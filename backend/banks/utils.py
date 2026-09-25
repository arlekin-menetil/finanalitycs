import re


# =========================
# 💣 CLEAN STRING
# =========================

def clean_string(text):
    if not text:
        return ""

    text = text.strip()
    text = re.sub(r"\s+", " ", text)

    return text


# =========================
# 💣 NORMALIZE KEY PART
# =========================

def normalize_key_part(text: str) -> str:
    if not text:
        return ""

    text = text.lower().strip()

    text = text.replace("‘", "'").replace("`", "'")
    text = re.sub(r"[\"'«»]", "", text)

    text = re.sub(r"[-–—]", " ", text)
    text = re.sub(r"[^a-zа-я0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================
# 💣 SEMANTIC NORMALIZATION
# =========================

STOPWORDS = [
    "кредит",
    "займ",
    "ссуда",
    "для",
    "от",
    "банк",
    "лицам",
    "средств",
    "министерства",
    "финансов",
    "продукт",
]


SYNONYMS = {
    # cash
    "наличными": "cash",
    "потребительский": "cash",
    "consumer": "cash",

    # education
    "образовательный": "education",
    "образования": "education",
    "образовательные": "education",

    # mortgage
    "ипотека": "mortgage",
    "ипотечный": "mortgage",
    "новостройки": "mortgage",

    # auto
    "авто": "auto",
    "автокредит": "auto",
    "car": "auto",

    # micro
    "микрозайм": "micro",
    "микро": "micro",
    "micro": "micro",
}


def normalize_semantic(text: str) -> str:
    if not text:
        return ""

    text = normalize_key_part(text)

    # 💣 УБИВАЕМ МУСОРНЫЕ ХВОСТЫ (очень важно)
    text = re.sub(
        r"(biznes|yangicha|imkon|kelajak|yoshlar|agroko|birinchi|qadam|uchun)",
        "",
        text
    )

    words = text.split()

    result = []

    for word in words:
        if word in STOPWORDS:
            continue

        word = SYNONYMS.get(word, word)

        # короткие мусорные слова убираем
        if len(word) <= 2:
            continue

        result.append(word)

    return " ".join(result)


# =========================
# 💣 STRONG KEY (точный)
# =========================

def generate_unique_key(bank, name, rate=None):
    bank = normalize_key_part(bank)
    name = normalize_key_part(name)

    if not bank or not name:
        return None

    key = f"{bank}_{name}"

    if rate is not None:
        key += f"_{round(float(rate), 1)}"

    return key[:255]


# =========================
# 💣 SOFT KEY (умный)
# =========================

def generate_soft_key(bank, name):
    bank = normalize_key_part(bank)
    name = normalize_semantic(name)

    if not bank or not name:
        return None

    return f"{bank}_{name}"[:255]