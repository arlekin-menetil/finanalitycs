from rest_framework import serializers
from .models import (
    FinancialProfile,
    Income,
    Obligation,
    Employment,
    Identity
)


# ============================
# 💰 Income Serializer
# ============================

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = [
            "id",
            "source",
            "amount",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# ============================
# 💳 Obligation Serializer
# ============================

class ObligationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obligation
        fields = [
            "id",
            "description",
            "monthly_payment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# ============================
# 💼 Employment Serializer
# ============================

class EmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employment
        fields = [
            "company_name",
            "position",
            "salary",
            "work_experience_months",
            "is_company_verified",
        ]


# ============================
# 🪪 Identity Serializer
# ============================

class IdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Identity
        fields = [
            "passport_series",
            "passport_number",
        ]


# ============================
# 🧠 Financial Profile Serializer (FIXED)
# ============================

class FinancialProfileSerializer(serializers.ModelSerializer):

    incomes = IncomeSerializer(many=True, read_only=True)
    obligations = ObligationSerializer(many=True, read_only=True)

    # 💣 KYC (старый способ)
    employment = serializers.SerializerMethodField()
    identity = serializers.SerializerMethodField()

    # 💣 НОВОЕ: прямые поля
    full_name = serializers.CharField(read_only=True)
    birth_date = serializers.DateField(read_only=True)
    passport = serializers.CharField(read_only=True)
    job_type = serializers.CharField(read_only=True)
    experience = serializers.IntegerField(read_only=True)

    income = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
    expenses = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
    credit_score = serializers.IntegerField(read_only=True)

    is_profile_completed = serializers.BooleanField(read_only=True)

    class Meta:
        model = FinancialProfile
        fields = [
            # 💣 KYC (новое)
            "full_name",
            "birth_date",
            "passport",
            "job_type",
            "experience",

            # 💣 финансы (новое)
            "income",
            "expenses",
            "credit_score",

            # === агрегаты ===
            "monthly_income_total",
            "monthly_obligations_total",
            "net_balance",
            "dti_ratio",

            # === статус ===
            "is_profile_completed",

            # === system ===
            "profile_version",
            "calculated_at",

            # === relations ===
            "incomes",
            "obligations",

            # 💣 legacy (оставляем)
            "employment",
            "identity",
        ]

        read_only_fields = fields

    # ============================
    # 💼 Employment getter
    # ============================

    def get_employment(self, obj):
        user = obj.user

        if hasattr(user, "employment"):
            return EmploymentSerializer(user.employment).data

        return None

    # ============================
    # 🪪 Identity getter
    # ============================

    def get_identity(self, obj):
        user = obj.user

        if hasattr(user, "identity"):
            return IdentitySerializer(user.identity).data

        return None