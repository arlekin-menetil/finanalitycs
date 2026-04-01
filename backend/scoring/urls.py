from django.urls import path
from .views import (
    CalculateScoreAPIView,
    LatestScoreAPIView,
    ScoringHistoryAPIView,
)

urlpatterns = [
    path("calculate/", CalculateScoreAPIView.as_view(), name="calculate-score"),
    path("latest/", LatestScoreAPIView.as_view(), name="latest-score"),
    path("history/", ScoringHistoryAPIView.as_view(), name="scoring-history"),
]