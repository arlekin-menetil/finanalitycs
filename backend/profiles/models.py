from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


# ==========================================================
# 🧠 FINANCIAL PROFILE
# ==========================================================

class FinancialProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="financial_profile",
    )

    # ======================================================
    # KYC
    # ======================================================

    full_name = models.CharField(
        max_length=255,
        blank=True,
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
    )

    passport = models.CharField(
        max_length=20,
        blank=True,
    )

    job_type = models.CharField(
        max_length=20,
        choices=[
            ("employee", "Employee"),
            ("self", "Self-employed"),
            ("business", "Business"),
        ],
        default="employee",
    )

    # ======================================================
    # EMPLOYMENT
    # ======================================================

    employment_document = models.FileField(
        upload_to="employment/",
        null=True,
        blank=True,
    )

    company_name = models.CharField(
        max_length=255,
        blank=True,
    )

    company_inn = models.CharField(
        max_length=20,
        blank=True,
    )

    position = models.CharField(
        max_length=255,
        blank=True,
    )

    department = models.CharField(
        max_length=255,
        blank=True,
    )

    employment_start = models.DateField(
        null=True,
        blank=True,
    )

    employment_end = models.DateField(
        null=True,
        blank=True,
    )

    is_current_employee = models.BooleanField(
        default=False,
    )

    work_experience_months = models.PositiveIntegerField(
        default=0,
    )

    employment_verified = models.BooleanField(
        default=False,
    )

    employment_pinfl = models.CharField(
        max_length=20,
        blank=True,
    )

    # ======================================================
    # FINANCES
    # ======================================================

    income = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    expenses = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    credit_score = models.IntegerField(
        default=0,
    )

    # ======================================================
    # AGGREGATES
    # ======================================================

    monthly_income_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    monthly_obligations_total = models.DecimalField(
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

    is_profile_completed = models.BooleanField(
        default=False,
    )

    # ======================================================
    # SYSTEM
    # ======================================================

    profile_version = models.PositiveIntegerField(
        default=1,
    )

    calculated_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )
        # ======================================================
    # BUSINESS LOGIC
    # ======================================================

    def recalc_aggregates(self):

        self.monthly_income_total = self.income or Decimal("0.00")

        self.monthly_obligations_total = self.expenses or Decimal("0.00")

        self.net_balance = (
            self.monthly_income_total
            - self.monthly_obligations_total
        )

    def calculate_dti(self):

        income = Decimal(self.monthly_income_total or 0)

        obligations = Decimal(
            self.monthly_obligations_total or 0
        )

        if income <= 0:

            return Decimal("0.00")

        return (
            obligations
            / income
            * Decimal("100")
        ).quantize(
            Decimal("0.01")
        )

    def check_profile_complete(self):

        return all(

            [

                bool(self.full_name),

                bool(self.passport),

                self.income > 0,

            ]

        )

    # ======================================================
    # SAVE
    # ======================================================

    def save(self, *args, **kwargs):

        if self.pk:

            previous = FinancialProfile.objects.filter(
                pk=self.pk
            ).first()

            if previous:

                tracked_fields = [

                    "income",

                    "expenses",

                    "job_type",

                    "company_name",

                    "company_inn",

                    "position",

                    "department",

                    "employment_verified",

                    "work_experience_months",

                    "is_current_employee",

                ]

                changed = any(

                    getattr(previous, field)
                    != getattr(self, field)

                    for field in tracked_fields

                )

                if changed:

                    self.profile_version += 1

        self.recalc_aggregates()

        self.dti_ratio = self.calculate_dti()

        self.is_profile_completed = (
            self.check_profile_complete()
        )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.full_name or self.user}"
        )


# ==========================================================
# 💰 INCOME
# ==========================================================

class Income(models.Model):

    profile = models.ForeignKey(
        FinancialProfile,
        on_delete=models.CASCADE,
        related_name="incomes",
    )

    source = models.CharField(
        max_length=255,
    )

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_incomes",
    )

    def __str__(self):

        return (
            f"{self.source} — {self.amount}"
        )


# ==========================================================
# 💳 OBLIGATION
# ==========================================================

class Obligation(models.Model):

    profile = models.ForeignKey(
        FinancialProfile,
        on_delete=models.CASCADE,
        related_name="obligations",
    )

    description = models.CharField(
        max_length=255,
    )

    monthly_payment = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_obligations",
    )

    def __str__(self):

        return (
            f"{self.description} — {self.monthly_payment}"
        )


# ==========================================================
# 🏢 EMPLOYMENT
# ==========================================================

class Employment(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employment",
    )

    company_name = models.CharField(
        max_length=255,
    )

    position = models.CharField(
        max_length=255,
        blank=True,
    )

    salary = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    work_experience_months = models.PositiveIntegerField()

    is_company_verified = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):

        return (
            f"{self.company_name} — {self.salary}"
        )


# ==========================================================
# 🪪 IDENTITY
# ==========================================================

class Identity(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="identity",
    )

    passport_series = models.CharField(
        max_length=2,
    )

    passport_number = models.CharField(
        max_length=7,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def clean(self):

        if not self.passport_series.isalpha():

            raise ValidationError(
                "Серия паспорта должна быть буквами"
            )

        if not self.passport_number.isdigit():

            raise ValidationError(
                "Номер паспорта должен быть цифрами"
            )

    def __str__(self):

        return (
            f"{self.passport_series}{self.passport_number}"
        )


# ==========================================================
# 📊 PROFILE HISTORY
# ==========================================================

class FinancialProfileHistory(models.Model):

    profile = models.ForeignKey(
        FinancialProfile,
        on_delete=models.CASCADE,
        related_name="history",
    )

    monthly_income_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    monthly_obligations_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    net_balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    dti_ratio = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    version = models.PositiveIntegerField()

    calculated_at = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):

        return (
            f"Profile v{self.version}"
        )