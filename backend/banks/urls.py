from django.urls import path

# ==========================================
# 💣 CORE VIEWS
# ==========================================
from .views import (
    BankProductsAPIView,
    BankProductDetailAPIView,
    TopRecommendationsAPIView,
    MarketRatingAPIView,
    MobileBanksAnalyticsAPIView,
    BestBankProductsAPIView,
)

# ==========================================
# 💣 NEW API
# ==========================================
from .views_api import (
    BankListAPIView,
    RecommendationAPIView,
    TopBanksAPIView,
)

# ==========================================
# 💣 AGGREGATED
# ==========================================
from .views_aggregated import (
    AggregatedProductsAPIView,
    AggregatedProductDetailAPIView,
)

# ==========================================
# 📊 MONITORING
# ==========================================
from .views_monitoring import (
    MarketAlertsAPIView,
    DigitalRankingAPIView,
    InterestMonitorAPIView,
    MarketForecastAPIView,
    CompetitionMapAPIView,
)

# ==========================================
# 🗺 BRANCHES
# ==========================================
from .views_branches import (
    BankBranchesAPIView,
    BankBranchesMapAPIView,
    BankBranchDetailAPIView,
)

# ==========================================
# 💱 CURRENCY
# ==========================================
from .views_currency import (
    CurrencyRatesView,
)

from .views_currency_history import (
    CurrencyHistoryView,
)

# ==========================================
# 📊 PUBLIC STATS
# ==========================================
from .views_public import (
    PublicStatsAPIView,
)


app_name = "banks"


urlpatterns = [

    # ==================================================
    # 🏦 BANKS
    # ==================================================
    path(
        "",
        BankListAPIView.as_view(),
        name="banks-list",
    ),

    # ==================================================
    # 🗺 ALL BRANCHES MAP
    # ==================================================
    path(
        "branches/",
        BankBranchesMapAPIView.as_view(),
        name="branches-map",
    ),

    # ==================================================
    # 🏦 BANK BRANCHES
    # ==================================================
    path(
        "<int:bank_id>/branches/",
        BankBranchesAPIView.as_view(),
        name="bank-branches",
    ),

    # ==================================================
    # 🏦 BRANCH DETAIL
    # ==================================================
    path(
        "branches/<int:branch_id>/",
        BankBranchDetailAPIView.as_view(),
        name="branch-detail",
    ),

    # ==================================================
    # 💣 PRODUCTS
    # ==================================================
    path(
        "products/",
        BankProductsAPIView.as_view(),
        name="products-list",
    ),

    # ==================================================
    # 📊 PUBLIC STATS
    # ==================================================
    path(
        "public-stats/",
        PublicStatsAPIView.as_view(),
        name="public-stats",
    ),

    # ==================================================
    # 💣 PRODUCT DETAIL
    # ==================================================
    path(
        "products/<int:pk>/",
        BankProductDetailAPIView.as_view(),
        name="product-detail",
    ),

    # ==================================================
    # 💣 BEST PRODUCTS
    # ==================================================
    path(
        "best-products/",
        BestBankProductsAPIView.as_view(),
        name="best-products",
    ),

    # ==================================================
    # 💣 AGGREGATED PRODUCTS
    # ==================================================
    path(
        "products/aggregated/",
        AggregatedProductsAPIView.as_view(),
        name="aggregated-products",
    ),

    # ==================================================
    # 💣 AGGREGATED DETAIL
    # ==================================================
    path(
        "products/aggregated/<slug:slug>/",
        AggregatedProductDetailAPIView.as_view(),
        name="aggregated-detail",
    ),

    # ==================================================
    # 💣 RECOMMENDATIONS
    # ==================================================
    path(
        "recommendations/",
        RecommendationAPIView.as_view(),
        name="recommendations",
    ),

    # ==================================================
    # 💣 TOP BANKS
    # ==================================================
    path(
        "top-banks/",
        TopBanksAPIView.as_view(),
        name="top-banks",
    ),

    # ==================================================
    # 💱 CURRENT RATES
    # ==================================================
    path(
        "currency-rates/",
        CurrencyRatesView.as_view(),
        name="currency-rates",
    ),

    # ==================================================
    # 💱 CURRENCY HISTORY
    # ==================================================
    path(
        "currency-history/",
        CurrencyHistoryView.as_view(),
        name="currency-history",
    ),

    # ==================================================
    # ⚠️ LEGACY API
    # ==================================================
    path(
        "top/",
        TopRecommendationsAPIView.as_view(),
        name="legacy-top",
    ),

    path(
        "mobile-analytics/",
        MobileBanksAnalyticsAPIView.as_view(),
        name="mobile-analytics",
    ),

    path(
        "rating/",
        MarketRatingAPIView.as_view(),
        name="market-rating",
    ),

    # ==================================================
    # 📊 MONITORING
    # ==================================================
    path(
        "monitoring/alerts/",
        MarketAlertsAPIView.as_view(),
        name="monitoring-alerts",
    ),

    path(
        "monitoring/digital-ranking/",
        DigitalRankingAPIView.as_view(),
        name="digital-ranking",
    ),

    path(
        "monitoring/interest-monitor/",
        InterestMonitorAPIView.as_view(),
        name="interest-monitor",
    ),

    path(
        "monitoring/forecast/",
        MarketForecastAPIView.as_view(),
        name="market-forecast",
    ),

    path(
        "monitoring/competition-map/",
        CompetitionMapAPIView.as_view(),
        name="competition-map",
    ),

]