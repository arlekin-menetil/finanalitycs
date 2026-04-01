from django.db import models
from django.conf import settings
from decimal import Decimal


class CreditScore(models.Model):
    RISK_CHOICES = [
        ("LOW", "Low Risk"),
        ("MEDIUM", "Medium Risk"),
        ("HIGH", "High Risk"),
        ("REJECT", "Reject"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="credit_scores"
    )

    profile_version = models.PositiveIntegerField()

    score = models.PositiveIntegerField()  # 0–1000
    risk_category = models.CharField(max_length=10, choices=RISK_CHOICES)
    approval_probability = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} — {self.score}"