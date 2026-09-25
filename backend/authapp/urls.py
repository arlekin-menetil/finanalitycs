from django.urls import path
from .views import send_code, verify_code

urlpatterns = [
    path("send-code/", send_code),
    path("verify-code/", verify_code),
]