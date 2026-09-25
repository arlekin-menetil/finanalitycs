from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from profiles.models import FinancialProfile
from scoring.models import CreditScore
from banks.services.matching_engine import get_top_recommendations


class ProfileDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        # ==========================================
        # PROFILE
        # ==========================================

        profile = FinancialProfile.objects.filter(
            user=user
        ).first()

        # ==========================================
        # CREDIT SCORE
        # ==========================================

        score = CreditScore.objects.filter(
            user=user
        ).order_by("-created_at").first()

        # ==========================================
        # RECOMMENDATIONS
        # ==========================================

        recommendations = get_top_recommendations(
            user,
            limit=5,
        )

        # ==========================================
        # RESPONSE
        # ==========================================

        return Response({

            # ======================================
            # USER
            # ======================================

            "user": {

                "id": user.id,

                "phone": getattr(
                    user,
                    "phone_number",
                    "",
                ),

            },

            # ======================================
            # PROFILE
            # ======================================

            "profile": {

                "exists": profile is not None,

                # ==================================
                # PERSONAL
                # ==================================

                "full_name": getattr(
                    profile,
                    "full_name",
                    "",
                ) if profile else "",

                "passport": getattr(
                    profile,
                    "passport",
                    "",
                ) if profile else "",

                "birth_date": getattr(
                    profile,
                    "birth_date",
                    None,
                ) if profile else None,

                "job_type": getattr(
                    profile,
                    "job_type",
                    "",
                ) if profile else "",

                "is_profile_completed": getattr(
                    profile,
                    "is_profile_completed",
                    False,
                ) if profile else False,

                # ==================================
                # EMPLOYMENT
                # ==================================

                "company_name": getattr(
                    profile,
                    "company_name",
                    "",
                ) if profile else "",

                "company_inn": getattr(
                    profile,
                    "company_inn",
                    "",
                ) if profile else "",

                "position": getattr(
                    profile,
                    "position",
                    "",
                ) if profile else "",

                "department": getattr(
                    profile,
                    "department",
                    "",
                ) if profile else "",

                "employment_start": getattr(
                    profile,
                    "employment_start",
                    None,
                ) if profile else None,

                "employment_end": getattr(
                    profile,
                    "employment_end",
                    None,
                ) if profile else None,

                "employment_verified": getattr(
                    profile,
                    "employment_verified",
                    False,
                ) if profile else False,

                "employment_pinfl": getattr(
                    profile,
                    "employment_pinfl",
                    "",
                ) if profile else "",

                "is_current_employee": getattr(
                    profile,
                    "is_current_employee",
                    False,
                ) if profile else False,

                "work_experience_months": getattr(
                    profile,
                    "work_experience_months",
                    0,
                ) if profile else 0,

                "employment_document": bool(
                    getattr(
                        profile,
                        "employment_document",
                        None,
                    )
                ) if profile else False,

                # ==================================
                # FINANCE
                # ==================================

                "income": getattr(
                    profile,
                    "monthly_income_total",
                    0,
                ) if profile else 0,

                "expenses": getattr(
                    profile,
                    "monthly_obligations_total",
                    0,
                ) if profile else 0,

                "net_balance": getattr(
                    profile,
                    "net_balance",
                    0,
                ) if profile else 0,

                "dti": getattr(
                    profile,
                    "dti_ratio",
                    0,
                ) if profile else 0,

            },

            # ======================================
            # SCORE
            # ======================================

            "score": {

                "exists": score is not None,

                "credit_score": getattr(
                    score,
                    "score",
                    0,
                ) if score else 0,

                "approval_probability": getattr(
                    score,
                    "approval_probability",
                    0,
                ) if score else 0,

                "risk_category": getattr(
                    score,
                    "risk_category",
                    "",
                ) if score else "",

            },

            # ======================================
            # RECOMMENDATIONS
            # ======================================

            "recommendations": [

                {

                    "id": product.id,

                    "bank": product.bank.name,

                    "product": product.name,

                    "ranking_score": getattr(
                        product,
                        "ranking_score",
                        0,
                    ),

                    "approval_probability": getattr(
                        product,
                        "approval_probability",
                        0,
                    ),

                    "loan_limit": getattr(
                        product,
                        "loan_limit_hint",
                        0,
                    ),

                    "interest_rate": getattr(
                        product,
                        "interest_rate",
                        0,
                    ),

                }

                for product in recommendations

            ],

            # ======================================
            # CREDIT HISTORY
            # ======================================

            "credit_history": {

                "uploaded": score is not None,

                "provider": "Infokredit",

            },

            # ======================================
            # EMPLOYMENT STATUS
            # ======================================

            "employment": {

                "uploaded": bool(
                    getattr(
                        profile,
                        "employment_document",
                        None,
                    )
                ) if profile else False,

                "verified": getattr(
                    profile,
                    "employment_verified",
                    False,
                ) if profile else False,

            },

        })