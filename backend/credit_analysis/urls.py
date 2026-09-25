from django.urls import path

from .views import (
    UploadCreditReportAPIView,
    CreditReportAPIView,
    CreditContractsAPIView,
)

app_name = "credit_analysis"

urlpatterns = [

    # ==========================================
    # Upload credit report
    # ==========================================

    path(
        "upload/",
        UploadCreditReportAPIView.as_view(),
        name="upload-credit-report",
    ),

    # ==========================================
    # Last parsed credit report
    # ==========================================

    path(
        "report/",
        CreditReportAPIView.as_view(),
        name="credit-report",
    ),

    # ==========================================
    # Credit contracts
    # ==========================================

    path(
        "contracts/",
        CreditContractsAPIView.as_view(),
        name="credit-contracts",
    ),

]