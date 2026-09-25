import requests

from rest_framework.response import Response
from rest_framework.views import APIView


class CurrencyRatesView(APIView):

    def get(self, request):

        try:

            response = requests.get(
                "https://cbu.uz/uz/arkhiv-kursov-valyut/json/",
                timeout=10
            )

            data = response.json()

            needed = [
                "USD",
                "EUR",
                "RUB",
                "GBP",
                "KZT"
            ]

            result = {}

            for item in data:

                if item["Ccy"] in needed:

                    result[item["Ccy"]] = {
                        "rate": float(item["Rate"]),
                        "diff": float(item["Diff"])
                    }

            return Response(result)

        except Exception as e:

            return Response(
                {
                    "error": str(e)
                },
                status=500
            )