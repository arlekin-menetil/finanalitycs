from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from banks.services.matching_engine import get_top_recommendations
from banks.services.market_rating_engine import get_market_rating
from banks.services.mobile_apps_service import get_mobile_banks_data

from banks.models import (
    RecommendationSnapshot,
    RecommendationInteraction,
    BankProduct
)

from banks.serializers import BankProductSerializer


# =====================================================
# 🔥 PRODUCTS LIST
# =====================================================

class BankProductsAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        products = BankProduct.objects.filter(is_active=True)

        serializer = BankProductSerializer(products, many=True)

        return Response({
            "total": products.count(),
            "products": serializer.data
        })


# =====================================================
# 💣 PRODUCT DETAIL (🔥 НОВОЕ — ФИКС 404)
# =====================================================

class BankProductDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, product_id):
        try:
            product = BankProduct.objects.get(id=product_id, is_active=True)
        except BankProduct.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BankProductSerializer(product)

        return Response(serializer.data)


# =====================================================
# 💣 PERSONAL RECOMMENDATIONS
# =====================================================

class RecommendationsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        limit_param = request.query_params.get("limit")

        if limit_param == "all":
            limit = None
        else:
            try:
                limit = int(limit_param) if limit_param else 5
            except:
                limit = 5

        products = get_top_recommendations(user, limit)

        # fallback
        if not products:

            qs = BankProduct.objects.filter(is_active=True)

            ranked = []

            for product in qs:
                rate = float(product.interest_rate or 0)
                base_score = 100 - rate

                product.ranking_score = round(base_score, 2)
                product.approval_probability = 0.5

                ranked.append(product)

            ranked.sort(key=lambda x: x.ranking_score, reverse=True)

            products = ranked[:limit] if limit else ranked

        snapshot = RecommendationSnapshot.objects.create(
            user=user,
            ranking_version="v2"
        )

        result = []

        for product in products:

            bank = product.bank

            result.append({
                "product_id": product.id,
                "bank_id": bank.id,
                "bank_name": bank.short_name,
                "product_name": product.name,
                "interest_rate": float(product.interest_rate or 0),
                "website": bank.website,
                "ranking_score": getattr(product, "ranking_score", 0),
                "approval_probability": getattr(product, "approval_probability", None),
            })

        return Response({
            "snapshot_id": snapshot.id,
            "total": len(result),
            "recommendations": result
        })


# =====================================================
# TOP RECOMMENDATIONS
# =====================================================

class TopRecommendationsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:

            products = get_top_recommendations(request.user, limit=None)

            if not products:
                products = BankProduct.objects.filter(is_active=True)

            serializer = BankProductSerializer(products, many=True)

            return Response(serializer.data)

        except Exception as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =====================================================
# MOBILE ANALYTICS
# =====================================================

class MobileBanksAnalyticsAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        try:
            data = get_mobile_banks_data()

            return Response({
                "total_banks": len(data),
                "banks": data
            })

        except Exception as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =====================================================
# MARKET RATING
# =====================================================

class MarketRatingAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        rating = get_market_rating()

        return Response({
            "total_banks": len(rating),
            "rating": rating
        })


# =====================================================
# CLICK
# =====================================================

class RecommendationClickAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            product_id = request.data.get("product_id")
            snapshot_id = request.data.get("snapshot_id")

            product = BankProduct.objects.get(id=product_id)
            snapshot = RecommendationSnapshot.objects.get(id=snapshot_id)

            interaction = RecommendationInteraction.objects.create(
                user=request.user,
                product=product,
                snapshot=snapshot,
                clicked=True
            )

            return Response({
                "status": "click recorded",
                "interaction_id": interaction.id
            })

        except Exception as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =====================================================
# APPLY
# =====================================================

class RecommendationApplyAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        interaction_id = request.data.get("interaction_id")

        try:

            interaction = RecommendationInteraction.objects.get(
                id=interaction_id,
                user=request.user
            )

            interaction.applied = True
            interaction.save()

            return Response({"status": "application recorded"})

        except RecommendationInteraction.DoesNotExist:

            return Response(
                {"error": "Interaction not found"},
                status=status.HTTP_404_NOT_FOUND
            )


# =====================================================
# DECISION
# =====================================================

class RecommendationDecisionAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        interaction_id = request.data.get("interaction_id")
        approved = request.data.get("approved")

        try:

            interaction = RecommendationInteraction.objects.get(
                id=interaction_id,
                user=request.user
            )

            interaction.approved = bool(approved)
            interaction.save()

            return Response({"status": "decision recorded"})

        except RecommendationInteraction.DoesNotExist:

            return Response(
                {"error": "Interaction not found"},
                status=status.HTTP_404_NOT_FOUND
            )