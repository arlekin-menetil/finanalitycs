from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction

from .models import FinancialProfile, Income, Obligation
from .serializers import (
    FinancialProfileSerializer,
    IncomeSerializer,
    ObligationSerializer
)
from profiles.services.financial_calculator import recalculate_profile


# ==================================
# HELPER
# ==================================

def get_or_create_profile(user):
    profile, _ = FinancialProfile.objects.get_or_create(
        user=user
    )
    return profile


# ==================================
# GET /api/profile/
# ==================================

class FinancialProfileAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = get_or_create_profile(request.user)
        serializer = FinancialProfileSerializer(profile)
        return Response(serializer.data)


# ==================================
# 💣 PROFILE SETUP (ПОЛНЫЙ FIX)
# ==================================

class ProfileSetupAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):

        profile = get_or_create_profile(request.user)

        # ==================================
        # 💣 KYC ДАННЫЕ (из формы)
        # ==================================

        profile.full_name = request.data.get("full_name", profile.full_name)
        profile.birth_date = request.data.get("birth_date", profile.birth_date)
        profile.passport = request.data.get("passport", profile.passport)
        profile.job_type = request.data.get("job_type", profile.job_type)
        profile.experience = request.data.get("experience", profile.experience)

        # ==================================
        # 💣 ФИНАНСЫ
        # ==================================

        income = request.data.get("income")
        expenses = request.data.get("expenses")
        credit_score = request.data.get("credit_score")

        if income is not None:
            profile.income = income

        if expenses is not None:
            profile.expenses = expenses

        if credit_score is not None:
            profile.credit_score = credit_score

        # ==================================
        # 💣 ФИНАЛ
        # ==================================

        profile.is_profile_completed = True
        profile.save()

        # 💣 пересчёт скоринга
        recalculate_profile(profile)

        return Response({
            "message": "Profile completed",
            "is_profile_completed": True
        })


# ==================================
# Income ViewSet (FULL CRUD)
# ==================================

class IncomeViewSet(viewsets.ModelViewSet):

    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile = get_or_create_profile(self.request.user)
        return Income.objects.filter(
            profile=profile
        ).order_by("-created_at")

    @transaction.atomic
    def perform_create(self, serializer):
        profile = get_or_create_profile(self.request.user)

        serializer.save(
            profile=profile,
            created_by=self.request.user
        )

        recalculate_profile(profile)

    @transaction.atomic
    def perform_update(self, serializer):
        instance = serializer.save()
        recalculate_profile(instance.profile)

    @transaction.atomic
    def perform_destroy(self, instance):
        profile = instance.profile
        instance.delete()
        recalculate_profile(profile)


# ==================================
# Obligation ViewSet (FULL CRUD)
# ==================================

class ObligationViewSet(viewsets.ModelViewSet):

    serializer_class = ObligationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile = get_or_create_profile(self.request.user)
        return Obligation.objects.filter(
            profile=profile
        ).order_by("-created_at")

    @transaction.atomic
    def perform_create(self, serializer):
        profile = get_or_create_profile(self.request.user)

        serializer.save(
            profile=profile,
            created_by=self.request.user
        )

        recalculate_profile(profile)

    @transaction.atomic
    def perform_update(self, serializer):
        instance = serializer.save()
        recalculate_profile(instance.profile)

    @transaction.atomic
    def perform_destroy(self, instance):
        profile = instance.profile
        instance.delete()
        recalculate_profile(profile)