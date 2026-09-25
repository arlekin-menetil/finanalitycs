from rest_framework import serializers

from scoring.models import CreditScore


class CreditScoreSerializer(serializers.ModelSerializer):

    approval_probability = serializers.FloatField()

    recommended_limit = serializers.FloatField()

    monthly_income = serializers.FloatField()

    monthly_obligations = serializers.FloatField()

    net_balance = serializers.FloatField()

    dti_ratio = serializers.FloatField()

    class Meta:

        model = CreditScore

        fields = (

            "id",

            # =====================================
            # MAIN
            # =====================================

            "score",

            "risk_category",

            "approval_probability",

            "recommended_limit",

            "profile_version",

            # =====================================
            # FINANCIAL
            # =====================================

            "monthly_income",

            "monthly_obligations",

            "net_balance",

            "dti_ratio",

            # =====================================
            # AI SCORES
            # =====================================

            "income_score",

            "dti_score",

            "employment_score",

            "history_score",

            "profile_score",

            # =====================================
            # DATE
            # =====================================

            "created_at",

        )

        read_only_fields = fields