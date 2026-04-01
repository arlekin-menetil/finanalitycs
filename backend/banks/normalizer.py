import re


def normalize_bank_name(name: str) -> str:
    if not name:
        return "Unknown"

    name = name.lower()

    mapping = {
        "асак": "Asakabank",
        "asaka": "Asakabank",
        "ипотека": "Ipoteka-bank",
        "agro": "Agrobank",
        "tbc": "TBC Bank",
    }

    for key, value in mapping.items():
        if key in name:
            return value

    return name.capitalize()


def clean_name(text: str) -> str:
    if not text:
        return ""

    text = re.sub(r"\d+[.,]?\d*\s*%", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_item(item: dict) -> dict:
    return {
        "bank": normalize_bank_name(item.get("bank")),
        "name": clean_name(item.get("name")),
        "rate": item.get("rate"),
    }