import requests

from datetime import datetime, timedelta

from rest_framework.response import Response
from rest_framework.views import APIView


class CurrencyHistoryView(APIView):

    def get(self, request):

        currencies = [
            "USD",
            "EUR",
            "RUB",
            "GBP",
            "KZT",
        ]

        result = {}

        try:

            today = datetime.today()

            for currency in currencies:

                history = []

                for i in range(7):

                    date = (
                        today - timedelta(days=i)
                    ).strftime("%Y-%m-%d")

                    url = (
                        "https://cbu.uz/uz/"
                        f"arkhiv-kursov-valyut/json/{currency}/{date}/"
                    )

                    try:

                        response = requests.get(
                            url,
                            timeout=10
                        )

                        data = response.json()

                        if data:

                            history.append({

                                "date": date,

                                "rate": float(
                                    data[0]["Rate"]
                                )

                            })

                    except Exception:
                        pass

                result[currency] = list(
                    reversed(history)
                )

            return Response(result)

        except Exception as e:

            return Response(
                {
                    "error": str(e)
                },
                status=500
            )