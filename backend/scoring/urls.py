from django.urls import path

from .views import (
    CalculateScoreAPIView,
    LatestScoreAPIView,
    ScoringHistoryAPIView,
    RecommendationsAPIView,
    SafeProductsAPIView,
    PremiumProductsAPIView,
    FinancialDashboardAPIView,
)

urlpatterns = [
    # ==========================================
    # 💣 SCORING
    # ==========================================
    path(
        "calculate/",
        CalculateScoreAPIView.as_view(),
        name="calculate-score",
    ),
    path(
        "latest/",
        LatestScoreAPIView.as_view(),
        name="latest-score",
    ),
    path(
        "history/",
        ScoringHistoryAPIView.as_view(),
        name="scoring-history",
    ),
    # ==========================================
    # 💣 RECOMMENDATIONS
    # ==========================================
    path(
        "recommendations/",
        RecommendationsAPIView.as_view(),
        name="recommendations",
    ),
    path(
        "safe-products/",
        SafeProductsAPIView.as_view(),
        name="safe-products",
    ),
    path(
        "premium-products/",
        PremiumProductsAPIView.as_view(),
        name="premium-products",
    ),
    # ==========================================
    # 💣 DASHBOARD
    # ==========================================
    path(
        "dashboard/",
        FinancialDashboardAPIView.as_view(),
        name="financial-dashboard",
    ),
]
