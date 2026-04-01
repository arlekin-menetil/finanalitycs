from rest_framework import serializers
from scoring.models import CreditScore


class CreditScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditScore
        fields = [
            "id",
            "score",
            "risk_category",
            "approval_probability",
            "profile_version",
            "created_at",
        ]