from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)

from rest_framework import status

from rest_framework.generics import (
    ListAPIView,
)

from profiles.models import (
    FinancialProfile,
)

from scoring.models import (
    CreditScore,
)

from scoring.serializers import (
    CreditScoreSerializer,
)

from credit_analysis.models import (
    CreditReport,
)

from credit_analysis.serializers import (
    CreditReportShortSerializer,
)

from scoring.services.scoring_engine import (
    generate_credit_score,
)

from banks.serializers import (
    BankProductSerializer,
)

from banks.recommendation_engine import (
    get_recommendations_for_user,
    get_safe_products_for_user,
    get_premium_products_for_user,
)

# ==========================================
# 💣 HELPERS
# ==========================================


def build_profile_summary(
    profile,
) -> dict:

    return {
        "full_name": profile.full_name,
        "monthly_income_total": float(profile.monthly_income_total or 0),
        "monthly_obligations_total": float(profile.monthly_obligations_total or 0),
        "net_balance": float(profile.net_balance or 0),
        "dti_ratio": float(profile.dti_ratio or 0),
        "job_type": profile.job_type,
        "work_experience_months": profile.work_experience_months,
        "employment_verified": profile.employment_verified,
        "profile_completed": profile.is_profile_completed,
    }


# ==========================================
# 💣 CALCULATE SCORE
# ==========================================


class CalculateScoreAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(
        self,
        request,
    ):

        profile = FinancialProfile.objects.filter(user=request.user).first()

        if not profile:

            return Response(
                {
                    "detail": "Financial profile not found",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            result = generate_credit_score(profile)

            serializer = CreditScoreSerializer(result)

            return Response(
                {
                    "success": True,
                    "profile": build_profile_summary(profile),
                    "scoring": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception:

            import traceback

            traceback.print_exc()

            return Response(
                {
                    "success": False,
                    "detail": "Scoring calculation failed",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ==========================================
# 💣 LATEST SCORE
# ==========================================


class LatestScoreAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(
        self,
        request,
    ):

        latest_score = (
            CreditScore.objects.filter(user=request.user)
            .order_by("-created_at")
            .first()
        )

        if not latest_score:

            return Response(
                {
                    "detail": "No scoring history found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CreditScoreSerializer(latest_score)

        return Response(
            {
                "success": True,
                "latest_score": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================
# 💣 SCORING HISTORY
# ==========================================


class ScoringHistoryAPIView(ListAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = CreditScoreSerializer

    def get_queryset(self):

        return CreditScore.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )


# ==========================================
# 💣 RECOMMENDATIONS
# ==========================================


class RecommendationsAPIView(APIView):

    permission_classes = [AllowAny]

    def get(
        self,
        request,
    ):

        try:

            recommendations = get_recommendations_for_user(
                request.user,
                limit=10,
            )

            recommendations = BankProductSerializer(
                recommendations,
                many=True,
            ).data

            return Response(
                {
                    "success": True,
                    "count": len(recommendations),
                    "recommendations": recommendations,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            print(
                "💥 RECOMMENDATIONS ERROR:",
                e,
            )

            return Response(
                {
                    "success": False,
                    "detail": "Failed to load recommendations",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        # ==========================================


# 💣 SAFE PRODUCTS
# ==========================================


class SafeProductsAPIView(APIView):

    permission_classes = [AllowAny]

    def get(
        self,
        request,
    ):

        try:

            safe_products = get_safe_products_for_user(
                request.user,
                limit=10,
            )

            safe_products = BankProductSerializer(
                safe_products,
                many=True,
            ).data

            return Response(
                {
                    "success": True,
                    "count": len(safe_products),
                    "products": safe_products,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            print(
                "💥 SAFE PRODUCTS ERROR:",
                e,
            )

            return Response(
                {
                    "success": False,
                    "detail": "Failed to load safe products",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ==========================================
# 💣 PREMIUM PRODUCTS
# ==========================================


class PremiumProductsAPIView(APIView):

    permission_classes = [AllowAny]

    def get(
        self,
        request,
    ):

        try:

            premium_products = get_premium_products_for_user(
                request.user,
                limit=10,
            )

            premium_products = BankProductSerializer(
                premium_products,
                many=True,
            ).data

            return Response(
                {
                    "success": True,
                    "count": len(premium_products),
                    "products": premium_products,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            print(
                "💥 PREMIUM PRODUCTS ERROR:",
                e,
            )

            return Response(
                {
                    "success": False,
                    "detail": "Failed to load premium products",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ==========================================
# 💣 FULL FINANCIAL DASHBOARD
# ==========================================


class FinancialDashboardAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(
        self,
        request,
    ):

        profile = FinancialProfile.objects.filter(
            user=request.user,
        ).first()

        if not profile:

            return Response(
                {
                    "success": False,
                    "detail": "Financial profile not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:

            # ======================================
            # AI CREDIT SCORE
            # ======================================

            scoring = (
                CreditScore.objects.filter(
                    user=request.user,
                )
                .order_by("-created_at")
                .first()
            )

            if scoring is None:

                scoring = generate_credit_score(
                    profile,
                )

            elif scoring.profile_version != profile.profile_version:

                scoring = generate_credit_score(
                    profile,
                )

            scoring_serializer = CreditScoreSerializer(
                scoring,
            )

            # ======================================
            # OFFICIAL CREDIT REPORT
            # ======================================

            credit_report = (
                CreditReport.objects.filter(
                    user=request.user,
                    parsed=True,
                )
                .order_by("-created_at")
                .first()
            )

            credit_report_serializer = (
                CreditReportShortSerializer(
                    credit_report,
                )
                if credit_report
                else None
            )

            # ======================================
            # PRODUCTS
            # ======================================

            recommendations = get_recommendations_for_user(
                request.user,
                limit=5,
            )

            safe_products = get_safe_products_for_user(
                request.user,
                limit=5,
            )

            premium_products = get_premium_products_for_user(
                request.user,
                limit=5,
            )
            # ======================================
            # SERIALIZE PRODUCTS
            # ======================================

            recommendations = BankProductSerializer(
                recommendations,
                many=True,
            ).data

            safe_products = BankProductSerializer(
                safe_products,
                many=True,
            ).data

            premium_products = BankProductSerializer(
                premium_products,
                many=True,
            ).data

            # ======================================
            # RESPONSE
            # ======================================

            return Response(
                {
                    "success": True,
                    "profile": build_profile_summary(
                        profile,
                    ),
                    # ----------------------------------
                    # AI Credit Score
                    # ----------------------------------
                    "scoring": scoring_serializer.data,
                    # ----------------------------------
                    # Official Credit Bureau Score
                    # ----------------------------------
                    "credit_report": (
                        credit_report_serializer.data
                        if credit_report_serializer
                        else None
                    ),
                    # ----------------------------------
                    # Recommendations
                    # ----------------------------------
                    "recommendations": recommendations,
                    "safe_products": safe_products,
                    "premium_products": premium_products,
                },
                status=status.HTTP_200_OK,
            )

        except Exception:

            import traceback

            traceback.print_exc()

            return Response(
                {
                    "success": False,
                    "detail": "Failed to build dashboard",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
