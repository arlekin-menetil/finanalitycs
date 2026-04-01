from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import BankAccount
from .serializers import BankAccountSerializer
from transactions.services import get_account_balance
import uuid


class BankAccountViewSet(viewsets.ModelViewSet):
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Показываем только счета текущего пользователя
    def get_queryset(self):
        return BankAccount.objects.filter(owner=self.request.user)

    # При создании автоматически назначаем владельца и генерируем номер
    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user,
            account_number=str(uuid.uuid4()).replace("-", "")[:16]
        )

    # ============================
    # GET /api/accounts/{id}/balance/
    # ============================
    @action(detail=True, methods=["get"])
    def balance(self, request, pk=None):
        account = get_object_or_404(
            BankAccount,
            pk=pk,
            owner=request.user
        )

        balance = get_account_balance(account)

        return Response({
            "account_id": account.id,
            "account_number": account.account_number,
            "currency": account.currency,
            "balance": balance
        })