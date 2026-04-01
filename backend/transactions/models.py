from django.db import models
from accounts.models import BankAccount
from django.utils import timezone
from decimal import Decimal
import uuid


class Transaction(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("flagged", "Flagged"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="outgoing")
    to_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="incoming")
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.amount}"


class LedgerEntry(models.Model):
    ENTRY_TYPE = [
        ("debit", "Debit"),
        ("credit", "Credit"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="ledger_entries")
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="entries")
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPE)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.entry_type} {self.amount}"