from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from django.db.models import Q

from .serializers import TransferSerializer, TransactionSerializer
from .services import transfer_funds, InsufficientFunds, InvalidAccount
from .models import Transaction


# ==========================================
# POST /api/transfer/
# ==========================================

class TransferAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            tx = transfer_funds(
                serializer.validated_data["from_account"],
                serializer.validated_data["to_account"],
                serializer.validated_data["amount"],
            )

            return Response(
                {
                    "transaction_id": tx.id,
                    "status": tx.status,
                    "amount": tx.amount,
                },
                status=status.HTTP_201_CREATED,
            )

        except InsufficientFunds:
            return Response(
                {"error": "Insufficient funds"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except InvalidAccount:
            return Response(
                {"error": "Invalid account"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception:
            return Response(
                {"error": "Transfer failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ==========================================
# GET /api/transactions/
# ==========================================

class TransactionListAPIView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_accounts = self.request.user.accounts.all()

        return Transaction.objects.filter(
            Q(from_account__in=user_accounts) |
            Q(to_account__in=user_accounts)
        ).order_by("-created_at")