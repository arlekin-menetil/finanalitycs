import math

from decimal import (
    Decimal,
    ROUND_HALF_UP,
)

from django.db import transaction

from profiles.models import FinancialProfile
from scoring.models import CreditScore
from credit_analysis.models import CreditReport


# ==========================================================
# BANK SCORING ENGINE v5
# ==========================================================

MIN_SCORE = 300
MAX_SCORE = 850

BASE_SCORE = 300

MAX_INCOME_SCORE = 180
MAX_DTI_SCORE = 180
MAX_EMPLOYMENT_SCORE = 80
MAX_PROFILE_SCORE = 40
MAX_HISTORY_SCORE = 70

PROBABILITY_CENTER = 620
PROBABILITY_FACTOR = Decimal("0.018")


# ==========================================================
# HELPERS
# ==========================================================

def decimal(value):

    try:

        if value is None:

            return Decimal("0")

        return Decimal(str(value))

    except Exception:

        return Decimal("0")


def money(value):

    return decimal(value).quantize(

        Decimal("1"),

        rounding=ROUND_HALF_UP,

    )


def clamp(value, minimum, maximum):

    return max(

        minimum,

        min(value, maximum),

    )


# ==========================================================
# LAST CREDIT REPORT
# ==========================================================

def get_credit_report(profile):

    return (

        CreditReport.objects.filter(

            user=profile.user,

            parsed=True,

        )

        .order_by("-created_at")

        .first()

    )


# ==========================================================
# RISK
# ==========================================================

def determine_risk(score):

    if score >= 760:

        return "LOW"

    elif score >= 650:

        return "MEDIUM"

    elif score >= 550:

        return "HIGH"

    return "REJECT"


# ==========================================================
# APPROVAL PROBABILITY
# ==========================================================

def calculate_probability(score):

    probability = (

        1 /

        (

            1 +

            math.exp(

                -float(PROBABILITY_FACTOR)

                *

                (score - PROBABILITY_CENTER)

            )

        )

    )

    return Decimal(

        probability

    ).quantize(

        Decimal("0.01"),

        rounding=ROUND_HALF_UP,

    )
# ==========================================================
# INCOME SCORE
# ==========================================================

def calculate_income_score(profile):

    income = decimal(

        profile.monthly_income_total

    )

    if income >= Decimal("50000000"):

        return 180

    elif income >= Decimal("30000000"):

        return 170

    elif income >= Decimal("20000000"):

        return 160

    elif income >= Decimal("15000000"):

        return 145

    elif income >= Decimal("10000000"):

        return 130

    elif income >= Decimal("7000000"):

        return 115

    elif income >= Decimal("5000000"):

        return 95

    elif income >= Decimal("3000000"):

        return 75

    elif income >= Decimal("1500000"):

        return 55

    return 25


# ==========================================================
# DTI SCORE
# ==========================================================

def calculate_dti_score(profile):

    dti = decimal(

        profile.dti_ratio

    )

    if dti <= 10:

        return 180

    elif dti <= 20:

        return 165

    elif dti <= 30:

        return 145

    elif dti <= 40:

        return 120

    elif dti <= 50:

        return 90

    elif dti <= 60:

        return 55

    elif dti <= 70:

        return 25

    return 0


# ==========================================================
# EMPLOYMENT SCORE
# ==========================================================

def calculate_employment_score(profile):

    score = 0

    months = profile.work_experience_months or 0

    if months >= 120:

        score += 40

    elif months >= 60:

        score += 35

    elif months >= 36:

        score += 28

    elif months >= 24:

        score += 22

    elif months >= 12:

        score += 15

    elif months >= 6:

        score += 10

    if profile.employment_verified:

        score += 25

    if profile.is_current_employee:

        score += 15

    return clamp(

        score,

        0,

        MAX_EMPLOYMENT_SCORE,

    )


# ==========================================================
# PROFILE SCORE
# ==========================================================

def calculate_profile_score(profile):

    score = 0

    if profile.full_name:

        score += 5

    if profile.passport:

        score += 5

    if profile.birth_date:

        score += 5

    if profile.job_type:

        score += 5

    if profile.company_name:

        score += 5

    if profile.company_inn:

        score += 5

    if profile.position:

        score += 5

    if profile.is_profile_completed:

        score += 5

    return clamp(

        score,

        0,

        MAX_PROFILE_SCORE,

    )
# ==========================================================
# CREDIT HISTORY SCORE
# ==========================================================

def calculate_credit_history_score(profile):

    report = get_credit_report(profile)

    if report is None:

        return 0

    score = 0

    # ==========================================
    # CREDIT SCORE (INFOKREDIT)
    # ==========================================

    bureau_score = report.credit_score or 0

    if bureau_score >= 900:

        score += 35

    elif bureau_score >= 800:

        score += 30

    elif bureau_score >= 700:

        score += 25

    elif bureau_score >= 600:

        score += 18

    elif bureau_score >= 500:

        score += 10

    # ==========================================
    # OVERDUE
    # ==========================================

    overdue = decimal(

        report.overdue_debt

    )

    if overdue > 0:

        if overdue >= Decimal("50000000"):

            score -= 40

        elif overdue >= Decimal("10000000"):

            score -= 30

        elif overdue >= Decimal("3000000"):

            score -= 20

        else:

            score -= 10

    else:

        score += 15

    # ==========================================
    # CONTRACTS
    # ==========================================

    contracts = report.contracts_count or 0

    if contracts == 0:

        score += 10

    elif contracts <= 2:

        score += 15

    elif contracts <= 4:

        score += 10

    elif contracts <= 6:

        score += 5

    elif contracts <= 10:

        score -= 5

    else:

        score -= 10

    # ==========================================
    # RISK CLASS
    # ==========================================

    risk = (report.risk_class or "").upper()

    if risk == "LOW":

        score += 10

    elif risk == "MEDIUM":

        score += 5

    elif risk == "HIGH":

        score -= 10

    return clamp(

        score,

        0,

        MAX_HISTORY_SCORE,

    )


# ==========================================================
# RECOMMENDED CREDIT LIMIT
# ==========================================================

def calculate_credit_limit(profile, final_score):

    income = decimal(

        profile.monthly_income_total

    )

    balance = decimal(

        profile.net_balance

    )

    if balance <= 0:

        return Decimal("0")

    coefficient = Decimal("1.0")

    if final_score >= 800:

        coefficient = Decimal("18")

    elif final_score >= 760:

        coefficient = Decimal("15")

    elif final_score >= 700:

        coefficient = Decimal("12")

    elif final_score >= 650:

        coefficient = Decimal("9")

    elif final_score >= 600:

        coefficient = Decimal("6")

    elif final_score >= 500:

        coefficient = Decimal("3")

    return money(

        balance * coefficient

    )
# ==========================================================
# FINAL SCORE
# ==========================================================

@transaction.atomic
def calculate_credit_score(profile: FinancialProfile):

    # ==========================================
    # COMPONENTS
    # ==========================================

    income_score = calculate_income_score(
        profile
    )

    dti_score = calculate_dti_score(
        profile
    )

    employment_score = calculate_employment_score(
        profile
    )

    profile_score = calculate_profile_score(
        profile
    )

    history_score = calculate_credit_history_score(
        profile
    )

    # ==========================================
    # TOTAL SCORE
    # ==========================================

    total_score = (

        BASE_SCORE

        + income_score

        + dti_score

        + employment_score

        + profile_score

        + history_score

    )

    total_score = clamp(

        int(total_score),

        MIN_SCORE,

        MAX_SCORE,

    )

    # ==========================================
    # RISK CATEGORY
    # ==========================================

    risk = determine_risk(
        total_score
    )

    # ==========================================
    # APPROVAL PROBABILITY
    # ==========================================

    probability = calculate_probability(
        total_score
    )

    # ==========================================
    # RECOMMENDED LIMIT
    # ==========================================

    recommended_limit = calculate_credit_limit(

        profile,

        total_score,

    )

    # ==========================================
    # SAVE SCORING HISTORY
    # ==========================================

    score = CreditScore.objects.create(

        user=profile.user,

        profile_version=profile.profile_version,

        score=total_score,

        risk_category=risk,

        approval_probability=probability,

        recommended_limit=recommended_limit,

        monthly_income=profile.monthly_income_total,

        monthly_obligations=profile.monthly_obligations_total,

        net_balance=profile.net_balance,

        dti_ratio=profile.dti_ratio,

        income_score=income_score,

        dti_score=dti_score,

        employment_score=employment_score,

        history_score=history_score,

        profile_score=profile_score,

    )

    return score


# ==========================================================
# BACKWARD COMPATIBILITY
# ==========================================================

def generate_credit_score(
    profile,
):
    """
    Совместимость со старым API проекта.
    """

    return calculate_credit_score(
        profile
    )