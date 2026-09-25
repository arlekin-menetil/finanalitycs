from decimal import Decimal, ROUND_HALF_UP

from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from profiles.models import (
    FinancialProfile,
    FinancialProfileHistory,
    Income,
    Obligation,
)

from credit_analysis.models import CreditReport


@transaction.atomic
def recalculate_profile(profile: FinancialProfile):
    """
    Пересчет финансового профиля.

    Источник доходов:

    1. Income
    2. Infokredit (если Income отсутствует)
    3. Поле profile.income

    Источник обязательств:

    1. Obligation
    2. Поле profile.expenses
    """

    # =====================================================
    # CREDIT REPORT
    # =====================================================

    credit_report = (
        CreditReport.objects.filter(
            user=profile.user,
            parsed=True,
        )
        .order_by("-created_at")
        .first()
    )

    # =====================================================
    # ДОХОДЫ
    # =====================================================

    income_total = (
        Income.objects.filter(
            profile=profile
        ).aggregate(
            total=Sum("amount")
        )["total"]
    )

    if income_total is None:

        if (
            credit_report
            and credit_report.extracted_income > 0
        ):

            income_total = Decimal(
                credit_report.extracted_income
            )

        else:

            income_total = Decimal(
                profile.income or 0
            )

    income_total = max(
        Decimal("0"),
        income_total,
    )

    # =====================================================
    # ОБЯЗАТЕЛЬСТВА
    # =====================================================

    obligation_total = (
        Obligation.objects.filter(
            profile=profile
        ).aggregate(
            total=Sum("monthly_payment")
        )["total"]
    )

    if obligation_total is None:

        obligation_total = Decimal(
            profile.expenses or 0
        )

    obligation_total = max(
        Decimal("0"),
        obligation_total,
    )

    # =====================================================
    # NET BALANCE
    # =====================================================

    net_balance = income_total - obligation_total

    # =====================================================
    # DTI
    # =====================================================

    if income_total > 0:

        dti = (
            obligation_total
            / income_total
            * Decimal("100")
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    else:

        dti = Decimal("0.00")

    # =====================================================
    # HISTORY SNAPSHOT
    # =====================================================

    if profile.calculated_at:

        FinancialProfileHistory.objects.create(

            profile=profile,

            monthly_income_total=profile.monthly_income_total,

            monthly_obligations_total=profile.monthly_obligations_total,

            net_balance=profile.net_balance,

            dti_ratio=profile.dti_ratio,

            version=profile.profile_version,

            calculated_at=profile.calculated_at,

        )

    # =====================================================
    # UPDATE PROFILE
    # =====================================================

    profile.monthly_income_total = income_total

    profile.monthly_obligations_total = obligation_total

    profile.net_balance = net_balance

    profile.dti_ratio = dti

    profile.profile_version += 1

    profile.calculated_at = timezone.now()

    profile.save(
        update_fields=[
            "monthly_income_total",
            "monthly_obligations_total",
            "net_balance",
            "dti_ratio",
            "profile_version",
            "calculated_at",
            "updated_at",
        ]
    )