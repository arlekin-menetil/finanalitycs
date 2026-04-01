from rest_framework import serializers
from .models import Transaction


# ============================
# Transfer Serializer
# ============================

class TransferSerializer(serializers.Serializer):
    from_account = serializers.UUIDField()
    to_account = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value


# ============================
# Transaction List Serializer
# ============================

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "from_account",
            "to_account",
            "amount",
            "status",
            "created_at",
        ]
        read_only_fields = fields