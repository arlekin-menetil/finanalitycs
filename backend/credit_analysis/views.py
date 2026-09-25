from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import (
    CreditReport,
    CreditContract,
)

from .serializers import (
    CreditReportSerializer,
    CreditContractSerializer,
)

from .services import parse_credit_report


# ==========================================================
# UPLOAD CREDIT REPORT
# ==========================================================

class UploadCreditReportAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        uploaded_file = request.FILES.get("file")

        if not uploaded_file:

            return Response(

                {

                    "success": False,

                    "error": "No file provided."

                },

                status=status.HTTP_400_BAD_REQUEST

            )

        report = CreditReport.objects.create(

            user=request.user,

            uploaded_file=uploaded_file,

        )

        try:

            result = parse_credit_report(

                report.uploaded_file.path

            )

            profile = result.get("profile", {})

            report_data = result.get("report", {})

            contracts = result.get("contracts", [])

            # ==========================================
            # CREDIT REPORT
            # ==========================================

            report.full_name = profile.get(

                "full_name",

                ""

            )

            report.passport = profile.get(

                "passport",

                ""

            )

            report.phone = profile.get(

                "phone",

                ""

            )

            report.credit_score = report_data.get(

                "score",

                0

            )

            report.risk_class = report_data.get(

                "risk",

                ""

            )

            report.score_version = report_data.get(

                "score_version",

                ""

            )

            report.extracted_income = report_data.get(

                "income",

                0

            )

            report.extracted_debt = report_data.get(

                "total_debt",

                0

            )

            report.overdue_debt = report_data.get(

                "overdue_debt",

                0

            )

            report.contracts_count = len(contracts)

            report.parsed = True

            report.save()

            # ==========================================
            # CONTRACTS
            # ==========================================

            report.contracts.all().delete()

            for item in contracts:

                CreditContract.objects.create(

                    report=report,

                    bank_name=item.get(

                        "bank_name",

                        ""

                    ),

                    contract_number=item.get(

                        "contract_number",

                        ""

                    ),

                    product_name=item.get(

                        "product_name",

                        ""

                    ),

                    currency=item.get(

                        "currency",

                        "UZS"

                    ),

                    issued_amount=item.get(

                        "issued_amount",

                        0

                    ) or 0,

                    current_debt=item.get(

                        "current_debt",

                        0

                    ) or 0,

                    overdue_debt=item.get(

                        "overdue_debt",

                        0

                    ) or 0,

                    monthly_payment=item.get(

                        "monthly_payment",

                        0

                    ) or 0,

                    interest_rate=item.get(

                        "interest_rate",

                        0

                    ) or 0,

                    issued_date=item.get(

                        "issued_date"

                    ),

                    closed_date=item.get(

                        "closed_date"

                    ),

                    status=item.get(

                        "status",

                        "UNKNOWN"

                    ),

                )

            serializer = CreditReportSerializer(report)

            return Response(

                {

                    "success": True,

                    "message": "Credit report parsed successfully.",

                    "report": serializer.data,

                },

                status=status.HTTP_201_CREATED

            )

        except Exception as e:

            report.delete()

            return Response(

                {

                    "success": False,

                    "error": str(e)

                },

                status=status.HTTP_400_BAD_REQUEST

            )


# ==========================================================
# LAST CREDIT REPORT
# ==========================================================

class CreditReportAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        report = (

            CreditReport.objects

            .filter(user=request.user)

            .order_by("-created_at")

            .first()

        )

        if not report:

            return Response(

                {

                    "success": False,

                    "error": "Credit report not found."

                },

                status=status.HTTP_404_NOT_FOUND

            )

        serializer = CreditReportSerializer(report)

        return Response(

            serializer.data,

            status=status.HTTP_200_OK

        )


# ==========================================================
# CREDIT CONTRACTS
# ==========================================================

class CreditContractsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        report = (

            CreditReport.objects

            .filter(user=request.user)

            .order_by("-created_at")

            .first()

        )

        if not report:

            return Response(

                [],

                status=status.HTTP_200_OK

            )

        serializer = CreditContractSerializer(

            report.contracts.all(),

            many=True

        )

        return Response(

            serializer.data,

            status=status.HTTP_200_OK

        )