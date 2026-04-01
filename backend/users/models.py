from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from datetime import date, timedelta
import random

from .managers import UserManager


# =========================
# 🧠 ВАЛИДАЦИЯ 18+
# =========================
def validate_age(value):
    today = date.today()
    age = today.year - value.year

    if (today.month, today.day) < (value.month, value.day):
        age -= 1

    if age < 18:
        raise ValidationError("Пользователю должно быть 18+")


# =========================
# 💣 USER MODEL
# =========================
class User(AbstractBaseUser, PermissionsMixin):
    # 📱 ОСНОВА
    phone_number = models.CharField(max_length=15, unique=True)

    # 👤 ЛИЧНЫЕ ДАННЫЕ (KYC START)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    birth_date = models.DateField(
        null=True,
        blank=True,
        validators=[validate_age]
    )

    # 🔐 СТАТУСЫ
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)  # 💣 прошёл ли KYC

    # 🧠 РОЛИ
    ROLE_CHOICES = (
        ("user", "User"),
        ("analyst", "Analyst"),
        ("admin", "Admin"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="user"
    )

    # 📊 META
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 🔑 AUTH
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone_number

    # =========================
    # 🧠 ВОЗРАСТ
    # =========================
    @property
    def age(self):
        if not self.birth_date:
            return None

        today = date.today()
        age = today.year - self.birth_date.year

        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1

        return age


# =========================
# 💣 SMS CODE MODEL
# =========================
class SMSCode(models.Model):
    phone = models.CharField(max_length=15, db_index=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["phone", "code"]),
        ]

    def __str__(self):
        return f"{self.phone} - {self.code}"

    # =========================
    # 🧠 ПРОВЕРКА КОДА
    # =========================
    def is_valid(self):
        return (
            not self.is_used and
            timezone.now() <= self.created_at + timedelta(minutes=5)
        )

    # =========================
    # 🔢 ГЕНЕРАЦИЯ КОДА
    # =========================
    @staticmethod
    def generate_code():
        return str(random.randint(100000, 999999))