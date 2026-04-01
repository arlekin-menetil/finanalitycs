import re
import requests
from bs4 import BeautifulSoup
from decimal import Decimal

from banks.models import Bank, BankProduct


URL = "https://depozit.uz/"


# =========================
# 💣 BANK NORMALIZATION
# =========================

BANK_MAPPING = {
    "ipak": "Ipak Yo‘li",
    "ipotek": "Ipoteka-bank",
    "agro": "Agrobank",
    "asaka": "Asakabank",
    "ziraat": "Ziraat Bank Uzbekistan",
    "xalq": "Xalq Bank",
    "kapital": "Kapitalbank",
    "anor": "Anor Bank",
}


def normalize_bank(name: str):
    name_lower = name.lower()

    for key, value in BANK_MAPPING.items():
        if key in name_lower:
            return value

    return name.strip()


# =========================
# UTILS
# =========================

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_rate(text: str):
    match = re.search(r"(\d+[.,]?\d*)\s*%", text)
    if match:
        return float(match.group(1).replace(",", "."))
    return None


def is_valid_deposit(text: str):

    text_lower = text.lower()

    if "%" not in text:
        return False

    keywords = ["вклад", "депозит", "omонат"]

    if not any(k in text_lower for k in keywords):
        return False

    banned = [
        "новости",
        "курс",
        "калькулятор",
        "сравнение",
        "банки узбекистана"
    ]

    if any(b in text_lower for b in banned):
        return False

    return True


def split_bank_and_product(text: str):

    # 🥇 если есть тире
    if "—" in text:
        left, right = text.split("—", 1)
        return left.strip(), right.strip()

    # 🥈 fallback
    parts = text.split()

    if len(parts) < 3:
        return None, None

    bank = parts[0]
    product = " ".join(parts[1:])

    return bank, product


def extract_product_name(product_text: str):

    parts = product_text.split()

    name_parts = []

    for p in parts:
        if "%" in p:
            break
        name_parts.append(p)

    return " ".join(name_parts)


# =========================
# MAIN PARSER
# =========================

def parse_depozi():

    print("🚀 Parsing depozit.uz...")

    try:
        res = requests.get(
            URL,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
    except Exception as e:
        print("❌ Request error:", e)
        return 0

    soup = BeautifulSoup(res.text, "html.parser")

    blocks = soup.find_all("div")

    created = 0

    for block in blocks:

        try:
            text = clean_text(block.get_text(" ", strip=True))

            if not text or len(text) < 20:
                continue

            if not is_valid_deposit(text):
                continue

            rate = extract_rate(text)
            if not rate:
                continue

            bank_name, product_text = split_bank_and_product(text)

            if not bank_name or not product_text:
                continue

            bank_name = normalize_bank(bank_name)

            name = extract_product_name(product_text)

            if not name or len(name) < 5:
                continue

            # =========================
            # BANK
            # =========================

            bank, _ = Bank.objects.get_or_create(
                short_name=bank_name,
                defaults={"name": bank_name}
            )

            # =========================
            # DUPLICATE CHECK
            # =========================

            if BankProduct.objects.filter(
                bank=bank,
                name=name
            ).exists():
                continue

            # =========================
            # CREATE
            # =========================

            BankProduct.objects.create(
                bank=bank,
                name=name,
                interest_rate=Decimal(str(rate)),
                is_active=True,
                source_url=URL
            )

            created += 1

            print(f"✅ {bank_name} — {name} ({rate}%)")

        except Exception as e:
            print("❌ Error:", e)

    print(f"🎉 depozit done: {created}")

    return created