from decimal import Decimal

from banks.models import (
    BankProduct,
    RecommendationRule,
)

from scoring.models import CreditScore
from profiles.models import FinancialProfile

# ==================================================
# RANKING VERSION
# ==================================================

RANKING_VERSION = "6.0"


# ==================================================
# DEFAULT WEIGHTS
# ==================================================

APPROVAL_WEIGHT = Decimal("0.20")
CREDIT_WEIGHT = Decimal("0.15")
DTI_WEIGHT = Decimal("0.10")
INCOME_WEIGHT = Decimal("0.05")
INTEREST_WEIGHT = Decimal("0.20")
PRIORITY_WEIGHT = Decimal("0.30")
STABILITY_WEIGHT = Decimal("0.05")

FEATURED_BONUS = Decimal("0.15")
ONLINE_BONUS = Decimal("0.02")


# ==================================================
# SAFE DECIMAL
# ==================================================


def to_decimal(value, default="0"):

    try:

        if value in (None, ""):
            return Decimal(default)

        return Decimal(str(value))

    except Exception:

        return Decimal(default)


# ==================================================
# CLAMP
# ==================================================


def clamp(
    value,
    minimum=Decimal("0"),
    maximum=Decimal("1"),
):

    value = to_decimal(value)

    if value < minimum:
        return minimum

    if value > maximum:
        return maximum

    return value


# ==================================================
# NORMALIZE DTI
# ==================================================


def normalize_dti(dti):

    if dti is None:
        return Decimal("0")

    dti = to_decimal(dti)

    if dti > 1:
        dti /= Decimal("100")

    return clamp(dti)


# ==================================================
# NORMALIZE CREDIT SCORE
# ==================================================


def normalize_credit_score(score):

    score = to_decimal(score)

    if score <= 0:
        return Decimal("0.30")

    return clamp(score / Decimal("1000"))


# ==================================================
# LOAD RECOMMENDATION RULES
# ==================================================


def get_rules():

    return {
        rule.bank_id: rule
        for rule in RecommendationRule.objects.filter(enabled=True).select_related(
            "bank"
        )
    }


# ==================================================
# BANK PRIORITY
# ==================================================


def get_priority(bank, rules):

    if not bank:
        return 1

    rule = rules.get(bank.id)

    if rule:

        return max(
            int(rule.priority or 1),
            1,
        )

    return max(
        int(getattr(bank, "priority_weight", 1) or 1),
        1,
    )


# ==================================================
# FEATURED
# ==================================================


def is_featured(bank, rules):

    if not bank:
        return False

    rule = rules.get(bank.id)

    if rule is not None:
        return bool(rule.featured)

    return bool(
        getattr(
            bank,
            "is_featured",
            False,
        )
    )


# ==================================================
# INTEREST COMPONENT
# ==================================================


def calculate_interest_component(
    product,
    min_rate,
    max_rate,
):

    if product.interest_rate is None or max_rate <= min_rate:
        return Decimal("0.50")

    return clamp((max_rate - to_decimal(product.interest_rate)) / (max_rate - min_rate))


# ==================================================
# STABILITY COMPONENT
# ==================================================


def get_stability_component(
    risk_category,
):

    risk = (risk_category or "medium").lower()

    if risk == "low":
        return Decimal("1.00")

    if risk == "medium":
        return Decimal("0.70")

    return Decimal("0.40")


# ==================================================
# CALCULATE RANKING SCORE
# ==================================================


def calculate_ranking(
    approval_component,
    credit_component,
    dti_component,
    income_component,
    interest_component,
    priority_component,
    stability_component,
    featured=False,
    online=False,
):

    score = (
        approval_component * APPROVAL_WEIGHT
        + credit_component * CREDIT_WEIGHT
        + dti_component * DTI_WEIGHT
        + income_component * INCOME_WEIGHT
        + interest_component * INTEREST_WEIGHT
        + priority_component * PRIORITY_WEIGHT
        + stability_component * STABILITY_WEIGHT
    )

    if featured:

        score += FEATURED_BONUS

    if online:

        score += ONLINE_BONUS

    return clamp(score)


# ==================================================
# APPROVAL
# ==================================================


def calculate_approval(
    approval_probability,
    interest_component,
    priority_component,
    credit_component,
):

    return clamp(
        approval_probability * Decimal("0.55")
        + interest_component * Decimal("0.15")
        + priority_component * Decimal("0.20")
        + credit_component * Decimal("0.10")
    )


# ==================================================
# LOAN LIMIT
# ==================================================


def calculate_limit(
    income,
    approval,
    product,
):

    loan_limit = income * Decimal("6") * approval

    max_amount = to_decimal(
        getattr(
            product,
            "max_amount",
            None,
        )
    )

    if max_amount > 0:

        loan_limit = min(
            loan_limit,
            max_amount,
        )

    return loan_limit


# ==================================================
# SORT PRODUCTS
# ==================================================


def sort_products(
    products,
    rules,
):

    def priority(product):

        bank = getattr(
            product,
            "bank",
            None,
        )

        return get_priority(
            bank,
            rules,
        )

    def featured(product):

        bank = getattr(
            product,
            "bank",
            None,
        )

        return is_featured(
            bank,
            rules,
        )

    return sorted(
        products,
        key=lambda product: (
            # =====================================
            # AI RANKING SCORE
            # =====================================
            float(
                getattr(
                    product,
                    "ranking_score",
                    0,
                )
                or 0
            ),
            # =====================================
            # APPROVAL PROBABILITY
            # =====================================
            float(
                getattr(
                    product,
                    "approval_probability",
                    0,
                )
                or 0
            ),
            # =====================================
            # FEATURED BANK
            # =====================================
            int(
                featured(
                    product,
                )
            ),
            # =====================================
            # BANK PRIORITY
            # =====================================
            priority(
                product,
            ),
            # =====================================
            # LOWER INTEREST RATE IS BETTER
            # =====================================
            -float(
                getattr(
                    product,
                    "interest_rate",
                    999,
                )
                or 999
            ),
        ),
        reverse=True,
    )


# ==================================================
# RECOMMENDATIONS
# ==================================================


def get_top_recommendations(
    user,
    limit=100,
):

    score_obj = CreditScore.objects.filter(user=user).order_by("-created_at").first()

    if not score_obj:
        return []

    profile = FinancialProfile.objects.filter(user=user).first()

    if not profile:
        return []

    rules = get_rules()

    # ==================================================
    # PRODUCT TYPES
    # ==================================================

    RECOMMENDATION_PRODUCT_TYPES = [
        "loan",
        "business_credit",
        "micro",
        "mortgage",
        "auto",
        "education",
        "green",
        "card",
        "overdraft",
        "installment",
    ]

    # ==================================================
    # LOAD PRODUCTS
    # ==================================================

    products = list(
        BankProduct.objects.filter(
            is_active=True,
            bank__is_active=True,
            product_type__in=RECOMMENDATION_PRODUCT_TYPES,
        ).select_related("bank")
    )

    if not products:
        return []

    interest_rates = [
        to_decimal(p.interest_rate) for p in products if p.interest_rate is not None
    ]

    if not interest_rates:
        return []

    min_rate = min(interest_rates)
    max_rate = max(interest_rates)

    max_priority = max(
        get_priority(
            p.bank,
            rules,
        )
        for p in products
        if p.bank
    )

    # ==================================================
    # USER DATA
    # ==================================================

    score_component = normalize_credit_score(score_obj.score or 0)

    approval_probability = to_decimal(score_obj.approval_probability) / Decimal("100")

    user_dti = normalize_dti(profile.dti_ratio)

    user_income = to_decimal(profile.monthly_income_total)

    risk_category = (score_obj.risk_category or "medium").lower()

    ranked_products = []

    # ==================================================
    # CALCULATE SCORE
    # ==================================================

    for product in products:

        bank = getattr(
            product,
            "bank",
            None,
        )

        approval_component = clamp(approval_probability)

        credit_component = clamp(score_component)

        dti_component = Decimal("1") - clamp(user_dti)

        income_component = clamp(user_income / Decimal("10000000"))

        if product.interest_rate is not None and max_rate > min_rate:

            interest_component = clamp(
                (max_rate - to_decimal(product.interest_rate)) / (max_rate - min_rate)
            )

        else:

            interest_component = Decimal("0.5")

        priority_component = clamp(
            Decimal(
                str(
                    get_priority(
                        bank,
                        rules,
                    )
                )
            )
            / Decimal(str(max_priority))
        )

        if risk_category == "low":

            stability_component = Decimal("1")

        elif risk_category == "medium":

            stability_component = Decimal("0.7")

        else:

            stability_component = Decimal("0.4")

        featured = is_featured(
            bank,
            rules,
        )

        ranking_score = calculate_ranking(
            approval_component,
            credit_component,
            dti_component,
            income_component,
            interest_component,
            priority_component,
            stability_component,
            featured=featured,
            online=getattr(
                product,
                "is_online",
                False,
            ),
        )

        approval = calculate_approval(
            approval_probability,
            interest_component,
            priority_component,
            credit_component,
        )

        loan_limit = calculate_limit(
            user_income,
            approval,
            product,
        )

        product.ranking_score = float(
            round(
                ranking_score * Decimal("100"),
                2,
            )
        )

        product.approval_probability = float(
            round(
                approval * Decimal("100"),
                2,
            )
        )

        product.loan_limit_hint = float(
            round(
                loan_limit,
                2,
            )
        )

        ranked_products.append(product)

    # ==================================================
    # SORT
    # ==================================================

    ranked_products = sort_products(
        ranked_products,
        rules,
    )

    # ==================================================
    # BEST PRODUCT PER BANK
    # ==================================================

    best_by_bank = {}

    for product in ranked_products:

        bank_name = (
            getattr(
                product,
                "bank_name",
                None,
            )
            or (
                product.bank.name
                if getattr(
                    product,
                    "bank",
                    None,
                )
                else None
            )
            or "Unknown Bank"
        )

        if bank_name not in best_by_bank:

            best_by_bank[bank_name] = product

    best_products = list(best_by_bank.values())

    # ==================================================
    # FINAL SORT
    # ==================================================

    best_products = sort_products(
        best_products,
        rules,
    )

    if limit:

        return best_products[:limit]

    return best_products
