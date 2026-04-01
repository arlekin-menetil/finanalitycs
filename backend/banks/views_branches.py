from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Bank, BankBranch


# ==================================================
# BRANCHES OF ONE BANK
# ==================================================

class BankBranchesAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, bank_id):

        try:
            bank = Bank.objects.get(id=bank_id)
        except Bank.DoesNotExist:
            return Response(
                {"error": "Bank not found"},
                status=404
            )

        branches = BankBranch.objects.filter(bank=bank, is_active=True)

        result = []

        for branch in branches:

            result.append({
                "id": branch.id,
                "name": branch.name,

                "city": branch.city,
                "address": branch.address,

                "phone": branch.phone,
                "working_hours": branch.working_hours,

                "lat": float(branch.latitude) if branch.latitude else None,
                "lng": float(branch.longitude) if branch.longitude else None
            })

        return Response({
            "bank": bank.short_name,
            "branches": result
        })


# ==================================================
# ALL BRANCHES (MAP)
# ==================================================

class BankBranchesMapAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        branches = BankBranch.objects.select_related("bank").filter(is_active=True)

        result = []

        for branch in branches:

            result.append({

                "bank_id": branch.bank.id,
                "bank_name": branch.bank.short_name,

                "name": branch.name,

                "city": branch.city,
                "address": branch.address,

                "phone": branch.phone,
                "working_hours": branch.working_hours,

                "lat": float(branch.latitude) if branch.latitude else None,
                "lng": float(branch.longitude) if branch.longitude else None

            })

        return Response(result)
