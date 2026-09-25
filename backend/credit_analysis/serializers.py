from rest_framework import serializers

from .models import (
    CreditReport,
    CreditContract,
)


# ==========================================================
# CREDIT CONTRACT
# ==========================================================

class CreditContractSerializer(serializers.ModelSerializer):

    class Meta:

        model = CreditContract

        fields = [

            "id",

            "bank_name",

            "contract_number",

            "product_name",

            "currency",

            "issued_amount",

            "current_debt",

            "overdue_debt",

            "monthly_payment",

            "interest_rate",

            "issued_date",

            "closed_date",

            "status",

        ]


# ==========================================================
# CREDIT REPORT
# ==========================================================

class CreditReportSerializer(serializers.ModelSerializer):

    contracts = CreditContractSerializer(
        many=True,
        read_only=True,
    )

    # ------------------------------------------
    # aliases for frontend
    # ------------------------------------------

    income = serializers.DecimalField(
        source="extracted_income",
        max_digits=18,
        decimal_places=2,
        read_only=True,
    )

    total_debt = serializers.DecimalField(
        source="extracted_debt",
        max_digits=18,
        decimal_places=2,
        read_only=True,
    )

    contracts_count = serializers.IntegerField(
        read_only=True,
    )

    contracts_total = serializers.IntegerField(
        source="contracts_count",
        read_only=True,
    )

    class Meta:

        model = CreditReport

        fields = [

            "id",

            "full_name",

            "passport",

            "phone",

            "credit_score",

            "risk_class",

            "score_version",

            # -------------------------
            # old names
            # -------------------------

            "extracted_income",

            "extracted_debt",

            "contracts_count",

            # -------------------------
            # new frontend names
            # -------------------------

            "income",

            "total_debt",

            "contracts_total",

            # -------------------------

            "overdue_debt",

            "parsed",

            "created_at",

            "updated_at",

            "contracts",

        ]


# ==========================================================
# SHORT REPORT
# ==========================================================

class CreditReportShortSerializer(serializers.ModelSerializer):

    income = serializers.DecimalField(
        source="extracted_income",
        max_digits=18,
        decimal_places=2,
        read_only=True,
    )

    total_debt = serializers.DecimalField(
        source="extracted_debt",
        max_digits=18,
        decimal_places=2,
        read_only=True,
    )

    contracts_total = serializers.IntegerField(
        source="contracts_count",
        read_only=True,
    )

    class Meta:

        model = CreditReport

        fields = [

            "id",

            "credit_score",

            "risk_class",

            "contracts_count",

            "contracts_total",

            "income",

            "total_debt",

            "overdue_debt",

            "parsed",

            "created_at",

        ]