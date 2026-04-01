from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from profiles.models import (
    FinancialProfile,
    FinancialProfileHistory,
    Income,
    Obligation
)


@transaction.atomic
def recalculate_profile(profile: FinancialProfile):
    """
    Полный пересчёт финансового профиля.
    Создаёт snapshot перед обновлением.
    """

    # === 1. Считаем суммы через SQL ===
    income_agg = Income.objects.filter(profile=profile).aggregate(
        total=Sum("amount")
    )

    obligation_agg = Obligation.objects.filter(profile=profile).aggregate(
        total=Sum("monthly_payment")
    )

    total_income = income_agg["total"] or Decimal("0.00")
    total_obligations = obligation_agg["total"] or Decimal("0.00")

    # === 2. Net balance ===
    net_balance = total_income - total_obligations

    # === 3. DTI calculation ===
    if total_income == Decimal("0.00"):
        dti = Decimal("0.00")
    else:
        dti = (
            (total_obligations / total_income) * Decimal("100")
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # === 4. Snapshot (только если это не первый расчёт) ===
    if profile.calculated_at is not None:
        FinancialProfileHistory.objects.create(
            profile=profile,
            monthly_income_total=profile.monthly_income_total,
            monthly_obligations_total=profile.monthly_obligations_total,
            net_balance=profile.net_balance,
            dti_ratio=profile.dti_ratio,
            version=profile.profile_version,
            calculated_at=profile.calculated_at,
        )

    # === 5. Обновляем профиль ===
    profile.monthly_income_total = total_income
    profile.monthly_obligations_total = total_obligations
    profile.net_balance = net_balance
    profile.dti_ratio = dti
    profile.profile_version += 1
    profile.calculated_at = timezone.now()

    profile.save(update_fields=[
        "monthly_income_total",
        "monthly_obligations_total",
        "net_balance",
        "dti_ratio",
        "profile_version",
        "calculated_at",
        "updated_at"
    ])