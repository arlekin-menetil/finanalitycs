from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.db.models import Q, Value
from django.db.models.functions import Coalesce

from .models import Bank
from .recommendation_engine import get_best_products


# ==================================================
# 🏦 BANK LIST
# ==================================================
class BankListAPIView(APIView):
    """
    Public API: список банков
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):

        search = request.GET.get("search")

        banks = Bank.objects.annotate(
            display_name=Coalesce("name", "short_name", Value(""))
        )

        if search:
            banks = banks.filter(
                Q(name__icontains=search) |
                Q(short_name__icontains=search)
            )

        banks = banks.order_by("display_name")

        data = [
            {
                "id": b.id,
                "name": b.display_name if b.display_name else b.short_name,
                "short_name": b.short_name,
            }
            for b in banks
        ]

        return Response({
            "total": len(data),
            "banks": data
        })


# ==================================================
# 💣 RECOMMENDATIONS API (ГЛАВНЫЙ)
# ==================================================
class RecommendationsAPIView(APIView):
    """
    Public API: рекомендации кредитов
    (используется фронтом)
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):

        limit = request.GET.get("limit", 5)

        try:
            limit = int(limit)
        except:
            limit = 5

        products = get_best_products(limit=limit)

        data = []

        for p in products:
            data.append({
                "product_id": p.id,
                "bank_id": p.bank.id if p.bank else None,
                "bank_name": p.bank.name if p.bank else "Bank",
                "product_name": p.name,
                "interest_rate": float(p.interest_rate or 0),

                # 💣 ЗАГЛУШКИ (под твой фронт)
                "approval_probability": 75,
                "ranking_score": 80,
                "loan_limit_hint": None,
                "website": None,

                # 💣 для UI
                "is_featured": False
            })

        return Response({
            "total": len(data),
            "recommendations": data
        })


# ==================================================
# 💣 BACKWARD COMPATIBILITY (ВАЖНО)
# ==================================================
class RecommendationAPIView(RecommendationsAPIView):
    """
    Алиас для старых импортов (чтобы не ломался urls.py)
    """
    pass