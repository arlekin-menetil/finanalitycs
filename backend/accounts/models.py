from django.db import models
from django.conf import settings
import uuid


class BankAccount(models.Model):
    CURRENCY_CHOICES = [
        ("UZS", "Uzbek Sum"),
        ("USD", "US Dollar"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accounts")
    account_number = models.CharField(max_length=24, unique=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_number}"