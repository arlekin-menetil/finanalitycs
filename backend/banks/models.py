from django.db import models
from django.conf import settings
from django.utils.text import slugify


# ==========================================
# Bank
# ==========================================

class Bank(models.Model):

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=100)

    # 💣 УБРАЛИ unique на старте (важно!)
    slug = models.SlugField(max_length=120, blank=True, null=True, db_index=True)

    website = models.URLField(blank=True, null=True)
    logo = models.URLField(blank=True, null=True)

    is_featured = models.BooleanField(default=False, db_index=True)

    priority_weight = models.FloatField(default=1.0, db_index=True)

    is_active = models.BooleanField(default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "-priority_weight", "name"]
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["priority_weight"]),
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):
        # 💣 Генерация slug с уникальностью
        if not self.slug:
            base_slug = slugify(self.short_name or self.name or "bank")

            slug = base_slug
            counter = 1

            while Bank.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.short_name


# ==========================================
# Bank Branch
# ==========================================

class BankBranch(models.Model):

    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name="branches"
    )

    name = models.CharField(max_length=255)

    city = models.CharField(max_length=100, default="Tashkent")
    address = models.CharField(max_length=500)

    phone = models.CharField(max_length=50, blank=True, null=True)

    working_hours = models.CharField(
        max_length=100,
        default="09:00 - 18:00"
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["bank", "name"]
        indexes = [
            models.Index(fields=["bank"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.bank.short_name} — {self.name}"


# ==========================================
# Bank Product
# ==========================================

class BankProduct(models.Model):

    PRODUCT_TYPES = (
        ("loan", "Loan"),
        ("credit_card", "Credit Card"),
        ("deposit", "Deposit"),
        ("mortgage", "Mortgage"),
    )

    CURRENCIES = (
        ("UZS", "UZS"),
        ("USD", "USD"),
    )

    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=255)

    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPES,
        default="loan",
        db_index=True
    )

    currency = models.CharField(
        max_length=10,
        choices=CURRENCIES,
        default="UZS"
    )

    min_score = models.PositiveIntegerField(null=True, blank=True, db_index=True)

    max_dti = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    min_income = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True
    )

    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        db_index=True
    )

    max_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True
    )

    term = models.CharField(max_length=100, null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    source_url = models.URLField(null=True, blank=True)

    is_featured = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "interest_rate"]
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["min_score"]),
            models.Index(fields=["interest_rate"]),
            models.Index(fields=["product_type"]),
        ]

    def __str__(self):
        return f"{self.bank.short_name} — {self.name}"


# ==========================================
# Recommendation Snapshot
# ==========================================

class RecommendationSnapshot(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recommendation_snapshots"
    )

    ranking_version = models.CharField(max_length=20, db_index=True)

    user_score = models.IntegerField()

    approval_probability = models.DecimalField(max_digits=6, decimal_places=4)

    dti_ratio = models.DecimalField(max_digits=6, decimal_places=4)

    monthly_income = models.DecimalField(max_digits=14, decimal_places=2)

    risk_category = models.CharField(max_length=20)

    min_market_rate = models.DecimalField(max_digits=5, decimal_places=2)
    max_market_rate = models.DecimalField(max_digits=5, decimal_places=2)

    feature_vector = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["ranking_version"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Snapshot v{self.ranking_version} — User {self.user_id}"


# ==========================================
# Recommendation Interaction
# ==========================================

class RecommendationInteraction(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recommendation_interactions"
    )

    product = models.ForeignKey(
        BankProduct,
        on_delete=models.CASCADE,
        related_name="interactions"
    )

    snapshot = models.ForeignKey(
        RecommendationSnapshot,
        on_delete=models.CASCADE,
        related_name="interactions"
    )

    clicked = models.BooleanField(default=False)
    applied = models.BooleanField(default=False)

    approved = models.BooleanField(null=True, blank=True)

    ranking_version = models.CharField(max_length=20, db_index=True)

    ranking_score = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["product"]),
            models.Index(fields=["ranking_version"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.user_id} → {self.product.name} ({self.ranking_version})"