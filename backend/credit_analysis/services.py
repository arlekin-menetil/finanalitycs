import pdfplumber
from decimal import Decimal


def parse_credit_report(file_path):
    extracted_income = Decimal("0")
    extracted_debt = Decimal("0")
    credit_score = 0

    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""

    # Простейшая логика (потом заменим на ML)
    if "Income" in text:
        extracted_income = Decimal("5000000")

    if "Debt" in text:
        extracted_debt = Decimal("2000000")

    if "Score" in text:
        credit_score = 650

    return extracted_income, extracted_debt, credit_score