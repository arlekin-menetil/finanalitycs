from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from accounts.views import BankAccountViewSet
from transactions.views import (
    TransferAPIView,
    TransactionListAPIView,
)
from users.views import MeAPIView

from banks.views import (
    BankProductsAPIView,
    AggregatedProductsAPIView,
    BestBankProductsAPIView,
    BankProductDetailAPIView,
    ProductsBySourceAPIView,
)

# ==========================================
# ROUTER
# ==========================================

router = DefaultRouter()

router.register(
    r"accounts",
    BankAccountViewSet,
    basename="accounts",
)

# ==========================================
# HEALTH CHECK
# ==========================================

def health_check(request):

    return JsonResponse({

        "status": "ok",
        "service": "bankanalytics",
        "version": "2.0",

    })


# ==========================================
# URLS
# ==========================================

urlpatterns = [

    # ==========================================
    # SYSTEM
    # ==========================================

    path(
        "",
        health_check,
    ),

    path(
        "admin/",
        admin.site.urls,
    ),

    # ==========================================
    # AUTH
    # ==========================================

    path(
        "api/auth/",
        include("users.urls"),
    ),

    path(
        "api/auth/me/",
        MeAPIView.as_view(),
    ),

    # ==========================================
    # JWT
    # ==========================================

    path(
        "api/token/",
        TokenObtainPairView.as_view(),
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
    ),

    # ==========================================
    # ACCOUNTS
    # ==========================================

    path(
        "api/accounts/",
        include(router.urls),
    ),

    # ==========================================
    # TRANSACTIONS
    # ==========================================

    path(
        "api/transfer/",
        TransferAPIView.as_view(),
    ),

    path(
        "api/transactions/",
        TransactionListAPIView.as_view(),
    ),

    # ==========================================
    # PROFILE
    # ==========================================

    path(
        "api/profile/",
        include("profiles.urls"),
    ),

    # ==========================================
    # SCORING
    # ==========================================

    path(
        "api/scoring/",
        include("scoring.urls"),
    ),

    # ==========================================
    # BANKS
    # ==========================================

    path(
        "api/banks/",
        include("banks.urls"),
    ),

    # ==========================================
    # REPORTS
    # ==========================================

    path(
        "api/reports/",
        include("reports.urls"),
    ),

    # ==========================================
    # CREDIT ANALYSIS
    # ==========================================

    path(
        "api/credit-analysis/",
        include("credit_analysis.urls"),
    ),

    # ==========================================
    # PRODUCTS
    # ==========================================

    path(
        "api/products/",
        BankProductsAPIView.as_view(),
    ),

    path(
        "api/products/<int:product_id>/",
        BankProductDetailAPIView.as_view(),
    ),

    path(
        "api/products/by-source/",
        ProductsBySourceAPIView.as_view(),
    ),

    path(
        "api/aggregated/",
        AggregatedProductsAPIView.as_view(),
    ),

    path(
        "api/best-products/",
        BestBankProductsAPIView.as_view(),
    ),

    # ==========================================
    # FINANCE CALENDAR
    # ==========================================

    path(
        "api/calendar/",
        include("finance_calendar.urls"),
    ),

]

# ==========================================
# MEDIA
# ==========================================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )