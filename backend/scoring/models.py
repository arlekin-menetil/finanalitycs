from decimal import Decimal

from django.db import models
from django.conf import settings


# ==========================================================
# CREDIT SCORE
# ==========================================================

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

        related_name="credit_scores",

    )

    profile_version = models.PositiveIntegerField(

        default=1,

    )

    # ======================================================
    # RESULT
    # ======================================================

    score = models.PositiveIntegerField(

        default=300,

    )

    risk_category = models.CharField(

        max_length=10,

        choices=RISK_CHOICES,

        default="HIGH",

    )

    approval_probability = models.DecimalField(

        max_digits=5,

        decimal_places=2,

        default=Decimal("0.00"),

    )

    recommended_limit = models.DecimalField(

        max_digits=14,

        decimal_places=2,

        default=Decimal("0.00"),

    )

    # ======================================================
    # SNAPSHOT
    # ======================================================

    monthly_income = models.DecimalField(

        max_digits=14,

        decimal_places=2,

        default=Decimal("0.00"),

    )

    monthly_obligations = models.DecimalField(

        max_digits=14,

        decimal_places=2,

        default=Decimal("0.00"),

    )

    net_balance = models.DecimalField(

        max_digits=14,

        decimal_places=2,

        default=Decimal("0.00"),

    )

    dti_ratio = models.DecimalField(

        max_digits=5,

        decimal_places=2,

        default=Decimal("0.00"),

    )

    # ======================================================
    # DETAILS
    # ======================================================

    income_score = models.PositiveIntegerField(

        default=0,

    )

    dti_score = models.PositiveIntegerField(

        default=0,

    )

    employment_score = models.PositiveIntegerField(

        default=0,

    )

    history_score = models.PositiveIntegerField(

        default=0,

    )

    profile_score = models.PositiveIntegerField(

        default=0,

    )

    # ======================================================
    # SYSTEM
    # ======================================================

    created_at = models.DateTimeField(

        auto_now_add=True,

    )

    class Meta:

        ordering = [

            "-created_at",

        ]

        indexes = [

            models.Index(

                fields=[

                    "user",

                    "-created_at",

                ]

            ),

            models.Index(

                fields=[

                    "score",

                ]

            ),

        ]

    def __str__(self):

        return (

            f"{self.user} | "

            f"{self.score} | "

            f"{self.risk_category}"

        )