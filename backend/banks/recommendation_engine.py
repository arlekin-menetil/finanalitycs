from decimal import Decimal

from collections import defaultdict


from django.db.models import Q

from django.utils import timezone


from banks.models import (
    Bank,
    BankProduct,
    RecommendationRule,
    RecommendationCampaign,
)


from profiles.models import FinancialProfile

from scoring.models import CreditScore

# ==========================================================

# ENGINE VERSION

# ==========================================================


ENGINE_VERSION = "6.0"


# ==========================================================

# RECOMMENDATION PRODUCT TYPES

# ==========================================================


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


# ==========================================================

# WEIGHTS

# ==========================================================


APPROVAL_WEIGHT = Decimal("0.25")

CREDIT_WEIGHT = Decimal("0.15")

DTI_WEIGHT = Decimal("0.15")

INCOME_WEIGHT = Decimal("0.10")

INTEREST_WEIGHT = Decimal("0.25")

PRIORITY_WEIGHT = Decimal("0.15")

STABILITY_WEIGHT = Decimal("0.05")


FEATURED_BONUS = Decimal("0.15")

ONLINE_BONUS = Decimal("0.02")

CAMPAIGN_BONUS = Decimal("0.10")


# ==========================================================

# SAFE DECIMAL

# ==========================================================


def to_decimal(value, default="0"):

    try:

        if value is None:

            return Decimal(default)

        return Decimal(str(value))

    except Exception:

        return Decimal(default)


# ==========================================================

# CLAMP

# ==========================================================


def clamp(
    value,
    minimum=Decimal("0"),
    maximum=Decimal("1"),
):

    if value < minimum:

        return minimum

    if value > maximum:

        return maximum

    return value


# ==========================================================

# NORMALIZE CREDIT SCORE

# ==========================================================


def normalize_credit_score(score):

    score = to_decimal(score)

    if score <= 0:

        return Decimal("0.30")

    return clamp(score / Decimal("1000"))


# ==========================================================

# NORMALIZE DTI

# ==========================================================


def normalize_dti(dti):

    if dti is None:

        return Decimal("0")

    dti = to_decimal(dti)

    if dti > 1:

        dti /= Decimal("100")

    return clamp(dti)


# ==========================================================

# SAFE INTEREST

# ==========================================================


def normalize_interest(rate, minimum, maximum):

    if rate is None:

        return Decimal("0.50")

    if maximum <= minimum:

        return Decimal("0.50")

    return clamp((maximum - to_decimal(rate)) / (maximum - minimum))


# ==========================================================

# USER RISK

# ==========================================================


def risk_factor(category):

    category = (category or "").lower()

    if category == "low":

        return Decimal("1.00")

    if category == "medium":

        return Decimal("0.70")

    return Decimal("0.40")


# ==========================================================

# USER CONTEXT

# ==========================================================


def build_user_context(user):

    score = CreditScore.objects.filter(user=user).order_by("-created_at").first()

    profile = FinancialProfile.objects.filter(user=user).first()

    if not score or not profile:

        return None

    return {
        "score": score,
        "profile": profile,
        "credit_score": normalize_credit_score(score.score),
        "approval_probability": (
            to_decimal(score.approval_probability) / Decimal("100")
        ),
        "income": to_decimal(profile.monthly_income_total),
        "dti": normalize_dti(profile.dti_ratio),
        "risk_factor": risk_factor(score.risk_category),
    }


# ==========================================================

# LOAD RECOMMENDATION RULES

# ==========================================================


def load_rules():

    rules = {}

    queryset = RecommendationRule.objects.filter(enabled=True).select_related("bank")

    for rule in queryset:

        rules[rule.bank_id] = rule

    return rules


# ==========================================================

# LOAD CAMPAIGNS

# ==========================================================


def load_campaigns():

    now = timezone.now()

    campaigns = defaultdict(list)

    queryset = RecommendationCampaign.objects.filter(
        is_active=True,
    ).select_related("bank")

    for campaign in queryset:

        # ==========================================

        # NOT STARTED

        # ==========================================

        if campaign.starts_at:

            if campaign.starts_at > now:

                continue

        # ==========================================

        # EXPIRED

        # ==========================================

        if campaign.ends_at:

            if campaign.ends_at < now:

                continue

        campaigns[campaign.bank_id].append(campaign)

    return campaigns


# ==========================================================

# BANK PRIORITY

# ==========================================================


def get_priority_weight(
    bank,
    rules,
):

    if bank is None:

        return 1

    rule = rules.get(bank.id)

    if rule:

        return rule.priority or 1

    return (
        getattr(
            bank,
            "priority_weight",
            1,
        )
        or 1
    )


# ==========================================================

# FEATURED

# ==========================================================


def is_featured(
    bank,
    rules,
):

    if bank is None:

        return False

    rule = rules.get(bank.id)

    if rule:

        return bool(rule.featured)

    return bool(
        getattr(
            bank,
            "is_featured",
            False,
        )
    )


# ==========================================================

# CAMPAIGN BONUS

# ==========================================================


def campaign_bonus(
    bank,
    campaigns,
):

    if bank is None:

        return Decimal("0")

    active = campaigns.get(
        bank.id,
        [],
    )

    if not active:

        return Decimal("0")

    return CAMPAIGN_BONUS


# ==========================================================

# CALCULATE PRODUCT SCORE

# ==========================================================


def calculate_product_score(
    product,
    context,
    rules,
    campaigns,
    min_rate,
    max_rate,
    max_priority,
):

    bank = getattr(
        product,
        "bank",
        None,
    )

    # ======================================================

    # COMPONENTS

    # ======================================================

    approval_component = clamp(context["approval_probability"])

    credit_component = clamp(context["credit_score"])

    dti_component = Decimal("1") - clamp(context["dti"])

    income_component = clamp(context["income"] / Decimal("10000000"))

    interest_component = normalize_interest(
        product.interest_rate,
        min_rate,
        max_rate,
    )

    priority_weight = get_priority_weight(
        bank,
        rules,
    )

    priority_component = clamp(
        Decimal(str(priority_weight)) / Decimal(str(max_priority))
    )

    stability_component = context["risk_factor"]

    featured_bonus = (
        FEATURED_BONUS
        if is_featured(
            bank,
            rules,
        )
        else Decimal("0")
    )

    online_bonus = (
        ONLINE_BONUS
        if getattr(
            product,
            "is_online",
            False,
        )
        else Decimal("0")
    )

    campaign = campaign_bonus(
        bank,
        campaigns,
    )

    # ======================================================

    # FINAL SCORE

    # ======================================================

    final_score = (
        approval_component * APPROVAL_WEIGHT
        + credit_component * CREDIT_WEIGHT
        + dti_component * DTI_WEIGHT
        + income_component * INCOME_WEIGHT
        + interest_component * INTEREST_WEIGHT
        + priority_component * PRIORITY_WEIGHT
        + stability_component * STABILITY_WEIGHT
        + featured_bonus
        + online_bonus
        + campaign
    )

    final_score = clamp(final_score)

    ranking_percent = final_score * Decimal("100")

    # ======================================================

    # APPROVAL

    # ======================================================

    approval = clamp(
        context["approval_probability"] * Decimal("0.60")
        + interest_component * Decimal("0.20")
        + priority_component * Decimal("0.10")
        + credit_component * Decimal("0.10")
    )

    # ======================================================

    # LOAN LIMIT

    # ======================================================

    limit = context["income"] * Decimal("6") * approval

    max_amount = to_decimal(
        getattr(
            product,
            "max_amount",
            None,
        )
    )

    if max_amount > 0:

        limit = min(limit, max_amount)

    # ======================================================

    # SAVE

    # ======================================================

    product.ranking_score = float(
        round(
            ranking_percent,
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
            limit,
            2,
        )
    )

    product.priority = priority_weight

    product.featured = is_featured(
        bank,
        rules,
    )

    return product


# ==========================================================

# APPLY CAMPAIGN

# ==========================================================


def apply_campaign(
    product,
    bank,
    campaigns,
):

    if bank is None:

        return product

    active = campaigns.get(bank.id, [])

    if not active:

        return product

    badge = None

    bonus = Decimal("0")

    for campaign in active:

        bonus += to_decimal(campaign.bonus_score) / Decimal("100")

        if badge is None:

            badge = campaign.badge

    current = to_decimal(getattr(product, "ranking_score", 0))

    product.ranking_score = float(round(current + bonus, 2))

    product.has_campaign = True

    product.campaign_badge = badge

    return product


# ==========================================================

# BUILD RECOMMENDATIONS

# ==========================================================


def build_recommendations(
    user,
):

    context = build_user_context(
        user,
    )

    if context is None:

        return []

    # ======================================================

    # LOAD RULES

    # ======================================================

    rules = load_rules()

    campaigns = load_campaigns()

    # ======================================================

    # PRODUCTS

    # ======================================================

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

    queryset = BankProduct.objects.select_related("bank").filter(
        is_active=True,
        bank__is_active=True,
        product_type__in=RECOMMENDATION_PRODUCT_TYPES,
    )

    products = list(queryset)

    if not products:

        return []

    # ======================================================

    # INTEREST RANGE

    # ======================================================

    rates = [
        to_decimal(p.interest_rate) for p in products if p.interest_rate is not None
    ]

    if not rates:

        return []

    min_rate = min(rates)

    max_rate = max(rates)

    # ======================================================

    # MAX PRIORITY

    # ======================================================

    priorities = []

    for product in products:

        bank = getattr(
            product,
            "bank",
            None,
        )

        priorities.append(
            get_priority_weight(
                bank,
                rules,
            )
        )

    max_priority = max(priorities)

    # ======================================================

    # SCORE PRODUCTS

    # ======================================================

    ranked_products = []

    for product in products:

        ranked = calculate_product_score(
            product=product,
            context=context,
            rules=rules,
            campaigns=campaigns,
            min_rate=min_rate,
            max_rate=max_rate,
            max_priority=max_priority,
        )

        ranked_products.append(ranked)

    return ranked_products


# ==========================================================

# BEST PRODUCT PER BANK

# ==========================================================


def select_best_products_per_bank(
    products,
):

    best_products = {}

    for product in products:

        bank = getattr(
            product,
            "bank",
            None,
        )

        if bank:

            bank_key = bank.id

        else:

            bank_key = (
                getattr(
                    product,
                    "bank_name",
                    None,
                )
                or "Unknown"
            )

        current = best_products.get(bank_key)

        if current is None:

            best_products[bank_key] = product

            continue

        if getattr(
            product,
            "ranking_score",
            0,
        ) > getattr(
            current,
            "ranking_score",
            0,
        ):

            best_products[bank_key] = product

    return list(best_products.values())


# ==========================================================

# SORT PRODUCTS

# ==========================================================


def sort_products(
    products,
):
    """
    Sort recommendations by the calculated AI ranking first.

    ranking_score is the final recommendation score produced by
    calculate_product_score(). Other fields are used as tie-breakers.
    """
    return sorted(
        products,
        key=lambda product: (
            # ======================================
            # AI RANKING — PRIMARY
            # ======================================
            float(
                getattr(
                    product,
                    "ranking_score",
                    0,
                )
                or 0
            ),
            # ======================================
            # APPROVAL — TIE BREAKER
            # ======================================
            float(
                getattr(
                    product,
                    "approval_probability",
                    0,
                )
                or 0
            ),
            # ======================================
            # FEATURED
            # ======================================
            int(
                getattr(
                    product,
                    "featured",
                    False,
                )
            ),
            # ======================================
            # PRIORITY
            # ======================================
            getattr(
                product,
                "priority",
                0,
            ),
            # ======================================
            # ONLINE
            # ======================================
            int(
                getattr(
                    product,
                    "is_online",
                    False,
                )
            ),
            # ======================================
            # LOWER INTEREST RATE IS BETTER
            # ======================================
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


def finalize_recommendations(
    products,
    limit=None,
):

    # Сортируем все продукты

    products = sort_products(products)

    # Если задан лимит — возвращаем первые N

    if limit is not None:

        return products[:limit]

    # Иначе возвращаем весь список

    return products


# ==========================================================

# PUBLIC API

# ==========================================================


def get_top_recommendations(
    user,
    limit=100,
):

    products = build_recommendations(
        user,
    )

    products = finalize_recommendations(
        products,
        limit=limit,
    )

    return products


# ==========================================================

# BEST PRODUCTS

# ==========================================================


def get_best_products(
    user=None,
    limit=100,
):

    if user and getattr(user, "is_authenticated", False):

        return get_top_recommendations(
            user=user,
            limit=limit,
        )

    queryset = BankProduct.objects.select_related("bank").filter(
        is_active=True,
        bank__is_active=True,
        product_type__in=RECOMMENDATION_PRODUCT_TYPES,
    )

    products = list(queryset)

    if not products:

        return []

    rules = load_rules()

    campaigns = load_campaigns()

    ranked = []

    for product in products:

        bank = getattr(
            product,
            "bank",
            None,
        )

        product.priority = get_priority_weight(
            bank,
            rules,
        )

        product.featured = is_featured(
            bank,
            rules,
        )

        apply_campaign(
            product,
            bank,
            campaigns,
        )

        ranked.append(product)

    return finalize_recommendations(
        ranked,
        limit=limit,
    )


# ==========================================================

# SAFE PRODUCTS

# ==========================================================


def get_safe_products(
    user,
    limit=20,
):

    products = get_top_recommendations(
        user=user,
        limit=None,
    )

    safe = [
        product
        for product in products
        if getattr(
            product,
            "approval_probability",
            0,
        )
        >= 80
    ]

    return safe[:limit]


# ==========================================================

# PREMIUM PRODUCTS

# ==========================================================


def get_premium_products(
    user,
    limit=20,
):

    products = get_top_recommendations(
        user=user,
        limit=None,
    )

    premium = [
        product
        for product in products
        if getattr(
            product,
            "ranking_score",
            0,
        )
        >= 90
    ]

    return premium[:limit]


# ==========================================================

# BACKWARD COMPATIBILITY

# ==========================================================


def get_recommendations_for_user(
    user,
    limit=10,
):

    return get_top_recommendations(
        user=user,
        limit=limit,
    )


def get_safe_products_for_user(
    user,
    limit=10,
):

    return get_safe_products(
        user=user,
        limit=limit,
    )


def get_premium_products_for_user(
    user,
    limit=10,
):

    return get_premium_products(
        user=user,
        limit=limit,
    )
