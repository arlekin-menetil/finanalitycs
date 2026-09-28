import requests

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta

from django.core.cache import cache

from rest_framework.response import Response
from rest_framework.views import APIView


class CurrencyHistoryView(APIView):

    CACHE_KEY = "currency_history_7_days"
    CACHE_TIMEOUT = 60 * 60  # 1 час

    CURRENCIES = [
        "USD",
        "EUR",
        "RUB",
        "GBP",
        "KZT",
    ]

    def get_history(self, currency, date):
        url = "https://cbu.uz/uz/" f"arkhiv-kursov-valyut/json/{currency}/{date}/"

        try:
            response = requests.get(
                url,
                timeout=5,
            )

            response.raise_for_status()

            data = response.json()

            if not data:
                return None

            return {
                "date": date,
                "rate": float(data[0]["Rate"]),
            }

        except Exception:
            return None

    def get(self, request):
        cached_result = cache.get(self.CACHE_KEY)

        if cached_result is not None:
            return Response(cached_result)

        try:
            today = datetime.today()

            tasks = []

            for currency in self.CURRENCIES:
                for i in range(7):
                    date = (today - timedelta(days=i)).strftime("%Y-%m-%d")

                    tasks.append((currency, date))

            result = {currency: [] for currency in self.CURRENCIES}

            with ThreadPoolExecutor(max_workers=10) as executor:

                future_map = {
                    executor.submit(
                        self.get_history,
                        currency,
                        date,
                    ): (currency, date)
                    for currency, date in tasks
                }

                for future in as_completed(future_map):

                    currency, date = future_map[future]

                    try:
                        history_item = future.result()

                        if history_item is not None:
                            result[currency].append(history_item)

                    except Exception:
                        pass

            for currency in result:
                result[currency].sort(key=lambda item: item["date"])

            cache.set(
                self.CACHE_KEY,
                result,
                self.CACHE_TIMEOUT,
            )

            return Response(result)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=500,
            )
