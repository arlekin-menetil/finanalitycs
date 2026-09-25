from django.contrib import admin

from .models import (
    Bank,
    BankProduct,
    RecommendationRule,
)


# ==========================================
# 🏦 BANK
# ==========================================

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "short_name",
        "name",
        "type",
        "priority_weight",
        "is_featured",
        "is_active",
        "updated_at",
    )

    search_fields = (
        "name",
        "short_name",
        "normalized_name",
    )

    list_filter = (
        "type",
        "is_active",
        "is_featured",
    )

    ordering = (
        "-is_featured",
        "-priority_weight",
        "name",
    )

    readonly_fields = (
        "normalized_name",
        "unique_key",
        "slug",
        "created_at",
        "updated_at",
    )


# ==========================================
# 💳 BANK PRODUCT
# ==========================================

@admin.register(BankProduct)
class BankProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "bank",
        "product_type",
        "loan_type",
        "interest_rate",
        "max_amount",
        "is_partner",
        "is_online",
        "real_online",
        "is_active",
    )

    list_filter = (
        "product_type",
        "loan_type",
        "bank",
        "currency",
        "is_partner",
        "is_online",
        "real_online",
        "is_active",
    )

    search_fields = (
        "name",
        "bank__name",
        "bank_name",
    )

    ordering = (
        "-score",
        "-interest_rate",
    )

    list_select_related = (
        "bank",
    )

    readonly_fields = (
        "unique_key",
        "normalized_name",
        "slug",
        "loan_type",
        "search_vector",
        "last_parsed_at",
        "created_at",
        "updated_at",
    )


# ==========================================
# ⭐ RECOMMENDATION RULE
# ==========================================

@admin.register(RecommendationRule)
class RecommendationRuleAdmin(admin.ModelAdmin):

    list_display = (
        "bank",
        "enabled",
        "featured",
        "priority",
        "min_score",
        "max_score",
        "min_income",
        "max_dti",
        "show_dashboard",
        "show_recommendations",
    )

    list_filter = (
        "enabled",
        "featured",
        "show_dashboard",
        "show_recommendations",
        "show_landing",
    )

    search_fields = (
        "bank__name",
        "reason",
    )

    ordering = (
        "-featured",
        "-priority",
    )

    autocomplete_fields = (
        "bank",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "Банк",
            {
                "fields": (
                    "bank",
                    "enabled",
                    "featured",
                    "priority",
                )
            },
        ),

        (
            "Ограничения",
            {
                "fields": (
                    "min_score",
                    "max_score",
                    "min_income",
                    "max_dti",
                )
            },
        ),

        (
            "Где отображать",
            {
                "fields": (
                    "show_dashboard",
                    "show_recommendations",
                    "show_landing",
                )
            },
        ),

        (
            "Описание",
            {
                "fields": (
                    "reason",
                    "notes",
                )
            },
        ),

        (
            "Срок действия",
            {
                "fields": (
                    "valid_from",
                    "valid_to",
                )
            },
        ),

        (
            "Система",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),

    )