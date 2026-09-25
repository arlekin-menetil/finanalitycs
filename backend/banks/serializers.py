from rest_framework import serializers
from .models import Bank, BankProduct, AggregatedProduct

# =====================================
# 🏦 Bank Serializer
# =====================================


class BankSerializer(serializers.ModelSerializer):
    is_unknown = serializers.SerializerMethodField()

    class Meta:
        model = Bank
        fields = [
            "id",
            "name",
            "short_name",
            "logo",
            "is_unknown",
        ]

    def get_is_unknown(self, obj):
        return False


# =====================================
# 💳 Bank Product Serializer
# =====================================


class BankProductSerializer(serializers.ModelSerializer):

    bank = serializers.SerializerMethodField()
    interest_rate = serializers.SerializerMethodField()
    max_amount = serializers.SerializerMethodField()

    # 🔥 НОВЫЕ ПОЛЯ
    requirements = serializers.SerializerMethodField()
    fee = serializers.SerializerMethodField()
    loan_type = serializers.SerializerMethodField()
    real_online = serializers.SerializerMethodField()

    # 🔥 ФИКС: добавили source как метод
    source = serializers.SerializerMethodField()
    currency = serializers.CharField(read_only=True)
    bank_name = serializers.CharField(read_only=True)
    raw_data = serializers.JSONField(read_only=True)

    class Meta:
        model = BankProduct
        fields = [
            "id",
            "name",
            "bank_name",
            "bank",
            "currency",
            "interest_rate",
            "max_amount",
            "term",
            "description",
            "raw_data",
            "product_type",
            "source_url",
            "source",
            "requirements",
            "fee",
            "loan_type",
            "real_online",
        ]

    # 💣 безопасный банк
    def get_bank(self, obj):
        if not obj.bank:
            return {
                "id": None,
                "name": "Не указан",
                "short_name": None,
                "logo": None,
                "is_unknown": True,
            }

        return {
            "id": obj.bank.id,
            "name": obj.bank.name,
            "short_name": obj.bank.short_name,
            # 🔥 ФИКС
            "logo": obj.bank.logo if obj.bank.logo else None,
            "is_unknown": False,
        }

    # 💣 безопасные числа
    def get_interest_rate(self, obj):
        try:
            return float(obj.interest_rate) if obj.interest_rate is not None else None
        except:
            return None

    def get_max_amount(self, obj):
        try:
            return float(obj.max_amount) if obj.max_amount is not None else None
        except:
            return None

    # 🔥 НОВЫЕ ГЕТТЕРЫ

    def get_requirements(self, obj):
        return obj.requirements if obj.requirements else None

    def get_fee(self, obj):
        return obj.fee if obj.fee else None

    def get_loan_type(self, obj):
        return obj.loan_type if obj.loan_type else None

    def get_real_online(self, obj):
        return obj.real_online if obj.real_online is not None else False

    # 🔥 SOURCE (теперь безопасно)
    def get_source(self, obj):
        if obj.source_url and "bank.uz" in obj.source_url:
            return "bank.uz"
        return "external"


# =====================================
# 🔥 Aggregated Product (SHORT)
# =====================================


class AggregatedProductSerializer(serializers.ModelSerializer):
    best_rate = serializers.SerializerMethodField()
    min_rate = serializers.SerializerMethodField()
    max_rate = serializers.SerializerMethodField()

    class Meta:
        model = AggregatedProduct
        fields = [
            "id",
            "name",
            "normalized_name",
            "best_rate",
            "min_rate",
            "max_rate",
            "offers_count",
            "is_online",
        ]

    def get_best_rate(self, obj):
        return float(obj.best_rate) if obj.best_rate else None

    def get_min_rate(self, obj):
        return float(obj.min_rate) if obj.min_rate else None

    def get_max_rate(self, obj):
        return float(obj.max_rate) if obj.max_rate else None


# =====================================
# 🔥 Aggregated Product DETAIL (с офферами)
# =====================================


class AggregatedProductDetailSerializer(serializers.ModelSerializer):
    offers = BankProductSerializer(many=True, read_only=True)

    best_rate = serializers.SerializerMethodField()
    min_rate = serializers.SerializerMethodField()
    max_rate = serializers.SerializerMethodField()

    class Meta:
        model = AggregatedProduct
        fields = [
            "id",
            "name",
            "normalized_name",
            "best_rate",
            "min_rate",
            "max_rate",
            "offers_count",
            "is_online",
            "offers",
        ]

    def get_best_rate(self, obj):
        return float(obj.best_rate) if obj.best_rate else None

    def get_min_rate(self, obj):
        return float(obj.min_rate) if obj.min_rate else None

    def get_max_rate(self, obj):
        return float(obj.max_rate) if obj.max_rate else None
