from django.db import models
from django.conf import settings


# ==========================================================
# CREDIT REPORT
# ==========================================================

class CreditReport(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="credit_reports",
    )

    uploaded_file = models.FileField(
        upload_to="credit_reports/",
    )

    # ======================================================
    # PERSONAL
    # ======================================================

    full_name = models.CharField(
        max_length=255,
        blank=True,
    )

    passport = models.CharField(
        max_length=30,
        blank=True,
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    # ======================================================
    # SCORING
    # ======================================================

    credit_score = models.PositiveIntegerField(
        default=0,
    )

    risk_class = models.CharField(
        max_length=20,
        blank=True,
    )

    score_version = models.CharField(
        max_length=20,
        blank=True,
    )

    # ======================================================
    # FINANCIAL
    # ======================================================

    extracted_income = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
    )

    extracted_debt = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
    )

    overdue_debt = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
    )

    contracts_count = models.PositiveIntegerField(
        default=0,
    )

    parsed = models.BooleanField(
        default=False,
    )

    # ======================================================
    # TIMESTAMPS
    # ======================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "Credit report"

        verbose_name_plural = "Credit reports"

    def __str__(self):

        return f"{self.full_name or self.user} ({self.credit_score})"

    @property
    def has_income(self):

        return self.extracted_income > 0

    @property
    def has_overdue(self):

        return self.overdue_debt > 0


# ==========================================================
# CREDIT CONTRACT
# ==========================================================

class CreditContract(models.Model):

    STATUS_CHOICES = [

        ("ACTIVE", "Active"),

        ("CLOSED", "Closed"),

        ("OVERDUE", "Overdue"),

        ("UNKNOWN", "Unknown"),

    ]

    report = models.ForeignKey(
        CreditReport,
        on_delete=models.CASCADE,
        related_name="contracts",
    )

    bank_name = models.CharField(
        max_length=255,
    )

    contract_number = models.CharField(
        max_length=255,
        blank=True,
    )

    product_name = models.CharField(
        max_length=255,
        blank=True,
    )

    currency = models.CharField(
        max_length=20,
        default="UZS",
    )

    issued_amount = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
    )

    current_debt = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
    )

    overdue_debt = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
    )

    monthly_payment = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
    )

    interest_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    issued_date = models.DateField(
        null=True,
        blank=True,
    )

    closed_date = models.DateField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="UNKNOWN",
    )

    class Meta:

        ordering = [

            "-issued_date",

            "bank_name",

        ]

        verbose_name = "Credit contract"

        verbose_name_plural = "Credit contracts"

    def __str__(self):

        return f"{self.bank_name} - {self.current_debt}"