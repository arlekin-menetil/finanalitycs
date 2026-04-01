from rest_framework import serializers
from .models import Bank, BankProduct


# =====================================
# 🏦 Bank Serializer
# =====================================

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = [
            "id",
            "name",
            "short_name",
            "logo",
            "rating",
        ]


# =====================================
# 💳 Bank Product Serializer
# =====================================

class BankProductSerializer(serializers.ModelSerializer):
    bank = BankSerializer(read_only=True)

    class Meta:
        model = BankProduct
        fields = [
            "id",
            "name",
            "bank",
            "interest_rate",
            "max_amount",
            "term",
            "description",
            "product_type",
            "source_url",
        ]