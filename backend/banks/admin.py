from django.contrib import admin
from .models import (
    Bank,
    BankProduct,
    RecommendationSnapshot,
    RecommendationInteraction
)


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = (
        "short_name",
        "name",
        "priority_weight",
        "is_featured",
        "is_active",
    )
    search_fields = ("name", "short_name")
    list_filter = ("is_active", "is_featured")


@admin.register(BankProduct)
class BankProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "bank",
        "interest_rate",
        "min_score",
        "max_dti",
        "min_income",
        "is_active",
    )
    list_filter = ("bank", "is_active")
    search_fields = ("name",)


@admin.register(RecommendationSnapshot)
class RecommendationSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "ranking_version",
        "user_score",
        "approval_probability",
        "risk_category",
        "created_at",
    )
    list_filter = ("ranking_version", "risk_category")


@admin.register(RecommendationInteraction)
class RecommendationInteractionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "product",
        "clicked",
        "applied",
        "approved",
        "ranking_version",
        "created_at",
    )
    list_filter = ("clicked", "applied", "approved")