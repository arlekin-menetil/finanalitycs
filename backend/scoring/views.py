from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import ListAPIView

from profiles.models import FinancialProfile
from scoring.services.scoring_engine import generate_credit_score
from scoring.models import CreditScore
from scoring.serializers import CreditScoreSerializer


# ==============================
# CALCULATE SCORE
# ==============================

class CalculateScoreAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile = FinancialProfile.objects.filter(
            user=request.user
        ).first()

        if not profile:
            return Response(
                {"detail": "Financial profile not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = generate_credit_score(profile)

        return Response(result, status=status.HTTP_200_OK)


# ==============================
# LATEST SCORE
# ==============================

class LatestScoreAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        latest_score = (
            CreditScore.objects
            .filter(user=request.user)
            .order_by("-created_at")
            .first()
        )

        if not latest_score:
            return Response(
                {"detail": "No scoring history found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CreditScoreSerializer(latest_score)

        return Response(serializer.data, status=status.HTTP_200_OK)


# ==============================
# SCORING HISTORY
# ==============================

class ScoringHistoryAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreditScoreSerializer

    def get_queryset(self):
        return (
            CreditScore.objects
            .filter(user=self.request.user)
            .order_by("-created_at")
        )