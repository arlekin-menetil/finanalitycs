from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import CreditReport
from .services import parse_credit_report


class UploadCreditReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response({"error": "No file provided"}, status=400)

        report = CreditReport.objects.create(
            user=request.user,
            uploaded_file=file
        )

        income, debt, score = parse_credit_report(report.uploaded_file.path)

        report.extracted_income = income
        report.extracted_debt = debt
        report.credit_score = score
        report.parsed = True
        report.save()

        return Response({
            "income": income,
            "debt": debt,
            "credit_score": score
        }, status=status.HTTP_201_CREATED)