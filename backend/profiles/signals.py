from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from .models import FinancialProfile, Income, Obligation
from scoring.services.scoring_engine import generate_credit_score


# -------------------------------------------------
# 1. Автоматическое создание профиля при создании пользователя
# -------------------------------------------------

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_financial_profile(sender, instance, created, **kwargs):
    if created:
        FinancialProfile.objects.create(user=instance)


# -------------------------------------------------
# 2. Универсальная функция пересчёта скоринга
# -------------------------------------------------

def recalculate_score(profile: FinancialProfile):
    if not profile:
        return

    try:
        generate_credit_score(profile)
    except Exception:
        # можно позже добавить логирование
        pass


# -------------------------------------------------
# 3. Income → пересчёт
# -------------------------------------------------

@receiver(post_save, sender=Income)
def income_saved(sender, instance, **kwargs):
    recalculate_score(instance.profile)


@receiver(post_delete, sender=Income)
def income_deleted(sender, instance, **kwargs):
    recalculate_score(instance.profile)


# -------------------------------------------------
# 4. Obligation → пересчёт
# -------------------------------------------------

@receiver(post_save, sender=Obligation)
def obligation_saved(sender, instance, **kwargs):
    recalculate_score(instance.profile)


@receiver(post_delete, sender=Obligation)
def obligation_deleted(sender, instance, **kwargs):
    recalculate_score(instance.profile)


# -------------------------------------------------
# 5. Изменение профиля → пересчёт
# -------------------------------------------------

@receiver(post_save, sender=FinancialProfile)
def profile_updated(sender, instance, created, **kwargs):
    # чтобы не зациклить создание профиля
    if not created:
        recalculate_score(instance)