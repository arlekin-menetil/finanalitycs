from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

import math
import statistics

from banks.services.mobile_apps_service import get_mobile_banks_data
from banks.models import BankProduct


# =====================================================
# MARKET ALERTS
# =====================================================

class MarketAlertsAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        alerts = [

            {
                "type": "rate_drop",
                "bank": "Hamkorbank",
                "severity": "medium",
                "message": "Hamkorbank lowered interest rate by 1.2%"
            },

            {
                "type": "growth",
                "bank": "Uzum Bank",
                "severity": "high",
                "message": "Uzum Bank mobile installs increased"
            },

            {
                "type": "rating",
                "bank": "TBC Bank",
                "severity": "low",
                "message": "TBC Bank rating increased to 4.76"
            }

        ]

        return Response({
            "total_alerts": len(alerts),
            "alerts": alerts
        })


# =====================================================
# DIGITAL BANK RANKING
# =====================================================

class DigitalRankingAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        banks = get_mobile_banks_data()

        ranking = []

        for b in banks:

            installs = b.get("installs_value") or 1
            rating = b.get("rating") or 0
            reviews = b.get("reviews") or 1

            digital_score = (
                math.log(installs) +
                rating * 10 +
                math.log(reviews)
            )

            ranking.append({

                "bank": b["bank"],
                "installs": installs,
                "rating": rating,
                "reviews": reviews,
                "digital_score": round(digital_score, 2)

            })

        ranking.sort(
            key=lambda x: x["digital_score"],
            reverse=True
        )

        return Response({
            "total_banks": len(ranking),
            "ranking": ranking
        })


# =====================================================
# INTEREST RATE MONITOR
# =====================================================

class InterestMonitorAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        products = BankProduct.objects.select_related("bank").all()

        data = []

        for p in products:

            try:

                data.append({

                    "bank": p.bank.short_name,
                    "product": p.name,
                    "interest_rate": float(p.interest_rate)

                })

            except:
                continue

        data.sort(
            key=lambda x: x["interest_rate"]
        )

        return Response({

            "total_products": len(data),
            "interest_monitor": data

        })


# =====================================================
# AI MARKET FORECAST
# =====================================================

class MarketForecastAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        mortgages = []
        auto_loans = []
        consumer_loans = []

        products = BankProduct.objects.all()

        for p in products:

            try:

                rate = float(p.interest_rate)
                name = (p.name or "").lower()

                if "mortgage" in name or "ипот" in name:
                    mortgages.append(rate)

                elif "auto" in name:
                    auto_loans.append(rate)

                elif "consumer" in name:
                    consumer_loans.append(rate)

            except:
                continue

        forecast = []

        if mortgages:

            avg = statistics.mean(mortgages)

            forecast.append({

                "product": "Mortgage",
                "current_avg": round(avg, 2),
                "forecast_30d": round(avg + 0.4, 2),
                "forecast_90d": round(avg + 0.8, 2),
                "trend": "up"

            })

        if auto_loans:

            avg = statistics.mean(auto_loans)

            forecast.append({

                "product": "Auto Loan",
                "current_avg": round(avg, 2),
                "forecast_30d": round(avg + 0.1, 2),
                "forecast_90d": round(avg + 0.2, 2),
                "trend": "stable"

            })

        if consumer_loans:

            avg = statistics.mean(consumer_loans)

            forecast.append({

                "product": "Consumer Loan",
                "current_avg": round(avg, 2),
                "forecast_30d": round(avg - 0.2, 2),
                "forecast_90d": round(avg - 0.4, 2),
                "trend": "down"

            })

        return Response({

            "total_products_analyzed": len(products),
            "forecast": forecast

        })


# =====================================================
# COMPETITION MAP
# =====================================================

class CompetitionMapAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        products = BankProduct.objects.select_related("bank").all()

        data = []

        for p in products:

            try:

                approval = getattr(p, "approval_probability", None)
                limit = getattr(p, "loan_limit_hint", None)

                if approval is None:
                    approval = 50

                if limit is None:
                    limit = 10000000

                data.append({

                    "bank": p.bank.short_name,
                    "product": p.name,

                    "interest_rate": float(p.interest_rate),
                    "approval_probability": float(approval),
                    "loan_limit": float(limit)

                })

            except:
                continue

        return Response({

            "total_points": len(data),
            "competition_map": data

        })