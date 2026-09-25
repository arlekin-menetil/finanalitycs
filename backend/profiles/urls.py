from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    FinancialProfileAPIView,
    ProfileSetupAPIView,
    EmploymentUploadAPIView,
    IncomeViewSet,
    ObligationViewSet,
)

from .dashboard import ProfileDashboardAPIView


# ==========================================
# DRF ROUTER
# ==========================================

router = DefaultRouter()

router.register(
    r"incomes",
    IncomeViewSet,
    basename="income",
)

router.register(
    r"obligations",
    ObligationViewSet,
    basename="obligation",
)


# ==========================================
# URL PATTERNS
# ==========================================

urlpatterns = [

    # ==========================================
    # 👤 PROFILE
    # GET /api/profile/
    # ==========================================
    path(
        "",
        FinancialProfileAPIView.as_view(),
        name="financial-profile",
    ),

    # ==========================================
    # 🚀 PROFILE DASHBOARD
    # GET /api/profile/dashboard/
    # ==========================================
    path(
        "dashboard/",
        ProfileDashboardAPIView.as_view(),
        name="profile-dashboard",
    ),

    # ==========================================
    # 📝 PROFILE SETUP
    # POST /api/profile/setup/
    # ==========================================
    path(
        "setup/",
        ProfileSetupAPIView.as_view(),
        name="profile-setup",
    ),

    # ==========================================
    # 💼 EMPLOYMENT DOCUMENT
    # POST /api/profile/upload-employment/
    # ==========================================
    path(
        "upload-employment/",
        EmploymentUploadAPIView.as_view(),
        name="employment-upload",
    ),

    # ==========================================
    # 💰 INCOMES / OBLIGATIONS
    # ==========================================
    path(
        "",
        include(router.urls),
    ),

]