from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from banks.merge_engine import run_merge


# =====================================================
# 🔥 SAFE FLOAT
# =====================================================
def safe_float(value):
    try:
        return float(value)
    except:
        return None


# =====================================================
# 💣 AGGREGATED PRODUCTS (FINAL FIX)
# =====================================================
class AggregatedProductsAPIView(APIView):
    """
    💣 Финальный агрегированный API
    Работает с merge_engine (dict)
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):

        # =========================
        # 💣 LOAD DATA
        # =========================
        raw_data = run_merge()

        data = []

        # =========================
        # 💣 NORMALIZE
        # =========================
        for item in raw_data:

            min_rate = safe_float(item.get("min_rate"))
            max_rate = safe_float(item.get("max_rate"))
            best_rate = safe_float(item.get("best_rate"))

            data.append({
                "name": item.get("name"),
                "product_type": item.get("product_type"),

                "min_rate": min_rate,
                "max_rate": max_rate,
                "best_rate": best_rate,

                "offers_count": item.get("count", 0),
                "banks_count": item.get("banks_count", 0),

                "best_bank": item.get("best_bank"),

                "is_online": item.get("is_online", False),

                # 💣 удобно для фронта
                "rating": round(100 - (best_rate or 100), 2)
            })

        # =========================
        # 💣 FILTERS
        # =========================
        product_type = request.GET.get("type")

        if product_type:
            data = [
                x for x in data
                if x.get("product_type") == product_type
            ]

        # =========================
        # 💣 SORTING (SAFE)
        # =========================
        sort_by = request.GET.get("sort", "best_rate")

        if sort_by == "min_rate":
            data.sort(key=lambda x: x["min_rate"] if x["min_rate"] is not None else 999)

        elif sort_by == "max_rate":
            data.sort(key=lambda x: x["max_rate"] if x["max_rate"] is not None else 0, reverse=True)

        elif sort_by == "best_rate":
            data.sort(key=lambda x: x["best_rate"] if x["best_rate"] is not None else 999)

        elif sort_by == "offers":
            data.sort(key=lambda x: x["offers_count"], reverse=True)

        elif sort_by == "banks":
            data.sort(key=lambda x: x["banks_count"], reverse=True)

        elif sort_by == "rating":
            data.sort(key=lambda x: x["rating"], reverse=True)

        # =========================
        # 💣 LIMIT
        # =========================
        limit = request.GET.get("limit")

        try:
            if limit:
                data = data[:int(limit)]
        except:
            pass

        # =========================
        # 💣 RESPONSE
        # =========================
        return Response({
            "total": len(data),
            "results": data
        })


# =====================================================
# 💣 OPTIONAL: DETAIL (чтобы убрать ImportError)
# =====================================================
class AggregatedProductDetailAPIView(APIView):
    """
    💣 DETAIL по ключу (fix ImportError)
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, key):

        raw_data = run_merge()

        for item in raw_data:
            if item.get("name") == key or item.get("product_type") == key:

                return Response({
                    "name": item.get("name"),
                    "product_type": item.get("product_type"),
                    "min_rate": safe_float(item.get("min_rate")),
                    "max_rate": safe_float(item.get("max_rate")),
                    "best_rate": safe_float(item.get("best_rate")),
                    "offers_count": item.get("count", 0),
                    "banks_count": item.get("banks_count", 0),
                    "best_bank": item.get("best_bank"),
                    "is_online": item.get("is_online", False),
                })

        return Response({"error": "Not found"}, status=404)