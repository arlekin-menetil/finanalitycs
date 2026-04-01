from decimal import Decimal
from banks.models import BankProduct, RecommendationSnapshot
from scoring.models import CreditScore
from profiles.models import FinancialProfile


RANKING_VERSION = "4.0"


def clamp(value, min_value=Decimal("0"), max_value=Decimal("1")):
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value


def normalize_dti(dti):

    if dti is None:
        return Decimal("0")

    dti = Decimal(dti)

    if dti > 1:
        return dti / Decimal("100")

    return dti


def get_top_recommendations(user, limit=5):

    score_obj = (
        CreditScore.objects
        .filter(user=user)
        .order_by("-created_at")
        .first()
    )

    if not score_obj:
        return []

    profile = FinancialProfile.objects.filter(user=user).first()

    if not profile:
        return []

    user_score = score_obj.score or 0

    approval_probability = Decimal(
        str(score_obj.approval_probability or 0)
    ) / Decimal("100")

    user_dti = normalize_dti(profile.dti_ratio)

    user_income = profile.monthly_income_total or Decimal("0")

    risk_category = (score_obj.risk_category or "medium").lower()

    # =========================
    # 💣 ОСНОВНОЙ QUERY
    # =========================

    products = (
        BankProduct.objects
        .filter(
            is_active=True,
            bank__is_active=True,
            min_score__lte=user_score,
            max_dti__gte=user_dti,
            min_income__lte=user_income
        )
        .select_related("bank")
    )

    # =========================
    # 💣 FALLBACK ЕСЛИ ПУСТО
    # =========================

    if not products.exists():
        products = (
            BankProduct.objects
            .filter(is_active=True)
            .select_related("bank")
        )

    products = list(products)

    if not products:
        return []

    # =========================
    # MARKET NORMALIZATION
    # =========================

    interest_rates = [p.interest_rate or Decimal("0") for p in products]

    min_rate = min(interest_rates)
    max_rate = max(interest_rates)

    priority_values = [p.bank.priority_weight or 1 for p in products]

    max_priority = max(priority_values) if priority_values else 1

    ranked_products = []

    for product in products:

        score_gap = Decimal(user_score) - Decimal(product.min_score or 0)

        approval_component = clamp(
            approval_probability + (score_gap / Decimal("1000"))
        )

        if product.max_dti:
            dti_ratio = clamp(user_dti / product.max_dti)
            dti_component = Decimal("1") - dti_ratio
        else:
            dti_component = Decimal("0.5")

        if product.min_income:
            income_ratio = user_income / product.min_income
            income_component = clamp(income_ratio / Decimal("2"))
        else:
            income_component = Decimal("0.5")

        if max_rate > min_rate:
            interest_component = clamp(
                (max_rate - product.interest_rate) /
                (max_rate - min_rate)
            )
        else:
            interest_component = Decimal("0.5")

        priority_component = clamp(
            Decimal(product.bank.priority_weight or 1) / Decimal(max_priority)
        )

        if risk_category == "low":
            stability_component = Decimal("1")
        elif risk_category == "medium":
            stability_component = Decimal("0.6")
        else:
            stability_component = Decimal("0.3")

        featured_bonus = Decimal("0.02") if product.bank.is_featured else Decimal("0")

        # 💣 УСИЛЕННЫЙ RANKING
        ranking_score = (
            approval_component * Decimal("0.30") +
            dti_component * Decimal("0.20") +
            income_component * Decimal("0.10") +
            interest_component * Decimal("0.20") +
            priority_component * Decimal("0.05") +
            stability_component * Decimal("0.10") +
            featured_bonus
        )

        ranking_score = clamp(ranking_score)

        ranking_percent = ranking_score * Decimal("100")

        # =========================
        # INTEREST FACTOR
        # =========================

        if max_rate > min_rate:
            interest_factor = clamp(
                Decimal("1") - ((product.interest_rate - min_rate) / Decimal("10"))
            )
        else:
            interest_factor = Decimal("1")

        # =========================
        # BANK FACTOR
        # =========================

        bank_factor = Decimal(str(product.bank.priority_weight or 1))

        # =========================
        # 💣 НОВЫЙ APPROVAL (СТАБИЛЬНЫЙ)
        # =========================

        adjusted_approval = clamp(
            (approval_probability * Decimal("0.7")) +
            (interest_factor * Decimal("0.2")) +
            (bank_factor * Decimal("0.1"))
        )

        # =========================
        # LOAN LIMIT
        # =========================

        base_multiplier = Decimal("8")

        risk_adjustment = adjusted_approval + Decimal("0.5")

        loan_limit = (
            user_income *
            base_multiplier *
            risk_adjustment *
            interest_factor *
            bank_factor
        )

        if product.max_amount:
            loan_limit = min(loan_limit, product.max_amount)

        # =========================
        # FINAL OUTPUT
        # =========================

        product.ranking_score = float(round(ranking_percent, 2))

        product.approval_probability = float(
            round(adjusted_approval * Decimal("100"), 2)
        )

        product.loan_limit_hint = float(loan_limit)

        product.ranking_explain = {
            "version": RANKING_VERSION,
            "approval_component": float(round(approval_component, 4)),
            "dti_component": float(round(dti_component, 4)),
            "income_component": float(round(income_component, 4)),
            "interest_component": float(round(interest_component, 4)),
            "priority_component": float(round(priority_component, 4)),
            "stability_component": float(round(stability_component, 4)),
            "featured_bonus": float(featured_bonus)
        }

        ranked_products.append(product)

    ranked_products.sort(
        key=lambda x: x.ranking_score,
        reverse=True
    )

    RecommendationSnapshot.objects.create(
        user=user,
        ranking_version=RANKING_VERSION,
        user_score=user_score,
        approval_probability=approval_probability,
        dti_ratio=user_dti,
        monthly_income=user_income,
        risk_category=risk_category,
        min_market_rate=min_rate,
        max_market_rate=max_rate,
        feature_vector={
            "approval": float(approval_probability),
            "dti": float(user_dti),
            "income": float(user_income),
            "risk_category": risk_category,
            "market_min_rate": float(min_rate),
            "market_max_rate": float(max_rate),
        }
    )

    if limit:
        return ranked_products[:limit]

    return ranked_products