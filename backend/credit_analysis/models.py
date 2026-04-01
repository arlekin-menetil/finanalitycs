from django.db import models
from django.conf import settings


class CreditReport(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="credit_reports"
    )

    uploaded_file = models.FileField(upload_to="credit_reports/")
    extracted_income = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    extracted_debt = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    credit_score = models.IntegerField(null=True, blank=True)

    parsed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)