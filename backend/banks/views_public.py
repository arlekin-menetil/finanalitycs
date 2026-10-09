from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Bank, BankProduct


class PublicStatsAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "banks": Bank.objects.filter(type="bank").count(),
            "products": BankProduct.objects.count(),
        })
