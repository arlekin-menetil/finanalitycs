from django.db import (
    IntegrityError,
    transaction,
)

from django.db.models import (
    Min,
    Max,
)

from typing import Optional, cast

import re
import json
import hashlib
import traceback

from banks.models import (
    Bank,
    BankProduct,
    AggregatedProduct,
    BankBranch,
    normalize_name,
)

from banks.normalizer import (
    normalize_item,
    normalize_bank_name,
    normalize_product_name,
)

from banks.utils import clean_string

# ==========================================
# 💣 NEW PARSERS
# ==========================================
from banks.parsers.bankuz.credits import (
    parse_credits,
)

from banks.parsers.bankuz.deposits import (
    parse_deposits,
)

from banks.parsers.bankuz.cards import (
    parse_cards,
)

from banks.parsers.bankuz.business import (
    parse_business,
)

from banks.parsers.bankuz.mortgage import (
    parse_mortgage,
)

# ==========================================
# 💣 SHARED HELPERS
# ==========================================
from banks.parsers.bankuz.shared.parsing import (
    parse_amount,
    parse_term,
)

from banks.parsers.bankuz.shared.normalization import (
    normalize_text,
)

from banks.parsers.bankuz.shared.logger import (
    log,
)


# ==========================================
# LOGGER
# ==========================================
def plog(msg):

    print(f"[PIPELINE] {msg}")


# ==========================================
# 💣 SAFE JSON
# ==========================================
def make_json_safe(value):

    try:

        return json.loads(
            json.dumps(
                value,
                default=str,
            )
        )

    except Exception:

        return {}


# ==========================================
# 💣 SAVE BRANCHES
# ==========================================
def save_branches(branches, bank):

    if not bank:

        return

    created = 0

    for b in branches:

        address = b.get("address")

        lat = b.get("lat") or b.get("latitude")

        lng = b.get("lng") or b.get("longitude")

        if not address:

            continue

        address = clean_string(address)

        if not address:

            continue

        try:

            with transaction.atomic():

                obj, was_created = BankBranch.objects.get_or_create(
                    bank=bank,
                    address=address,
                    defaults={
                        "latitude": lat,
                        "longitude": lng,
                    },
                )

        except IntegrityError:

            was_created = False

        if was_created:

            created += 1

    plog(f"📍 branches saved: {created}")


# ==========================================
# 💣 NORMALIZERS
# ==========================================
def safe_str(
    value,
    max_len=255,
):

    if value is None:

        return ""

    return str(value).strip()[:max_len]


def normalize_key(text):

    if not text:

        return ""

    text = str(text).lower().strip()

    text = re.sub(
        r"[^\w\s]",
        "",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text[:200]


def normalize_url(url):

    if not url:

        return None

    url = str(url).strip()

    if not url.startswith("http"):

        return None

    return url[:500]


# ==========================================
# 💣 AGGREGATION DETECTOR
# ==========================================
def get_aggregated_name(name):

    if not name:

        return "Финансовые продукты"

    n = normalize_text(name)

    if any(
        x in n
        for x in [
            "visa",
            "mastercard",
            "humo",
            "uzcard",
            "карта",
            "card",
        ]
    ):

        return "Банковские карты"

    if any(
        x in n
        for x in [
            "депозит",
            "deposit",
            "вклад",
        ]
    ):

        return "Депозиты"

    if any(
        x in n
        for x in [
            "factoring",
            "фактор",
        ]
    ):

        return "Факторинг"

    if any(
        x in n
        for x in [
            "рко",
            "расчетный счет",
        ]
    ):

        return "РКО"

    if any(
        x in n
        for x in [
            "business",
            "бизнес",
        ]
    ):

        return "Бизнес кредиты"

    if any(
        x in n
        for x in [
            "ипотек",
            "ipoteka",
            "жиль",
            "дом",
        ]
    ):

        return "Ипотека"

    if any(
        x in n
        for x in [
            "авто",
            "car",
            "kia",
            "byd",
            "hyundai",
        ]
    ):

        return "Автокредит"

    if any(
        x in n
        for x in [
            "микро",
            "micro",
            "займ",
        ]
    ):

        return "Микрозайм"

    return "Потребительский кредит"


# ==========================================
# 💣 GET OR CREATE BANK
# ==========================================
def get_or_create_bank(
    raw_bank,
) -> Optional[Bank]:

    if not raw_bank:

        return None

    clean_name = normalize_bank_name(raw_bank)

    if not clean_name:

        clean_name = str(raw_bank).strip()

    if not clean_name:

        return None

    bank_key = normalize_name(clean_name)

    if not bank_key:

        bank_key = hashlib.md5(clean_name.encode()).hexdigest()[:20]

    try:

        with transaction.atomic():

            existing = Bank.objects.filter(normalized_name=bank_key).first()

            if existing:

                return existing

            bank = Bank.objects.create(
                name=safe_str(
                    clean_name,
                    255,
                ),
                short_name=safe_str(
                    clean_name,
                    100,
                ),
                normalized_name=bank_key,
            )

            return bank

    except IntegrityError as e:

        plog(f"❌ IntegrityError BANK: " f"{clean_name} | {e}")

        return Bank.objects.filter(normalized_name=bank_key).first()

    except Exception as e:

        plog(f"❌ get_or_create_bank error: " f"{clean_name} | " f"{e}")

        traceback.print_exc()

        return None
    # ==========================================


# 💣 SAVE PRODUCTS
# ==========================================
def save_products(
    data,
    source="external",
):

    plog(f"\n💾 SAVING FROM: {source}")

    created = 0
    updated = 0
    skipped = 0

    source = (source or "external").strip()

    for raw in data:

        try:

            item = normalize_item(raw)

            if not isinstance(item, dict):

                item = {}

            raw_bank = raw.get("bank") or item.get("bank") or "Unknown Bank"

            # ==========================================
            # 💣 SAFE BANK
            # ==========================================
            bank_obj = get_or_create_bank(raw_bank)

            bank = None

            if bank_obj:

                bank = cast(
                    Bank,
                    bank_obj,
                )

            else:

                plog(f"⚠️ BANK NOT CREATED: " f"{raw_bank}")

            # ==========================================
            # 💣 NAME
            # ==========================================
            name = clean_string(item.get("name") or raw.get("name"))

            name = safe_str(
                name or "Финансовый продукт",
                255,
            )

            normalized_name = normalize_product_name(name) or normalize_key(name)

            if not normalized_name:

                normalized_name = (
                    f"product_" f"{hashlib.md5(name.encode()).hexdigest()[:8]}"
                )

            # ==========================================
            # 💣 URLS
            # ==========================================
            source_url = normalize_url(raw.get("source_url"))

            bank_url = normalize_url(raw.get("bank_url"))

            fallback_url = (
                f"{source}_"
                f"{raw_bank}_"
                f"{normalized_name}_"
                f"{hashlib.md5(str(raw).encode()).hexdigest()[:12]}"
            )

            key_url = source_url or bank_url or fallback_url

            # ==========================================
            # 💣 PRODUCT TYPE
            # ==========================================
            product_type = raw.get("product_type") or item.get("product_type")

            if not product_type:

                source_url_lower = str(source_url or "").lower()

                if "/card/" in source_url_lower:

                    product_type = "card"

                elif "/ipotek" in source_url_lower:

                    product_type = "mortgage"

                elif "/deposit" in source_url_lower:

                    product_type = "deposit"

                elif "/business" in source_url_lower:

                    product_type = "business"

                else:

                    product_type = "loan"

            # ==========================================
            # 💣 RATE
            # ==========================================
            rate = item.get("interest_rate") or item.get("rate")

            try:

                if rate is not None:

                    rate = float(rate)

                    if rate <= 0 or rate > 1000:

                        rate = None

            except Exception:

                rate = None

            # ==========================================
            # 💣 EXTRA DEPOSIT FIELDS
            # ==========================================
            payment_type = raw.get(
                "payment_type"
            )

            amount_min = raw.get(
                "amount_min"
            )

            amount_max = raw.get(
                "amount_max"
            )

            raw_data = raw.get("raw_data") or {}

            if not payment_type:

                payment_type = raw_data.get(
                    "payment_type"
                )

            if not amount_min:

                amount_min = raw_data.get(
                    "amount_min"
                )

            if not amount_max:

                amount_max = raw_data.get(
                    "amount_max"
                )

            currency = (
                raw.get("currency")
                or raw_data.get("currency")
            )

            updated_from_source = (
                raw.get("updated_from_source")
                or raw_data.get("updated_at")
            )

            try:

                if amount_min:

                    amount_min = int(amount_min)

            except Exception:

                amount_min = None

            try:

                if amount_max:

                    amount_max = int(amount_max)

            except Exception:

                amount_max = None

            plog(
                f"💰 currency={currency} | "
                f"amount_min={amount_min} | "
                f"amount_max={amount_max} | "
                f"payment={payment_type}"
            )

            # ==========================================
            # 💣 AMOUNT
            # ==========================================
            amount = (
                amount_max
                or item.get("max_amount")
                or raw.get("max_amount")
                or parse_amount(raw.get("amount"))
            )

            try:

                if amount:

                    amount = int(amount)

                    if amount < 1000 or amount > 50_000_000_000:

                        amount = None

            except Exception:

                amount = None

            # ==========================================
            # 💣 TERM
            # ==========================================
            term = item.get("term") or raw.get("term")

            term_min = None
            term_max = None

            if term:

                if isinstance(term, int):

                    term_min = term
                    term_max = term

                else:

                    parsed_term = parse_term(str(term))

                    if isinstance(parsed_term, tuple) and len(parsed_term) >= 2:

                        term_min = parsed_term[0]
                        term_max = parsed_term[1]

            # ==========================================
            # 💣 SCORE
            # ==========================================
            score = 0

            if rate is not None:

                score += max(
                    0,
                    100 - float(rate),
                )

            if amount:

                score += min(
                    amount / 1_000_000,
                    100,
                )

            score = round(score, 2)

            # ==========================================
            # 💣 UNIQUE KEY
            # ==========================================
            entity_key = (
                source_url
                or key_url
                or (f"{source}_" f"{raw_bank}_" f"{normalized_name}")
            )

            unique_key = hashlib.md5(
                (f"{source}_" f"{entity_key}").encode()
            ).hexdigest()

            # ==========================================
            # 💣 DESCRIPTION
            # ==========================================
            description = raw.get("description")

            if description:

                description = str(description).strip()

                if len(description) > 15000:

                    description = description[:15000]

            # ==========================================
            # 💣 DEBUG
            # ==========================================
            plog(
                f"🆕 {name} | "
                f"{raw_bank} | "
                f"type={product_type} | "
                f"rate={rate}"
            )

            plog(f"🔑 unique={unique_key[:12]} | " f"url={source_url}")

            # ==========================================
            # 💣 SAFE JSON
            # ==========================================
            safe_raw_data = make_json_safe(raw)

            safe_parser_metadata = make_json_safe(raw.get("entity_resolution") or {})

            # ==========================================
            # 💣 SAVE
            # ==========================================
            with transaction.atomic():

                obj, created_flag = BankProduct.objects.update_or_create(
                    unique_key=unique_key,
                    defaults={
                        # ==========================================
                        # 💣 BANK
                        # ==========================================
                        "bank": bank,
                        "bank_name": raw_bank,
                        # ==========================================
                        # 💣 BASE
                        # ==========================================
                        "name": name,
                        "normalized_name": normalized_name,
                        "product_type": product_type,
                        # ==========================================
                        # 💣 FINANCE
                        # ==========================================
                        "interest_rate": rate,
                        "max_amount": amount,
                        "term": term,
                        "term_min": term_min,
                        "term_max": term_max,
                        "score": score,
                        # ==========================================
                        # 💣 URLS
                        # ==========================================
                        "source_url": source_url,
                        "bank_url": bank_url,
                        # ==========================================
                        # 💣 FLAGS
                        # ==========================================
                        "is_active": True,
                        "is_online": bool(
                            raw.get(
                                "is_online",
                                raw.get(
                                    "online",
                                    False,
                                ),
                            )
                        ),
                        "real_online": raw.get("real_online"),
                        "has_branch": bool(
                            raw.get(
                                "has_branch",
                                True,
                            )
                        ),
                        "open_methods": (raw.get("open_methods") or []),
                        # ==========================================
                        # 💳 CARD DATA
                        # ==========================================
                        "currency": currency,
                        "card_system": raw.get("card_system"),
                        "card_type": raw.get("card_type"),
                        "issue_cost": raw.get("issue_cost"),
                        "service_cost": raw.get("service_cost"),
                        "validity_period": raw.get("validity_period"),
                        "documents_required": raw.get("documents_required"),
                        "image_url": raw.get("image_url"),
                        "requirements": raw.get("requirements"),
                        # ==========================================
                        # 💣 LOAN DATA
                        # ==========================================
                        "fee": raw.get("fee"),
                        "loan_type": raw.get("loan_type"),
                        # ==========================================
                        # 💣 TEXT
                        # ==========================================
                        "description": description,
                        # ==========================================
                        # 💣 META
                        # ==========================================
                        "updated_from_source": raw.get("updated_from_source"),
                        "raw_data": safe_raw_data,
                        "parser_metadata": (safe_parser_metadata),
                        "source_hash": hashlib.md5(str(raw).encode()).hexdigest(),
                        "source_name": source,
                        "parse_success": True,
                    },
                )

            # ==========================================
            # 💣 BRANCHES
            # ==========================================
            try:

                branches = raw.get("branches") or []

                if branches and bank:

                    save_branches(
                        branches,
                        bank,
                    )

            except Exception as e:

                plog(f"❌ branch save error: " f"{e}")

            # ==========================================
            # 💣 COUNTERS
            # ==========================================
            if created_flag:

                created += 1

            else:

                updated += 1

        except Exception as e:

            plog("=" * 80)

            plog(f"❌ SAVE ERROR: {e}")

            try:

                plog(f"❌ PRODUCT: {name}")

            except Exception:

                pass

            try:

                plog(f"❌ BANK: " f"{raw_bank}")

            except Exception:

                pass

            try:

                plog(f"❌ URL: {source_url}")

            except Exception:

                pass

            try:

                plog(f"❌ TYPE: {product_type}")

            except Exception:

                pass

            tb = traceback.format_exc()

            plog(tb)

            plog("=" * 80)

            skipped += 1

    plog(f"\n📊 {source.upper()} SUMMARY:")

    plog(f"🆕 Created: {created}")

    plog(f"♻️ Updated: {updated}")

    plog(f"⏭ Skipped: {skipped}")

    return created + updated + skipped
