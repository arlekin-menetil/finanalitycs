from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from django.db.models import Q

from .models import (
    Bank,
    BankBranch,
)


# ==================================================
# 🔥 SERIALIZER
# ==================================================
def serialize_branch(branch):

    bank = getattr(branch, "bank", None)

    return {
        # ==========================================
        # 💣 IDS
        # ==========================================
        "id": branch.pk,
        "bank_id": (bank.pk if bank else None),
        # ==========================================
        # 💣 BANK
        # ==========================================
        "bank_name": (bank.short_name or bank.name if bank else None),
        # ==========================================
        # 💣 BRANCH
        # ==========================================
        "name": branch.name,
        "city": branch.city,
        "address": branch.address,
        "normalized_address": (branch.normalized_address),
        # ==========================================
        # 💣 CONTACTS
        # ==========================================
        "phone": branch.phone,
        "email": branch.email,
        "working_hours": (branch.working_hours),
        # ==========================================
        # 💣 GEO
        # ==========================================
        "latitude": (float(branch.latitude) if branch.latitude else None),
        "longitude": (float(branch.longitude) if branch.longitude else None),
        # ==========================================
        # 💣 FRONTEND SHORTCUTS
        # ==========================================
        "lat": (float(branch.latitude) if branch.latitude else None),
        "lng": (float(branch.longitude) if branch.longitude else None),
        # ==========================================
        # 💣 STATUS
        # ==========================================
        "geocoded": branch.geocoded,
        "is_active": branch.is_active,
        # ==========================================
        # 💣 META
        # ==========================================
        "source_url": branch.source_url,
        "external_id": branch.external_id,
        "created_at": branch.created_at,
        "updated_at": branch.updated_at,
    }


# ==================================================
# 🏦 SINGLE BANK BRANCHES
# ==================================================
class BankBranchesAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, bank_id):

        try:

            bank = Bank.objects.get(pk=bank_id)

        except Bank.DoesNotExist:

            return Response(
                {"error": "Bank not found"}, status=status.HTTP_404_NOT_FOUND
            )

        branches = (
            BankBranch.objects.filter(bank=bank, is_active=True)
            .select_related("bank")
            .order_by("city", "address")
        )

        result = [serialize_branch(branch) for branch in branches]

        return Response(
            {
                "bank_id": bank.pk,
                "bank": (bank.short_name or bank.name),
                "branches_count": len(result),
                "branches": result,
            }
        )


# ==================================================
# 🗺 ALL BRANCHES MAP API
# ==================================================
class BankBranchesMapAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        # ==========================================
        # 💣 FILTERS
        # ==========================================
        bank_id = request.GET.get("bank_id")

        city = request.GET.get("city")

        q = request.GET.get("q")

        geocoded = request.GET.get("geocoded")

        # ==========================================
        # 💣 QUERYSET
        # ==========================================
        branches = BankBranch.objects.select_related("bank").filter(is_active=True)

        # ==========================================
        # 💣 BANK FILTER
        # ==========================================
        if bank_id:

            branches = branches.filter(bank_id=bank_id)

        # ==========================================
        # 💣 CITY FILTER
        # ==========================================
        if city:

            branches = branches.filter(city__icontains=city)

        # ==========================================
        # 💣 SEARCH
        # ==========================================
        if q:

            branches = branches.filter(
                Q(address__icontains=q)
                | Q(city__icontains=q)
                | Q(name__icontains=q)
                | Q(bank__name__icontains=q)
                | Q(bank__short_name__icontains=q)
            )

        # ==========================================
        # 💣 GEOCODED FILTER
        # ==========================================
        if geocoded == "true":

            branches = branches.filter(
                latitude__isnull=False,
                longitude__isnull=False,
            )

        # ==========================================
        # 💣 ORDER
        # ==========================================
        branches = branches.order_by(
            "bank__name",
            "city",
            "address",
        )

        # ==========================================
        # 💣 SERIALIZE
        # ==========================================
        result = [serialize_branch(branch) for branch in branches]

        return Response(
            {
                "count": len(result),
                "results": result,
            }
        )


# ==================================================
# 🔥 BRANCH DETAIL
# ==================================================
class BankBranchDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, branch_id):

        try:

            branch = BankBranch.objects.select_related("bank").get(
                pk=branch_id,
                is_active=True,
            )

        except BankBranch.DoesNotExist:

            return Response(
                {"error": "Branch not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(serialize_branch(branch))
