from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from decimal import Decimal

import re
import hashlib

# ==========================================
# 🔥 BANK ALIASES (CRITICAL)
# ==========================================
BANK_ALIASES = {
    "национальныи узбекистана": "nbu",
    "национальный узбекистана": "nbu",
    "национальный банк узбекистана": "nbu",
    "nbu": "nbu",
    "xalq banki": "xalq bank",
    "xalq i": "xalq bank",
    "mkbank": "mkbank",
    "mk": "mkbank",
    "apexbank": "apex bank",
    "apex": "apex bank",
    "mybank": "my bank",
    "my": "my bank",
}


# ==========================================
# 🔥 NORMALIZER
# ==========================================
def normalize_name(name):

    if not name:
        return ""

    name = str(name).lower()

    name = name.replace("й", "и")
    name = name.replace("ё", "е")

    name = re.sub(r"[\"'«»]", "", name)

    name = name.replace("банк", "bank")

    name = re.sub(r"[^a-zа-я0-9\s]", " ", name)

    name = re.sub(r"\s+", " ", name).strip()

    name = BANK_ALIASES.get(name, name)

    return name


# ==========================================
# 🔥 ADDRESS NORMALIZER
# ==========================================
def normalize_address(address):

    if not address:
        return ""

    address = str(address).lower()

    address = address.replace("й", "и")
    address = address.replace("ё", "е")

    address = re.sub(r"[^\w\s]", " ", address)

    address = re.sub(r"\s+", " ", address).strip()

    return address


# ==========================================
# 🔥 UNIQUE HASH ENGINE
# ==========================================
def generate_unique_key(*args):

    base = "|".join([str(a or "") for a in args])

    return hashlib.md5(base.encode("utf-8")).hexdigest()


# ==========================================
# 💣 LOAN TYPE DETECTOR
# ==========================================
def detect_loan_type(name: str, term_max=None, max_amount=None) -> str:

    name = (name or "").lower()

    if any(
        x in name
        for x in [
            "авто",
            "auto",
            "avto",
            "kia",
            "byd",
            "chevrolet",
            "hyundai",
            "changan",
            "haval",
            "jac",
            "toyota",
            "roodell",
            "adm",
            "onix",
            "tracker",
            "motors",
            "autocenter",
            "luxemotors",
            "damas",
            "labo",
            "jetour",
            "chery",
            "ducati",
        ]
    ):

        return "auto"

    if any(
        x in name
        for x in [
            "микро",
            "micro",
            "mikro",
            "qarz",
        ]
    ):

        return "micro"

    if any(
        x in name
        for x in [
            "образ",
            "student",
            "ta’lim",
            "ta'lim",
            "talim",
            "обуч",
        ]
    ):

        return "education"

    if any(
        x in name
        for x in [
            "овердрафт",
            "overdraft",
        ]
    ):

        return "overdraft"

    if any(
        x in name
        for x in [
            "green",
            "зелен",
            "yashil",
            "eco",
            "energy",
            "quyosh",
            "солнеч",
            "eko",
        ]
    ):

        return "green"

    if any(
        x in name
        for x in [
            "бизнес",
            "business",
            "startup",
            "start up",
            "tadbirkor",
            "biznes",
        ]
    ):

        return "business"

    if (
        any(
            x in name
            for x in [
                "ипот",
                "ipoteka",
                "жиль",
                "дом",
                "строит",
                "ремонт",
            ]
        )
        or (term_max and term_max >= 240)
        or (max_amount and max_amount >= 200_000_000)
    ):

        return "mortgage"

    return "loan"


# ==========================================
# 💣 BANK TYPES
# ==========================================
BANK_TYPES = (
    ("bank", "Bank"),
    ("fintech", "Fintech"),
    ("mfo", "Microfinance"),
)


# ==========================================
# 💣 BANK
# ==========================================
class Bank(models.Model):

    name = models.CharField(max_length=255)

    short_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    normalized_name = models.CharField(
        max_length=255,
        db_index=True,
    )

    unique_key = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        null=True,
        blank=True,
    )

    type = models.CharField(
        max_length=20,
        choices=BANK_TYPES,
        default="bank",
        db_index=True,
    )

    slug = models.SlugField(
        max_length=120,
        blank=True,
        null=True,
        db_index=True,
    )

    website = models.URLField(
        blank=True,
        null=True,
    )

    logo = models.URLField(
        blank=True,
        null=True,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    address = models.TextField(
        null=True,
        blank=True,
    )

    license_number = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    license_date = models.DateField(
        null=True,
        blank=True,
    )

    support_phone = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    telegram = models.URLField(
        null=True,
        blank=True,
    )

    instagram = models.URLField(
        null=True,
        blank=True,
    )

    facebook = models.URLField(
        null=True,
        blank=True,
    )

    source_url = models.URLField(
        null=True,
        blank=True,
    )

    external_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
    )

    last_parsed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    parser_version = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    is_featured = models.BooleanField(
        default=False,
        db_index=True,
    )

    priority_weight = models.FloatField(
        default=1.0,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "-is_featured",
            "-priority_weight",
            "name",
        ]

    def save(self, *args, **kwargs):

        # ==========================================
        # 💣 NORMALIZED NAME
        # ==========================================
        if self.name:

            self.normalized_name = normalize_name(self.name)

        # ==========================================
        # 💣 UNIQUE KEY
        # ==========================================
        if not self.unique_key:

            self.unique_key = generate_unique_key(
                self.name,
                self.website,
                "bank",
            )

        # ==========================================
        # 💣 SAFE SLUG
        # ==========================================
        if not self.slug:

            base_slug = slugify(self.short_name or self.name or "bank")[:80]

            # 💣 fallback если slugify дал пустоту
            if not base_slug:

                base_slug = hashlib.md5(str(self.name).encode()).hexdigest()[:12]

            slug = base_slug

            counter = 1

            while Bank.objects.filter(slug=slug).exclude(pk=self.pk).exists():

                slug = f"{base_slug}-{counter}"

                counter += 1

            self.slug = slug[:120]

        super().save(*args, **kwargs)

    def __str__(self):

        return self.short_name or self.name or "Unknown Bank"

    # ==========================================


# 💣 BANK BRANCH
# ==========================================
class BankBranch(models.Model):

    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name="branches",
        db_index=True,
    )

    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
    )

    city = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True,
    )

    address = models.TextField()

    normalized_address = models.TextField(
        null=True,
        blank=True,
        db_index=True,
    )

    phone = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    email = models.EmailField(
        null=True,
        blank=True,
    )

    working_hours = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    latitude = models.FloatField(
        null=True,
        blank=True,
        db_index=True,
    )

    longitude = models.FloatField(
        null=True,
        blank=True,
        db_index=True,
    )

    geocoded = models.BooleanField(
        default=False,
        db_index=True,
    )

    geocode_provider = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    source_url = models.URLField(
        null=True,
        blank=True,
    )

    external_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    last_parsed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "bank__name",
            "city",
            "address",
        ]

        unique_together = (
            "bank",
            "normalized_address",
        )

        indexes = [
            models.Index(fields=["city"]),
            models.Index(fields=["latitude", "longitude"]),
            models.Index(fields=["bank", "city"]),
            models.Index(fields=["is_active"]),
        ]

    def save(self, *args, **kwargs):

        if self.address:

            self.normalized_address = normalize_address(self.address)

        self.last_parsed_at = now()

        super().save(*args, **kwargs)

    def __str__(self):

        bank_name = self.bank.name if self.bank else "Unknown Bank"

        city = self.city or "Unknown City"

        return f"{bank_name} | " f"{city} | " f"{self.address[:80]}"


# ==========================================
# 💣 AGGREGATED PRODUCT
# ==========================================
class AggregatedProduct(models.Model):

    name = models.CharField(max_length=255)

    normalized_name = models.CharField(
        max_length=255,
        db_index=True,
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        null=True,
        blank=True,
    )

    product_type = models.CharField(
        max_length=20,
        db_index=True,
    )

    min_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    max_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    best_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    offers_count = models.IntegerField(default=0)

    is_online = models.BooleanField(
        default=False,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = ["best_rate"]

        unique_together = (
            "normalized_name",
            "product_type",
        )

    def save(self, *args, **kwargs):

        if self.name:

            self.normalized_name = normalize_name(self.name)

        if not self.slug:

            base_slug = slugify(self.name or "product")[:120]

            if not base_slug:

                base_slug = hashlib.md5(str(self.name).encode()).hexdigest()[:12]

            slug = base_slug

            counter = 1

            while (
                AggregatedProduct.objects.filter(slug=slug).exclude(pk=self.pk).exists()
            ):

                slug = f"{base_slug}-{counter}"

                counter += 1

            self.slug = slug[:255]

        super().save(*args, **kwargs)

    def __str__(self):

        return self.name or "Unnamed Product"


# ==========================================
# 💣 BANK PRODUCT
# ==========================================
class BankProduct(models.Model):

    PRODUCT_TYPES = (
        ("loan", "Loan"),
        ("deposit", "Deposit"),
        ("card", "Card"),
        ("micro", "Microloan"),
        ("auto", "Auto Loan"),
        ("mortgage", "Mortgage"),
        ("education", "Education"),
        ("overdraft", "Overdraft"),
        ("business", "Business Loan"),
        ("green", "Green Loan"),
    )

    # ==========================================
    # 💣 BANK RELATION
    # ==========================================
    bank = models.ForeignKey(
        Bank,
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        blank=True,
    )

    # 💣 RAW BANK NAME
    bank_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
    )

    aggregated_product = models.ForeignKey(
        AggregatedProduct,
        on_delete=models.CASCADE,
        related_name="offers",
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=255)

    normalized_name = models.CharField(
        max_length=255,
        db_index=True,
    )

    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
    )

    unique_key = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
    )

    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPES,
        default="loan",
        db_index=True,
    )

    loan_type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_index=True,
    )

    # ==========================================
    # 💣 DIGITAL / OPEN METHODS
    # ==========================================
    is_online = models.BooleanField(
        default=False,
        db_index=True,
    )

    real_online = models.BooleanField(
        null=True,
        blank=True,
        db_index=True,
    )

    has_branch = models.BooleanField(
        default=True,
        db_index=True,
    )

    open_methods = models.JSONField(
        default=list,
        blank=True,
    )

    # ==========================================
    # 💳 CARD DATA
    # ==========================================
    card_system = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_index=True,
    )

    card_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True,
    )

    currency = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        db_index=True,
    )

    issue_cost = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    service_cost = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    validity_period = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    documents_required = models.TextField(
        null=True,
        blank=True,
    )

    image_url = models.URLField(
        null=True,
        blank=True,
    )

    thumbnail_url = models.URLField(
        null=True,
        blank=True,
    )

    requirements = models.TextField(
        null=True,
        blank=True,
    )

    fee = models.TextField(
        null=True,
        blank=True,
    )

    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        db_index=True,
    )

    min_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        db_index=True,
    )

    max_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    has_rate = models.BooleanField(
        default=False,
        db_index=True,
    )

    max_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
    )

    term = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    term_min = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
    )

    term_max = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    raw_data = models.JSONField(
        default=dict,
        blank=True,
    )

    parser_metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    source_url = models.URLField(
        null=True,
        blank=True,
    )

    bank_url = models.URLField(
        null=True,
        blank=True,
    )

    updated_from_source = models.DateField(
        null=True,
        blank=True,
        db_index=True,
    )

    source_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_index=True,
    )

    source_hash = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        db_index=True,
    )

    duplicate_group = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        db_index=True,
    )

    is_partner = models.BooleanField(
        default=False,
        db_index=True,
    )

    score = models.FloatField(
        default=0,
        db_index=True,
    )

    search_vector = models.TextField(
        null=True,
        blank=True,
    )

    parse_success = models.BooleanField(
        default=True,
        db_index=True,
    )

    parse_error = models.TextField(
        null=True,
        blank=True,
    )

    is_virtual = models.BooleanField(
        default=False,
        db_index=True,
    )

    is_premium = models.BooleanField(
        default=False,
        db_index=True,
    )

    is_salary_card = models.BooleanField(
        default=False,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    last_parsed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "-score",
            "-real_online",
            "-has_rate",
            "interest_rate",
        ]

        indexes = [
            models.Index(fields=["product_type"]),
            models.Index(fields=["bank"]),
            models.Index(fields=["bank_name"]),
            models.Index(fields=["currency"]),
            models.Index(fields=["card_system"]),
            models.Index(fields=["interest_rate"]),
            models.Index(fields=["is_online"]),
            models.Index(fields=["updated_from_source"]),
        ]

    def save(self, *args, **kwargs):

        # ==========================================
        # 💣 NORMALIZED NAME
        # ==========================================
        if self.name:

            self.normalized_name = normalize_name(self.name)

        # ==========================================
        # 💣 SAFE SLUG
        # ==========================================
        if not self.slug:

            bank_part = str(self.bank.pk) if self.bank else (self.bank_name or "bank")

            base_slug = slugify(f"{self.name}-{bank_part}")[:220]

            if not base_slug:

                base_slug = hashlib.md5(str(self.name).encode()).hexdigest()[:16]

            self.slug = base_slug[:255]

        # ==========================================
        # 💣 UNIQUE KEY
        # ==========================================
        if not self.unique_key:

            self.unique_key = generate_unique_key(
                self.name,
                (self.bank.pk if self.bank else self.bank_name),
                self.source_url,
                "product",
            )

        # ==========================================
        # 💣 TERM PARSER
        # ==========================================
        if self.term:

            nums = [
                int(n)
                for n in re.findall(
                    r"\d+",
                    str(self.term),
                )
            ]

            if nums:

                self.term_min = min(nums)

                self.term_max = max(nums)

                if self.term_max and self.term_max > 600:

                    self.term_max = None

        # ==========================================
        # 💣 LOAN TYPE
        # ==========================================
        self.loan_type = detect_loan_type(
            self.name,
            self.term_max,
            self.max_amount,
        )

        if not self.product_type or self.product_type == "loan":

            self.product_type = self.loan_type

        # ==========================================
        # 💣 FLAGS
        # ==========================================
        self.has_rate = bool(self.interest_rate)

        methods = []

        if self.real_online or self.is_online:

            methods.append("online")

        if self.has_branch:

            methods.append("branch")

        self.open_methods = sorted(list(set(methods)))

        if self.bank_url and "ads.bank.uz" in (self.bank_url or ""):

            self.is_partner = True

        self.last_parsed_at = now()

        # ==========================================
        # 💣 SEARCH VECTOR
        # ==========================================
        search_parts = [
            self.name,
            self.description,
            self.card_system,
            self.currency,
            self.bank_name,
        ]

        self.search_vector = " ".join([str(x) for x in search_parts if x])

        super().save(*args, **kwargs)

    def __str__(self):

        bank_name = (
            self.bank.short_name if self.bank else (self.bank_name or "Без банка")
        )

        return f"{bank_name} — " f"{self.name or 'Unnamed Product'}"

# ==========================================
# ⭐ RECOMMENDATION RULE
# ==========================================

class RecommendationRule(models.Model):
    """
    Ручные правила рекомендаций банков.

    Используются Recommendation Engine поверх AI-скоринга.
    """

    bank = models.OneToOneField(
        Bank,
        on_delete=models.CASCADE,
        related_name="recommendation_rule",
    )

    enabled = models.BooleanField(
        default=True,
        db_index=True,
    )

    featured = models.BooleanField(
        default=False,
        db_index=True,
    )

    priority = models.PositiveIntegerField(
        default=0,
        help_text="Дополнительный приоритет банка",
    )

    # =====================================
    # Ограничения
    # =====================================

    min_score = models.PositiveIntegerField(
        default=0,
    )

    max_score = models.PositiveIntegerField(
        default=1000,
    )

    min_income = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    max_dti = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("100.00"),
    )

    # =====================================
    # Где показывать
    # =====================================

    show_dashboard = models.BooleanField(
        default=True,
    )

    show_recommendations = models.BooleanField(
        default=True,
    )

    show_landing = models.BooleanField(
        default=False,
    )

    # =====================================
    # Дополнительно
    # =====================================

    reason = models.CharField(
        max_length=255,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    valid_from = models.DateField(
        null=True,
        blank=True,
        db_index=True,
    )

    valid_to = models.DateField(
        null=True,
        blank=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "-featured",
            "-priority",
            "bank__name",
        ]

        verbose_name = "Recommendation Rule"

        verbose_name_plural = "Recommendation Rules"

    # =====================================
    # Helpers
    # =====================================

    def is_valid(self):
        """
        Проверяет, активно ли правило
        на текущую дату.
        """

        today = now().date()

        if not self.enabled:
            return False

        if self.valid_from and today < self.valid_from:
            return False

        if self.valid_to and today > self.valid_to:
            return False

        return True

    @property
    def is_expired(self):
        """
        Истек ли срок действия правила.
        """

        if not self.valid_to:
            return False

        return now().date() > self.valid_to

    @property
    def has_period(self):
        """
        Есть ли ограничение по периоду действия.
        """

        return bool(
            self.valid_from or self.valid_to
        )

    def __str__(self):

        bank_name = self.bank.short_name or self.bank.name

        return f"{bank_name} ({self.priority})"
# ==========================================
# ⭐ RECOMMENDATION CAMPAIGN
# ==========================================

class RecommendationCampaign(models.Model):
    """
    Маркетинговые кампании банков.

    Позволяют временно повышать рейтинг
    отдельных банков без изменения кода.
    """

    BADGES = (

        ("promo", "🔥 Акция"),

        ("top", "⭐ TOP"),

        ("cashback", "💰 Cashback"),

        ("mortgage", "🏠 Ипотека"),

        ("auto", "🚗 Автокредит"),

        ("business", "💼 Бизнес"),

        ("green", "🌿 Green"),

    )

    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name="campaigns",
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    badge = models.CharField(
        max_length=30,
        choices=BADGES,
        default="promo",
    )

    bonus_score = models.PositiveIntegerField(
        default=10,
    )

    priority = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    show_dashboard = models.BooleanField(
        default=True,
    )

    show_recommendations = models.BooleanField(
        default=True,
    )

    show_landing = models.BooleanField(
        default=False,
    )

    starts_at = models.DateField(
        null=True,
        blank=True,
    )

    ends_at = models.DateField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = (
            "-priority",
            "-bonus_score",
            "-created_at",
        )

        verbose_name = "Recommendation Campaign"

        verbose_name_plural = "Recommendation Campaigns"

    def is_valid(self):

        today = now().date()

        if not self.is_active:
            return False

        if self.starts_at and today < self.starts_at:
            return False

        if self.ends_at and today > self.ends_at:
            return False

        return True

    def __str__(self):

        return f"{self.bank.short_name} — {self.title}"
# ==========================================
# ⭐ RECOMMENDATION REASON
# ==========================================

class RecommendationReason(models.Model):
    """
    Причины, по которым банк рекомендуется пользователю.

    Используются Recommendation Engine для формирования
    понятного объяснения рекомендаций.
    """

    REASON_TYPES = (

        ("score", "Высокий скоринг"),

        ("income", "Доход соответствует"),

        ("dti", "Низкая долговая нагрузка"),

        ("employment", "Подтвержденная занятость"),

        ("history", "Хорошая кредитная история"),

        ("partner", "Партнер BankAnalytics"),

        ("featured", "Избранный банк"),

        ("campaign", "Маркетинговая акция"),

        ("online", "Онлайн оформление"),

        ("rate", "Выгодная процентная ставка"),

        ("limit", "Высокий кредитный лимит"),

        ("custom", "Пользовательская"),

    )

    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name="recommendation_reasons",
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    reason_type = models.CharField(
        max_length=30,
        choices=REASON_TYPES,
        default="custom",
        db_index=True,
    )

    bonus_score = models.PositiveIntegerField(
        default=0,
        help_text="Дополнительные баллы рекомендации",
    )

    enabled = models.BooleanField(
        default=True,
        db_index=True,
    )

    priority = models.PositiveIntegerField(
        default=0,
    )

    show_dashboard = models.BooleanField(
        default=True,
    )

    show_recommendations = models.BooleanField(
        default=True,
    )

    show_landing = models.BooleanField(
        default=False,
    )

    starts_at = models.DateField(
        null=True,
        blank=True,
        db_index=True,
    )

    ends_at = models.DateField(
        null=True,
        blank=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = (
            "-priority",
            "-bonus_score",
            "title",
        )

        indexes = [

            models.Index(
                fields=[
                    "bank",
                    "enabled",
                ]
            ),

            models.Index(
                fields=[
                    "reason_type",
                    "enabled",
                ]
            ),

        ]

        verbose_name = "Recommendation Reason"

        verbose_name_plural = "Recommendation Reasons"

    # =====================================
    # Helpers
    # =====================================

    def is_valid(self):
        """
        Проверяет, активно ли правило
        на текущую дату.
        """

        today = now().date()

        if not self.enabled:
            return False

        if self.starts_at and today < self.starts_at:
            return False

        if self.ends_at and today > self.ends_at:
            return False

        return True

    @property
    def is_expired(self):
        """
        Истекла ли причина рекомендации.
        """

        if not self.ends_at:
            return False

        return now().date() > self.ends_at

    @property
    def has_period(self):
        """
        Используется ли ограничение
        по периоду действия.
        """

        return bool(
            self.starts_at or self.ends_at
        )

    @property
    def display_title(self):
        """
        Заголовок для Dashboard/API.
        """

        return self.title.strip()

    def __str__(self):

        bank_name = self.bank.short_name or self.bank.name

        return f"{bank_name} — {self.title}"