from typing import List
from decimal import Decimal
from banks.models import BankProduct


# ==========================================
# 🧠 USER DATA BUILDER (ИЗ МОДЕЛЕЙ)
# ==========================================

def build_user_data(user) -> dict:
    profile = getattr(user, "financial_profile", None)
    employment = getattr(user, "employment", None)

    if not profile:
        return {}

    income = float(profile.monthly_income_total or 0)
    obligations = float(profile.monthly_obligations_total or 0)

    dti = float(profile.dti_ratio or 0) / 100  # из % → в долю

    # 💣 простая вероятность одобрения
    approval_probability = 0.5

    if dti < 0.3:
        approval_probability += 0.3
    elif dti < 0.5:
        approval_probability += 0.1
    else:
        approval_probability -= 0.2

    # 💣 стабильность работы
    if employment:
        if employment.work_experience_months > 24:
            approval_probability += 0.1
        elif employment.work_experience_months < 6:
            approval_probability -= 0.2

    approval_probability = max(0, min(1, approval_probability))

    return {
        "income": income,
        "dti": dti,
        "approval_probability": approval_probability,
        "score": 600 + int(approval_probability * 200)  # псевдо credit score
    }


# ==========================================
# 💣 CORE SCORING FUNCTION
# ==========================================

def calculate_product_score(product, user_data: dict) -> float:
    probability = user_data.get("approval_probability", 0.5)
    dti = user_data.get("dti", 0.5)
    income = user_data.get("income", 0)

    interest = float(product.interest_rate or 30)

    # 💣 чем меньше ставка — тем лучше
    interest_score = max(0, (50 - interest) / 50)

    bank_weight = float(product.bank.priority_weight or 1.0)

    # =========================
    # 🔥 ФИЛЬТРЫ (как в банке)
    # =========================

    if product.min_score and user_data.get("score", 0) < product.min_score:
        return 0

    if product.max_dti and dti > float(product.max_dti):
        return 0

    if product.min_income and income < float(product.min_income):
        return 0

    # =========================
    # 💣 БОНУСЫ
    # =========================

    term_bonus = 0.05
    if product.term:
        if "месяц" in product.term.lower():
            term_bonus = 0.1

    # 💣 стабильность дохода
    stability_bonus = 0.1 if probability > 0.7 else 0

    # =========================
    # 💣 ФИНАЛЬНЫЙ SCORE
    # =========================

    score = (
        probability * 0.35 +
        interest_score * 0.35 +
        bank_weight * 0.1 +
        term_bonus * 0.1 +
        stability_bonus * 0.1
    )

    return round(score, 4)


# ==========================================
# 💬 EXPLANATION (ВАЖНО)
# ==========================================

def build_explanation(product, user_data: dict) -> dict:
    reasons = []

    if product.interest_rate and product.interest_rate < 25:
        reasons.append("низкая ставка")

    if user_data.get("dti", 1) < 0.4:
        reasons.append("хорошая долговая нагрузка")

    if user_data.get("approval_probability", 0) > 0.7:
        reasons.append("высокий шанс одобрения")

    if product.bank.priority_weight and product.bank.priority_weight > 1:
        reasons.append("надежный банк")

    if not reasons:
        reasons.append("сбалансированные условия")

    return {
        "bank": product.bank.short_name,
        "interest_rate": product.interest_rate,
        "reasons": reasons,
        "score_hint": "учитывается доход, нагрузка, ставка и стабильность"
    }


# ==========================================
# 🚀 MAIN RECOMMENDATION FUNCTION
# ==========================================

def get_recommendations_for_user(user, limit=5) -> List[dict]:
    user_data = build_user_data(user)

    products = BankProduct.objects.filter(
        is_active=True
    ).select_related("bank")

    scored_products = []

    for product in products:
        score = calculate_product_score(product, user_data)

        if score <= 0:
            continue

        scored_products.append({
            "product": product,
            "score": score,
            "explanation": build_explanation(product, user_data)
        })

    scored_products.sort(key=lambda x: x["score"], reverse=True)

    return scored_products[:limit]


# ==========================================
# 🔥 FALLBACK (без пользователя)
# ==========================================

def get_best_products(limit=5):
    return BankProduct.objects.filter(
        is_active=True
    ).select_related("bank").order_by(
        "-bank__priority_weight",
        "interest_rate"
    )[:limit]


def get_products_by_type(keyword: str):
    return BankProduct.objects.filter(
        name__icontains=keyword,
        is_active=True
    ).select_related("bank").order_by(
        "-bank__priority_weight",
        "interest_rate"
    )