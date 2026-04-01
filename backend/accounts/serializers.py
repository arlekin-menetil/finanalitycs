from rest_framework import serializers
from .models import BankAccount


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ["id", "account_number", "currency", "is_active", "created_at"]
        read_only_fields = ["id", "account_number", "created_at"]