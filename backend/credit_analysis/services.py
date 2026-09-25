import os
import re

from decimal import Decimal

import pdfplumber
from bs4 import BeautifulSoup


# ==========================================================
# NUMBERS
# ==========================================================

def normalize_number(value: str | None) -> Decimal:
    """
    Преобразует

    25 404 884.83
    25,404,884.83
    25 404 884

    в Decimal
    """

    if value is None:
        return Decimal("0")

    value = str(value)

    value = (
        value.replace("\xa0", "")
        .replace(" ", "")
        .replace(",", ".")
        .strip()
    )

    try:
        return Decimal(value)
    except Exception:
        return Decimal("0")


# ==========================================================
# PDF
# ==========================================================

def extract_pdf_text(file_path: str):

    text = ""

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

            text += "\n"

    return text


# ==========================================================
# HTML
# ==========================================================

def load_html(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:

        html = f.read()

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    return soup


# ==========================================================
# HTML TEXT
# ==========================================================

def extract_html_text(file_path):

    soup = load_html(file_path)

    return soup.get_text(
        separator=" ",
        strip=True
    )


# ==========================================================
# UNIVERSAL TEXT
# ==========================================================

def extract_text(file_path):

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_pdf_text(file_path)

    if ext in [".html", ".htm"]:
        return extract_html_text(file_path)

    raise ValueError(
        f"Unsupported extension {ext}"
    )


# ==========================================================
# REGEX SEARCH
# ==========================================================

def search(patterns, text):

    for pattern in patterns:

        m = re.search(
            pattern,
            text,
            flags=re.I | re.S
        )

        if m:
            return m.group(1)

    return None


# ==========================================================
# DECIMAL SEARCH
# ==========================================================

def search_decimal(patterns, text):

    value = search(patterns, text)

    return normalize_number(value)


# ==========================================================
# INTEGER SEARCH
# ==========================================================

def search_int(patterns, text):

    value = search(patterns, text)

    if not value:
        return 0

    value = re.sub(r"\D", "", value)

    if not value:
        return 0

    return int(value)


# ==========================================================
# SCORE FROM HTML
# ==========================================================

def extract_html_score(soup):
    """
    InfoKredit:

    <h2 id="score_text">273</h2>

    """

    node = soup.find(id="score_text")

    if node:

        try:
            return int(node.text.strip())
        except Exception:
            pass

    arrow = soup.find(id="score_arrow")

    if arrow:

        alt = arrow.get("alt")

        if alt:

            try:
                return int(
                    re.sub(r"\D", "", alt)
                )
            except Exception:
                pass

    return 0


# ==========================================================
# SCORE FROM TEXT
# ==========================================================

def extract_text_score(text):

    return search_int(

        [

            r"скоринговый балл[^0-9]{0,20}(\d+)",

            r"infoscore[^0-9]{0,20}(\d+)",

            r"credit score[^0-9]{0,20}(\d+)",

            r"score[^0-9]{0,20}(\d+)",

        ],

        text

    )
# ==========================================================
# RISK
# ==========================================================

def extract_risk(soup):

    text = soup.get_text(" ", strip=True)

    risk = search(

        [

            r"Класс оценки[^A-ZА-Я0-9]*([A-Z]\d)",

            r"Risk[^A-Z0-9]*([A-Z]\d)",

        ],

        text

    )

    if risk:
        return risk

    return ""


# ==========================================================
# SCORE VERSION
# ==========================================================

def extract_score_version(soup):

    text = soup.get_text(" ", strip=True)

    version = search(

        [

            r"Версия скоринга[^0-9]*([\d\.]+)",

            r"Version[^0-9]*([\d\.]+)",

        ],

        text

    )

    if version:
        return version

    return ""


# ==========================================================
# FULL NAME
# ==========================================================

def extract_full_name(soup):

    text = soup.get_text(" ", strip=True)

    value = search(

        [

            r"ФИО[^А-ЯA-Za-z0-9]*([А-ЯЁA-Z][^0-9]{5,80})",

            r"Клиент[^А-ЯA-Za-z0-9]*([А-ЯЁA-Z][^0-9]{5,80})",

        ],

        text

    )

    if value:
        return value.strip()

    return ""


# ==========================================================
# PASSPORT
# ==========================================================

def extract_passport(soup):

    text = soup.get_text(" ", strip=True)

    passport = search(

        [

            r"Паспорт[^A-Z0-9]*([A-Z]{2}\d{7})",

            r"Документ[^A-Z0-9]*([A-Z]{2}\d{7})",

        ],

        text

    )

    if passport:
        return passport

    return ""


# ==========================================================
# PHONE
# ==========================================================

def extract_phone(soup):

    text = soup.get_text(" ", strip=True)

    phone = search(

        [

            r"998\d{9}",

        ],

        text

    )

    if phone:
        return phone

    return ""


# ==========================================================
# INCOME
# ==========================================================

def extract_income(soup):

    text = soup.get_text(" ", strip=True)

    income = search_decimal(

        [

            r"Доход[^0-9]{0,20}([\d\s.,]+)",

            r"Ежемесячный доход[^0-9]{0,20}([\d\s.,]+)",

            r"Income[^0-9]{0,20}([\d\s.,]+)",

        ],

        text

    )

    return income


# ==========================================================
# TOTAL DEBT
# ==========================================================

def extract_total_debt(soup):

    total = Decimal("0")

    items = soup.find_all(text=re.compile("Остаток всей задолженности"))

    for item in items:

        parent = item.parent

        if parent:

            text = parent.get_text(" ", strip=True)

            value = search_decimal(

                [

                    r"([\d\s]+\.\d+)",

                    r"([\d\s]+)",

                ],

                text

            )

            total += value

    return total


# ==========================================================
# OVERDUE DEBT
# ==========================================================

def extract_overdue_debt(soup):

    total = Decimal("0")

    items = soup.find_all(text=re.compile("Просроченная задолженность"))

    for item in items:

        parent = item.parent

        if parent:

            text = parent.get_text(" ", strip=True)

            value = search_decimal(

                [

                    r"([\d\s]+\.\d+)",

                    r"([\d\s]+)",

                ],

                text

            )

            total += value

    return total


# ==========================================================
# ACTIVE CONTRACTS
# ==========================================================

def extract_contracts(soup):

    text = soup.get_text(" ", strip=True)

    return len(

        re.findall(

            r"Договор",

            text,

            flags=re.I

        )

    )


# ==========================================================
# BANKS
# ==========================================================

def extract_banks(soup):

    text = soup.get_text(" ", strip=True)

    known_banks = [

        "Hamkorbank",
        "Aloqabank",
        "SQB",
        "Agrobank",
        "Ipoteka",
        "NBU",
        "Anor Bank",
        "Asakabank",
        "Kapitalbank",
        "Ipak Yuli",
        "Trastbank",
        "TBC",
        "TBC FIN SERVICE",
        "Davr Bank",
        "Xalq Bank",
        "Mikrokreditbank",
        "Orient Finans",
        "Asia Alliance",
        "Universal Bank",
        "Garant Bank",
        "Turonbank",
        "Madad Invest Bank",
        "Ravnaq Bank",
        "Poytaxt Bank",

    ]

    found = set()

    lower_text = text.lower()

    for bank in known_banks:

        if bank.lower() in lower_text:

            found.add(bank)

    patterns = [

        r"Кредитор[:\s]+([A-Za-zА-ЯЁ0-9 \-\"']{3,80})",

        r"Creditor[:\s]+([A-Za-zА-ЯЁ0-9 \-\"']{3,80})",

    ]

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.I
        )

        for match in matches:

            bank = " ".join(match.split())

            if len(bank) > 2:

                found.add(bank)

    return sorted(found)


# ==========================================================
# CREDIT CONTRACTS
# ==========================================================

def extract_credit_contracts(soup):

    contracts = []

    # ------------------------------------------------------
    # Таблица с действующими кредитами
    # ------------------------------------------------------

    table = soup.find("table")

    if table is None:
        return contracts

    rows = table.find_all("tr")

    # ------------------------------------------------------
    # Пропускаем заголовок
    # ------------------------------------------------------

    for row in rows[1:]:

        cols = row.find_all("td")

        if len(cols) < 7:
            continue

        values = [

            col.get_text(" ", strip=True)

            for col in cols

        ]

        # --------------------------------------------------
        # Пустая строка
        # --------------------------------------------------

        if not any(values):
            continue

        # --------------------------------------------------
        # Конец таблицы
        # --------------------------------------------------

        if any(

            value.strip().lower() == "итого"

            for value in values

        ):
            break

        try:

            bank_name = re.sub(
                r"\(\d+\)",
                "",
                values[1]
            ).strip()

            if not bank_name:
                continue

            contract_number = values[2].strip()

            currency = values[3].strip()

            if currency not in ("UZS", "USD", "EUR"):

                currency = "UZS"

            current_debt = normalize_number(values[4])

            overdue_debt = normalize_number(values[5])

            monthly_payment = normalize_number(values[6])

            contracts.append(

                {

                    "bank_name": bank_name,

                    "contract_number": contract_number,

                    "product_name": "",

                    "currency": currency,

                    "issued_amount": Decimal("0"),

                    "current_debt": current_debt,

                    "overdue_debt": overdue_debt,

                    "monthly_payment": monthly_payment,

                    "interest_rate": Decimal("0"),

                    "issued_date": None,

                    "closed_date": None,

                    "status": "ACTIVE",

                }

            )

        except Exception as e:

            print(
                "Contract parse error:",
                e
            )

    return contracts
# ==========================================================
# MAIN PARSER
# ==========================================================

def parse_credit_report(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    # ------------------------------------------------------
    # HTML INFO KREDIT
    # ------------------------------------------------------

    if extension in [".html", ".htm"]:

        soup = load_html(file_path)

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        score = extract_html_score(soup)

        if score == 0:
            score = extract_text_score(text)

        profile = {

            "full_name": extract_full_name(soup),

            "passport": extract_passport(soup),

            "phone": extract_phone(soup),

        }

        report = {

            "score": score,

            "risk": extract_risk(soup),

            "score_version": extract_score_version(soup),

            "income": extract_income(soup),

            "total_debt": extract_total_debt(soup),

            "overdue_debt": extract_overdue_debt(soup),

            "contracts": extract_contracts(soup),

            "banks": extract_banks(soup),

        }

        # --------------------------------------------------
        # Извлекаем реальные кредитные договоры
        # --------------------------------------------------

        contracts = extract_credit_contracts(soup)

        print("=" * 60)
        print("INFO KREDIT REPORT")
        print("=" * 60)

        print("Client:", profile["full_name"])
        print("Passport:", profile["passport"])
        print("Phone:", profile["phone"])

        print("-" * 60)

        print("Score:", report["score"])
        print("Risk:", report["risk"])
        print("Version:", report["score_version"])

        print("-" * 60)

        print("Debt:", report["total_debt"])
        print("Overdue:", report["overdue_debt"])

        print("Contracts:", report["contracts"])

        print("Banks:")

        for bank in report["banks"]:
            print(" •", bank)

        print("-" * 60)

        print("Credit contracts:")

        for contract in contracts:

            print(
                contract["bank_name"],
                contract["contract_number"],
                contract["current_debt"]
            )

        print("=" * 60)

        return {

            "profile": profile,

            "report": report,

            "contracts": contracts,

        }

    # ------------------------------------------------------
    # PDF
    # ------------------------------------------------------

    if extension == ".pdf":

        text = extract_pdf_text(file_path)

        income = search_decimal(

            [

                r"income[^0-9]{0,20}([\d\s.,]+)",

                r"доход[^0-9]{0,20}([\d\s.,]+)",

            ],

            text

        )

        debt = search_decimal(

            [

                r"debt[^0-9]{0,20}([\d\s.,]+)",

                r"задолженн[^0-9]{0,20}([\d\s.,]+)",

            ],

            text

        )

        score = extract_text_score(text)

        return {

            "profile": {

                "full_name": "",

                "passport": "",

                "phone": "",

            },

            "report": {

                "score": score,

                "risk": "",

                "score_version": "",

                "income": income,

                "total_debt": debt,

                "overdue_debt": Decimal("0"),

                "contracts": 0,

                "banks": [],

            },

            "contracts": []

        }

    raise ValueError(

        f"Unsupported file type: {extension}"

    )