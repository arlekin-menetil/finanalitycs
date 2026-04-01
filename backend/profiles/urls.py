from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    FinancialProfileAPIView,
    IncomeViewSet,
    ObligationViewSet,
    ProfileSetupAPIView,
)

# =====================================
# Router
# =====================================

router = DefaultRouter()

router.register(
    r"incomes",
    IncomeViewSet,
    basename="incomes"
)

router.register(
    r"obligations",
    ObligationViewSet,
    basename="obligations"
)


# =====================================
# URL patterns
# =====================================

urlpatterns = [

    # ===============================
    # 👤 PROFILE (GET)
    # ===============================
    path(
        "",
        FinancialProfileAPIView.as_view(),
        name="financial-profile"
    ),

    # ===============================
    # 💣 PROFILE SETUP (POST)
    # ===============================
    path(
        "setup/",
        ProfileSetupAPIView.as_view(),
        name="profile-setup"
    ),

    # ===============================
    # 💰 INCOMES
    # ===============================
    path(
        "incomes/",
        include((router.urls, "incomes"))
    ),

    # ===============================
    # 💳 OBLIGATIONS
    # ===============================
    path(
        "obligations/",
        include((router.urls, "obligations"))
    ),

]