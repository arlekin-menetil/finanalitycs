from django.urls import path

# ==========================================
# 🔥 CORE VIEWS
# ==========================================
from .views import (
    BankProductsAPIView,
    BankProductDetailAPIView,  # 💣 ДОБАВИЛИ
    TopRecommendationsAPIView,
    MarketRatingAPIView,
    RecommendationClickAPIView,
    RecommendationApplyAPIView,
    RecommendationDecisionAPIView,
    MobileBanksAnalyticsAPIView
)

# ==========================================
# 💣 NEW API
# ==========================================
from .views_api import (
    BankListAPIView,
    RecommendationAPIView
)

# ==========================================
# 🏢 BRANCHES
# ==========================================
from .views_branches import (
    BankBranchesAPIView,
    BankBranchesMapAPIView
)

# ==========================================
# 📊 MONITORING
# ==========================================
from .views_monitoring import (
    MarketAlertsAPIView,
    DigitalRankingAPIView,
    InterestMonitorAPIView,
    MarketForecastAPIView,
    CompetitionMapAPIView
)

urlpatterns = [

    # ==================================================
    # 🏦 BANK LIST
    # ==================================================
    path("", BankListAPIView.as_view(), name="banks-list"),

    # ==================================================
    # 💣 PRODUCTS
    # ==================================================
    path("products/", BankProductsAPIView.as_view(), name="products-list"),

    # 💣 ВОТ ГЛАВНЫЙ ФИКС
    path(
        "products/<int:product_id>/",
        BankProductDetailAPIView.as_view(),
        name="product-detail"
    ),

    # ==================================================
    # 💣 RECOMMENDATIONS
    # ==================================================
    path("recommendations/", RecommendationAPIView.as_view(), name="recommendations"),

    # ==================================================
    # ⚠️ LEGACY
    # ==================================================
    path("top/", TopRecommendationsAPIView.as_view()),
    path("mobile-analytics/", MobileBanksAnalyticsAPIView.as_view()),
    path("rating/", MarketRatingAPIView.as_view()),

    # ==================================================
    # 📊 MONITORING
    # ==================================================
    path("monitoring/alerts/", MarketAlertsAPIView.as_view()),
    path("monitoring/digital-ranking/", DigitalRankingAPIView.as_view()),
    path("monitoring/interest-monitor/", InterestMonitorAPIView.as_view()),
    path("monitoring/forecast/", MarketForecastAPIView.as_view()),
    path("monitoring/competition-map/", CompetitionMapAPIView.as_view()),

    # ==================================================
    # 🧠 USER INTERACTIONS
    # ==================================================
    path("click/", RecommendationClickAPIView.as_view()),
    path("apply/", RecommendationApplyAPIView.as_view()),
    path("decision/", RecommendationDecisionAPIView.as_view()),

    # ==================================================
    # 🏢 BRANCHES
    # ==================================================
    path("<int:bank_id>/branches/", BankBranchesAPIView.as_view()),
    path("branches/map/", BankBranchesMapAPIView.as_view()),
]