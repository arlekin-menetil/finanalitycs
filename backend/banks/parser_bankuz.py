from banks.parsers.bankuz.credits import (
    parse_credits,
)

from banks.parsers.bankuz.mortgage import (
    parse_mortgage,
)

from banks.parsers.bankuz.cards import (
    parse_cards,
)

from banks.parsers.bankuz.deposits import (
    parse_deposits,
)

from banks.parsers.bankuz.business import (
    parse_business,
)

from banks.parsers.bankuz.shared.logger import (
    log,
)

# ==========================================
# 🔥 ENGINE REGISTRY
# ==========================================
PARSERS = {
    "credits": parse_credits,
    "mortgage": parse_mortgage,
    "cards": parse_cards,
    "deposits": parse_deposits,
    "business": parse_business,
}


# ==========================================
# 🔥 SAFE ENGINE EXECUTOR
# ==========================================
def run_engine(name, parser_func):

    try:

        log(f"🚀 START ENGINE: {name}")

        result = parser_func()

        count = len(result or [])

        log(f"✅ ENGINE SUCCESS: " f"{name} ({count})")

        return result or []

    except Exception as e:

        log(f"❌ ENGINE FAILED: " f"{name} | {e}")

        return []


# ==========================================
# 🔥 MAIN ENTRYPOINT
# ==========================================
def parse_bankuz():

    log("🔥 BANK.UZ START")

    final_results = {}

    total = 0

    for name, parser_func in PARSERS.items():

        result = run_engine(
            name,
            parser_func,
        )

        final_results[name] = result

        total += len(result)

    log(f"🎉 BANK.UZ DONE | " f"TOTAL: {total}")

    return final_results
