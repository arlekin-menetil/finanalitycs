import math
from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction

from profiles.models import FinancialProfile
from scoring.models import CreditScore


# =====================================================
# Конфигурация весов
# =====================================================

DTI_WEIGHTS = [
    (Decimal("20.00"), 400),
    (Decimal("35.00"), 300),
    (Decimal("50.00"), 200),
    (Decimal("65.00"), 100),
]


# =====================================================
# DTI Score
# =====================================================

def calculate_dti_score(dti: Decimal) -> int:
    if dti is None:
        return 0

    dti = Decimal(dti)

    for threshold, points in DTI_WEIGHTS:
        if dti <= threshold:
            return points

    return 0


# =====================================================
# Income Score
# =====================================================

def calculate_income_score(income: Decimal) -> int:
    if not income or income <= 0:
        return 0

    income_float = float(income)
    value = min(300, math.log10(income_float + 1) * 60)

    return int(max(0, value))


# =====================================================
# Stability Score
# =====================================================

def calculate_stability_score(obligations_total: Decimal) -> int:
    if obligations_total is None:
        return 100

    if obligations_total > 0:
        return 50

    return 100


# =====================================================
# Risk Category
# =====================================================

def determine_risk(score: int) -> str:
    if score >= 800:
        return "LOW"
    elif score >= 650:
        return "MEDIUM"
    elif score >= 500:
        return "HIGH"
    return "REJECT"


# =====================================================
# Approval Probability
# =====================================================

def calculate_probability(score: int) -> Decimal:
    p = 1 / (1 + math.exp(-0.01 * (score - 600)))

    return Decimal(p * 100).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )


# =====================================================
# Main Scoring Engine
# =====================================================

@transaction.atomic
def generate_credit_score(profile: FinancialProfile) -> dict:
    """
    Основная функция генерации скоринга.
    Если результат не изменился — новая запись не создаётся.
    """

    if not profile:
        raise ValueError("FinancialProfile is required")

    # Безопасные значения
    dti_ratio = profile.dti_ratio or Decimal("0.00")
    income = profile.monthly_income_total or Decimal("0.00")
    obligations_total = profile.monthly_obligations_total or Decimal("0.00")
    version = profile.profile_version or 1

    # Расчёт компонентов
    dti_score = calculate_dti_score(dti_ratio)
    income_score = calculate_income_score(income)
    stability_score = calculate_stability_score(obligations_total)
    version_factor = min(version * 10, 100)

    # Итоговый score
    total_score = dti_score + income_score + stability_score + version_factor
    total_score = min(total_score, 1000)

    risk = determine_risk(total_score)
    probability = calculate_probability(total_score)

    # =====================================================
    # 🔥 НОВАЯ ЛОГИКА — ПРОВЕРКА ДУБЛИКАТА
    # =====================================================

    last_score = (
        CreditScore.objects
        .filter(user=profile.user)
        .order_by("-created_at")
        .first()
    )

    if last_score:
        if (
            last_score.score == total_score and
            last_score.risk_category == risk and
            last_score.approval_probability == probability
        ):
            # Ничего не изменилось — возвращаем старый результат
            return {
                "score": last_score.score,
                "risk_category": last_score.risk_category,
                "approval_probability": last_score.approval_probability,
                "components": {
                    "dti_score": dti_score,
                    "income_score": income_score,
                    "stability_score": stability_score,
                    "version_factor": version_factor
                },
                "model_version": "v1.1",
                "unchanged": True
            }

    # =====================================================
    # Если изменилось — создаём новую запись
    # =====================================================

    credit_score = CreditScore.objects.create(
        user=profile.user,
        profile_version=version,
        score=total_score,
        risk_category=risk,
        approval_probability=probability,
    )

    return {
        "score": total_score,
        "risk_category": risk,
        "approval_probability": probability,
        "components": {
            "dti_score": dti_score,
            "income_score": income_score,
            "stability_score": stability_score,
            "version_factor": version_factor
        },
        "model_version": "v1.1",
        "unchanged": False
    }