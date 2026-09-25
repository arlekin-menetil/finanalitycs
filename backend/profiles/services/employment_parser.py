import re
from datetime import date, datetime

import pdfplumber


DATE_PATTERN = r"\d{2}\.\d{2}\.\d{4}"


# =========================================================
# PDF
# =========================================================

def extract_text(pdf_file):
    """
    Извлекает текст из PDF.
    """

    if hasattr(pdf_file, "seek"):
        pdf_file.seek(0)

    pages = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")

    return "\n".join(pages)


def extract_tables(pdf_file):
    """
    Извлекает таблицы из PDF.
    """

    if hasattr(pdf_file, "seek"):
        pdf_file.seek(0)

    tables = []

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            page_tables = page.extract_tables()

            if page_tables:
                tables.extend(page_tables)

    return tables


# =========================================================
# DATE
# =========================================================

def parse_date(value):

    if not value:
        return None

    try:
        return datetime.strptime(
            value,
            "%d.%m.%Y"
        ).date()

    except Exception:
        return None


# =========================================================
# EXPERIENCE
# =========================================================

def calculate_work_experience(start_date, end_date=None):
    """
    Возвращает

    total_months
    years
    months
    """

    if not start_date:
        return 0, 0, 0

    if end_date is None:
        end_date = date.today()

    total_months = (
        (end_date.year - start_date.year) * 12
        + (end_date.month - start_date.month)
    )

    if end_date.day < start_date.day:
        total_months -= 1

    if total_months < 0:
        total_months = 0

    years = total_months // 12
    months = total_months % 12

    return total_months, years, months


# =========================================================
# PARSER
# =========================================================

def parse_employment_document(pdf_file):

    text = extract_text(pdf_file)
    tables = extract_tables(pdf_file)

    result = {

        "full_name": "",

        "employment_pinfl": "",

        "document_number": "",

        "document_created_at": None,

        "company_name": "",

        "company_inn": "",

        "position": "",

        "department": "",

        "employment_start": None,

        "employment_end": None,

        "is_current_employee": False,

        "work_experience_months": 0,

        "work_experience_years": 0,

        "work_experience_remaining_months": 0,

        "employment_verified": False,
    }

    # =====================================================
    # ФИО
    # =====================================================

    match = re.search(
        r"Документ\s+выдан:\s*(.*?)\s*ПИНФЛ",
        text,
        re.S,
    )

    if match:
        result["full_name"] = " ".join(
            match.group(1).split()
        )

    # =====================================================
    # PINFL
    # =====================================================

    match = re.search(
        r"ПИНФЛ:\s*(\d+)",
        text,
    )

    if match:
        result["employment_pinfl"] = match.group(1)

    # =====================================================
    # Номер документа
    # =====================================================

    match = re.search(
        r"№\s*([A-Za-z0-9\-]+)",
        text,
    )

    if match:
        result["document_number"] = match.group(1)

    # =====================================================
    # Дата документа
    # =====================================================

    match = re.search(
        rf"Дата создания документа:\s*({DATE_PATTERN})",
        text,
    )

    if match:
        result["document_created_at"] = parse_date(
            match.group(1)
        )

    # =====================================================
    # Таблица
    # =====================================================

    for table in tables:

        for row in table:

            if not row:
                continue

            row = [
                str(cell).strip() if cell else ""
                for cell in row
            ]

            row_text = " ".join(row)

            if not re.search(DATE_PATTERN, row_text):
                continue

            dates = re.findall(
                DATE_PATTERN,
                row_text,
            )

            if dates:
                result["employment_start"] = parse_date(
                    dates[0]
                )

            if "До сих пор" in row_text:

                result["is_current_employee"] = True

            elif len(dates) > 1:

                result["employment_end"] = parse_date(
                    dates[1]
                )

            inn = re.search(
                r"\b\d{9}\b",
                row_text,
            )

            if inn:
                result["company_inn"] = inn.group()

            if len(row) > 4:
                result["company_name"] = row[4]

            if len(row) > 5:
                result["position"] = row[5]

            if len(row) > 6:
                result["department"] = row[6]

            break

        if result["employment_start"]:
            break

    # =====================================================
    # Fallback
    # =====================================================

    if not result["company_name"]:

        company = re.search(
            r'"([^"]+)"',
            text,
        )

        if company:
            result["company_name"] = company.group(1)

    # =====================================================
    # EXPERIENCE
    # =====================================================

    if result["employment_start"]:

        total, years, months = calculate_work_experience(
            result["employment_start"],
            result["employment_end"],
        )

        result["work_experience_months"] = total
        result["work_experience_years"] = years
        result["work_experience_remaining_months"] = months

    # =====================================================
    # VERIFIED
    # =====================================================

    result["employment_verified"] = bool(
        result["company_name"]
        and result["employment_start"]
    )

    return result