from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .parser import parse_credit_report


class CreditReportUploadAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    parser_classes = [
        MultiPartParser
    ]

    def post(
        self,
        request,
    ):

        report = request.FILES.get(
            "report"
        )

        if not report:

            return Response(

                {
                    "detail":
                    "Файл не выбран"
                },

                status=400

            )

        data = parse_credit_report(
            report
        )

        return Response(data)