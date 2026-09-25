from rest_framework import serializers

from .models import (
    FinancialProfile,
    Income,
    Obligation,
    Employment,
    Identity,
)


# ============================
# 💰 Income Serializer
# ============================

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = (
            "id",
            "source",
            "amount",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


# ============================
# 💳 Obligation Serializer
# ============================

class ObligationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obligation
        fields = (
            "id",
            "description",
            "monthly_payment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


# ============================
# 💼 Legacy Employment Serializer
# (оставляем для совместимости)
# ============================

class EmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employment
        fields = (
            "company_name",
            "position",
            "salary",
            "work_experience_months",
            "is_company_verified",
        )


# ============================
# 🪪 Identity Serializer
# ============================

class IdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Identity
        fields = (
            "passport_series",
            "passport_number",
        )


# ============================
# 🧠 Financial Profile Serializer
# ============================

class FinancialProfileSerializer(serializers.ModelSerializer):

    incomes = IncomeSerializer(many=True, read_only=True)
    obligations = ObligationSerializer(many=True, read_only=True)

    identity = serializers.SerializerMethodField()

    # legacy
    employment = serializers.SerializerMethodField()

    class Meta:
        model = FinancialProfile

        fields = (

            # ======================
            # KYC
            # ======================

            "full_name",
            "birth_date",
            "passport",
            "job_type",

            # ======================
            # Employment
            # ======================

            "employment_document",
            "company_name",
            "company_inn",
            "position",
            "department",

            "employment_start",
            "employment_end",

            "is_current_employee",

            "employment_verified",

            "employment_pinfl",

            "work_experience_months",

            # ======================
            # Finance
            # ======================

            "income",
            "expenses",
            "credit_score",

            # ======================
            # Aggregates
            # ======================

            "monthly_income_total",
            "monthly_obligations_total",
            "net_balance",
            "dti_ratio",

            # ======================
            # Status
            # ======================

            "is_profile_completed",

            # ======================
            # System
            # ======================

            "profile_version",
            "calculated_at",

            # ======================
            # Relations
            # ======================

            "incomes",
            "obligations",

            # ======================
            # Legacy
            # ======================

            "employment",
            "identity",
        )

        read_only_fields = fields

    # =====================================
    # Legacy Employment
    # =====================================

    def get_employment(self, obj):

        user = obj.user

        if hasattr(user, "employment"):
            return EmploymentSerializer(
                user.employment
            ).data

        return None

    # =====================================
    # Identity
    # =====================================

    def get_identity(self, obj):

        user = obj.user

        if hasattr(user, "identity"):
            return IdentitySerializer(
                user.identity
            ).data

        return None