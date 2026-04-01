import math
from decimal import Decimal
from profiles.models import FinancialProfile
from credit_analysis.models import CreditReport


class FeatureBuilder:

    def __init__(self, user):
        self.user = user

    def build(self):
        profile = FinancialProfile.objects.filter(user=self.user).first()
        report = CreditReport.objects.filter(user=self.user).order_by("-created_at").first()

        if not profile:
            return None

        income = float(profile.monthly_income_total or 0)
        obligations = float(profile.total_monthly_obligations or 0)
        dti = float(profile.dti_ratio or 0)

        # Если отчёта нет — используем безопасные дефолты
        history_score = float(getattr(report, "history_score", 650) if report else 650)
        active_loans = float(getattr(report, "active_loans", 2) if report else 2)
        delinquency_count = float(getattr(report, "delinquency_count", 0) if report else 0)

        return {
            "income": income,
            "dti": dti,
            "history_score": history_score,
            "active_loans": active_loans,
            "delinquency_count": delinquency_count,
        }