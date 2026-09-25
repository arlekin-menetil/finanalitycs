from django.urls import path
from .views import CalendarEventsAPIView

urlpatterns = [
    path("", CalendarEventsAPIView.as_view()),
]