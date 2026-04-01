from django.db import models
from django.conf import settings
from decimal import Decimal
from django.core.exceptions import ValidationError


# ============================
# 🧠 Financial Profile (Core)
# ============================

class FinancialProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="financial_profile"
    )

    # =====================================
    # 💣 KYC
    # =====================================

    full_name = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    passport = models.CharField(max_length=20, blank=True)

    job_type = models.CharField(
        max_length=20,
        choices=[
            ("employee", "Employee"),
            ("self", "Self-employed"),
            ("business", "Business"),
        ],
        default="employee"
    )

    experience = models.PositiveIntegerField(default=0)

    # =====================================
    # 💣 ФИНАНСЫ
    # =====================================

    income = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    expenses = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    credit_score = models.IntegerField(default=0)

    # =====================================
    # 💼 АГРЕГАТЫ
    # =====================================

    monthly_income_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    monthly_obligations_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    net_balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    dti_ratio = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00")
    )

    # 💣 ФЛАГ
    is_profile_completed = models.BooleanField(default=False)

    # =====================================
    # SYSTEM
    # =====================================

    profile_version = models.PositiveIntegerField(default=1)
    calculated_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # =====================================
    # 🧠 LOGIC (ФИКС ЗДЕСЬ 💣)
    # =====================================

    def calculate_dti(self):
        try:
            income = Decimal(str(self.income or 0))
            expenses = Decimal(str(self.expenses or 0))

            if income == 0:
                return Decimal("0.00")

            return (expenses / income) * Decimal("100")

        except Exception as e:
            print("💥 DTI ERROR:", e)
            return Decimal("0.00")

    def check_profile_complete(self):
        return all([
            self.full_name,
            self.passport,
            self.income and self.income > 0
        ])

    def save(self, *args, **kwargs):
        # 💣 безопасный пересчет
        self.dti_ratio = self.calculate_dti()

        # 💣 авто-статус
        self.is_profile_completed = self.check_profile_complete()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"FinancialProfile of {self.user.phone_number}"


# ============================
# 💰 Income
# ============================

class Income(models.Model):
    profile = models.ForeignKey(
        FinancialProfile,
        on_delete=models.CASCADE,
        related_name="incomes"
    )

    source = models.CharField(max_length=255)

    amount = models.DecimalField(max_digits=14, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_incomes"
    )

    def __str__(self):
        return f"{self.source} — {self.amount}"


# ============================
# 💳 Obligation
# ============================

class Obligation(models.Model):
    profile = models.ForeignKey(
        FinancialProfile,
        on_delete=models.CASCADE,
        related_name="obligations"
    )

    description = models.CharField(max_length=255)

    monthly_payment = models.DecimalField(max_digits=14, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_obligations"
    )

    def __str__(self):
        return f"{self.description} — {self.monthly_payment}"


# ============================
# 🏢 Employment
# ============================

class Employment(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employment"
    )

    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True)

    salary = models.DecimalField(max_digits=14, decimal_places=2)

    work_experience_months = models.PositiveIntegerField()

    is_company_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} — {self.salary}"


# ============================
# 🪪 Identity
# ============================

class Identity(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="identity"
    )

    passport_series = models.CharField(max_length=2)
    passport_number = models.CharField(max_length=7)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.passport_series.isalpha():
            raise ValidationError("Серия паспорта должна быть буквами")

        if not self.passport_number.isdigit():
            raise ValidationError("Номер паспорта должен быть цифрами")

    def __str__(self):
        return f"{self.passport_series}{self.passport_number}"


# ============================
# 📊 History
# ============================

class FinancialProfileHistory(models.Model):
    profile = models.ForeignKey(
        FinancialProfile,
        on_delete=models.CASCADE,
        related_name="history"
    )

    monthly_income_total = models.DecimalField(max_digits=14, decimal_places=2)
    monthly_obligations_total = models.DecimalField(max_digits=14, decimal_places=2)
    net_balance = models.DecimalField(max_digits=14, decimal_places=2)
    dti_ratio = models.DecimalField(max_digits=5, decimal_places=2)

    version = models.PositiveIntegerField()
    calculated_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile v{self.version} snapshot"