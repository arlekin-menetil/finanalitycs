import hashlib

from .normalization import normalize_text


def build_product_key(item: dict) -> str:

    raw = "|".join(
        [
            str(item.get("bank") or ""),
            str(item.get("name") or ""),
            str(item.get("source_url") or ""),
        ]
    )

    raw = normalize_text(raw)

    return hashlib.md5(raw.encode("utf-8")).hexdigest()
