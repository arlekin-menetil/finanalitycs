from django.urls import path
from .views import (
    SendCodeAPIView,
    VerifyCodeAPIView,
)

urlpatterns = [
    # 📱 SMS авторизация
    path("send-code/", SendCodeAPIView.as_view()),
    path("verify-code/", VerifyCodeAPIView.as_view()),
]