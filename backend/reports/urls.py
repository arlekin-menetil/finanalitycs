from django.urls import path

from .views import (
    CreditReportUploadAPIView,
)

urlpatterns = [

    path(
        "upload/",
        CreditReportUploadAPIView.as_view(),
        name="credit-report-upload",
    ),

]