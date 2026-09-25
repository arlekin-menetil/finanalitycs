from django.db.models import Min

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)
from rest_framework import status

from banks.models import (
    BankProduct,
    AggregatedProduct,
)

from banks.services.matching_engine import (
    get_top_recommendations,
)

from banks.services.market_rating_engine import (
    get_market_rating,
)

from banks.services.mobile_apps_service import (
    get_mobile_banks_data,
)

# ==========================================
# 💣 PRIORITY BANKS
# ==========================================
PRIORITY_BANKS = [
    "Hamkorbank",
    "Aloqabank",
    "Kapitalbank",
    "NBU",
    "SQB",
]


# ==========================================
# 💣 SAFE FLOAT
# ==========================================
def safe_float(value):

    try:

        if value in [None, ""]:
            return None

        return float(value)

    except Exception:

        return None


# ==========================================
# 💣 SAFE INT
# ==========================================
def safe_int(value):

    try:

        if value in [None, ""]:
            return None

        return int(value)

    except Exception:

        return None


# ==========================================
# 💣 SAFE BOOL
# ==========================================
def safe_bool(value):

    return bool(value)


# ==========================================
# 💣 BANK SERIALIZER
# ==========================================
def get_bank_data(bank):

    if not bank:

        return {
            "id": None,
            "name": "Unknown Bank",
            "short_name": None,
            "is_unknown": True,
        }

    return {
        "id": getattr(bank, "id", None),
        "name": getattr(bank, "name", "Unknown Bank"),
        "short_name": getattr(bank, "short_name", None),
        "is_unknown": False,
    }


# ==========================================
# 💣 PRODUCT SERIALIZER
# ==========================================
def serialize_product(product):

    bank = getattr(product, "bank", None)

    bank_name = (
        getattr(product, "bank_name", None)
        or (bank.name if bank else None)
        or "Unknown Bank"
    )

    short_name = (
        getattr(bank, "short_name", None)
        if bank
        else None
    )

    logo_name = (
        short_name
        or bank_name
    ).lower().replace(" ", "").replace("-", "")

    return {

        # =====================================
        # IDS
        # =====================================

        "id": product.id,

        "bank_id": (
            bank.id
            if bank
            else None
        ),

        # =====================================
        # BANK
        # =====================================

        "bank_name": bank_name,

        "bank": get_bank_data(bank),

        "bank_logo": f"/banks/{logo_name}.png",

        # =====================================
        # PRODUCT
        # =====================================

        "name": product.name,

        "normalized_name": product.normalized_name,

        "product_type": product.product_type,

        "loan_type": product.loan_type,

        "currency": product.currency,

        # =====================================
        # RATES
        # =====================================

        "interest_rate": safe_float(
            product.interest_rate
        ),

        "min_rate": safe_float(
            product.min_rate
        ),

        "max_rate": safe_float(
            product.max_rate
        ),

        # =====================================
        # AMOUNT
        # =====================================

        "max_amount": safe_float(
            product.max_amount
        ),

        "term": product.term,

        # =====================================
        # ONLINE
        # =====================================

        "is_online": safe_bool(
            product.is_online
        ),

        # =====================================
        # DESCRIPTION
        # =====================================

        "description": product.description,

        # =====================================
        # LINKS
        # =====================================

        "source_url": product.source_url,

        "bank_url": product.bank_url,

        # =====================================
        # IMAGES
        # =====================================

        "image_url": product.image_url,

        "thumbnail_url": product.thumbnail_url,

        # =====================================
        # META
        # =====================================

        "source_name": product.source_name,

        "ranking_score": safe_float(
            product.score
        ),

        "raw_data": product.raw_data or {},

    }

# ==========================================
# 💣 SORT PRODUCTS
# ==========================================
def sort_products(products):

    def score(product):

        bank_name = (
            product.bank.name
            if getattr(product, "bank", None)
            else (getattr(product, "bank_name", "") or "")
        )

        priority = 0 if bank_name in PRIORITY_BANKS else 1

        rate = safe_float(getattr(product, "interest_rate", None))

        if rate is None:
            rate = 999

        amount = safe_float(getattr(product, "max_amount", None)) or 0

        return (
            priority,
            rate,
            -amount,
            getattr(product, "id", 0) or 0,
        )

    return sorted(products, key=score)


# ==========================================
# 💣 PRODUCTS BY SOURCE
# ==========================================
class ProductsBySourceAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        result = {
            "bankuz": [],
            "depozit": [],
            "bankxizmatlari": [],
        }

        products = BankProduct.objects.filter(is_active=True).select_related("bank")

        for product in products:

            item = serialize_product(product)

            source = getattr(product, "source_name", None) or getattr(
                product, "source", None
            )

            if source == "bankuz":

                result["bankuz"].append(item)

            elif source == "depozit":

                result["depozit"].append(item)

            else:

                result["bankxizmatlari"].append(item)

        return Response(result)


# ==========================================
# 💣 PRODUCTS
# ==========================================
class BankProductsAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        queryset = (
            BankProduct.objects
            .filter(is_active=True)
            .select_related("bank")
        )

        # ======================================
        # SEARCH
        # ======================================

        search = request.GET.get("search")

        if search:

            queryset = queryset.filter(
                name__icontains=search
            )

        # ======================================
        # BANK
        # ======================================

        bank = request.GET.get("bank")

        if bank:

            queryset = queryset.filter(
                bank_name__icontains=bank
            )

        # ======================================
        # PRODUCT TYPE
        # ======================================

        product_type = request.GET.get("type")

        if product_type:

            queryset = queryset.filter(
                product_type=product_type
            )

        # ======================================
        # CURRENCY
        # ======================================

        currency = request.GET.get("currency")

        if currency:

            queryset = queryset.filter(
                currency__iexact=currency
            )

        # ======================================
        # ONLINE
        # ======================================

        online = request.GET.get("online")

        if online:

            if online.lower() in [
                "true",
                "1",
                "yes",
            ]:

                queryset = queryset.filter(
                    is_online=True
                )

        # ======================================
        # SORTING
        # ======================================

        ordering = request.GET.get(
            "ordering",
            "score",
        )

        if ordering == "rate":

            queryset = queryset.order_by(
                "interest_rate",
                "-score",
            )

        elif ordering == "amount":

            queryset = queryset.order_by(
                "-max_amount",
                "-score",
            )

        elif ordering == "bank":

            queryset = queryset.order_by(
                "bank_name",
                "interest_rate",
            )

        else:

            queryset = queryset.order_by(
                "-score",
                "interest_rate",
            )

        # ======================================
        # PAGINATION
        # ======================================

        page = int(
            request.GET.get(
                "page",
                1,
            )
        )

        page_size = int(
            request.GET.get(
                "page_size",
                request.GET.get(
                    "limit",
                    20,
                ),
            )
        )

        total = queryset.count()

        start = (page - 1) * page_size

        end = start + page_size

        products = queryset[start:end]

        # ======================================
        # RESPONSE
        # ======================================

        return Response(

            {

                "count": total,

                "page": page,

                "page_size": page_size,

                "pages": (
                    total + page_size - 1
                ) // page_size,

                "results": [

                    serialize_product(
                        product
                    )

                    for product in products

                ],

            }

        )
# ==========================================
# 💣 PRODUCT DETAIL
# ==========================================
class BankProductDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(
        self,
        request,
        pk=None,
        product_id=None,
        *args,
        **kwargs,
    ):

        try:

            object_id = (
                product_id
                or pk
                or kwargs.get("product_id")
                or kwargs.get("pk")
            )

            if not object_id:

                return Response(
                    {"detail": "Product id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            product = (
                BankProduct.objects
                .select_related("bank")
                .get(
                    pk=object_id,
                    is_active=True,
                )
            )

            return Response(
                serialize_product(product)
            )

        except BankProduct.DoesNotExist:

            return Response(
                {"detail": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:

            print(
                "💥 PRODUCT DETAIL ERROR:",
                e,
            )

            return Response(
                {"detail": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
# ==========================================
# 💣 BEST PRODUCTS
# ==========================================
class BestBankProductsAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        best_rates = (
            BankProduct.objects.filter(is_active=True, interest_rate__isnull=False)
            .values("bank")
            .annotate(best_rate=Min("interest_rate"))
        )

        result = []

        for item in best_rates:

            product = (
                BankProduct.objects.select_related("bank")
                .filter(bank=item["bank"], interest_rate=item["best_rate"])
                .first()
            )

            if not product:
                continue

            result.append(serialize_product(product))

        return Response(result)


# ==========================================
# 💣 AGGREGATED PRODUCTS
# ==========================================
class AggregatedProductsAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        qs = AggregatedProduct.objects.all().order_by("best_rate")

        result = []

        for item in qs:

            result.append(
                {
                    "id": getattr(item, "id", None),
                    "name": getattr(item, "name", None),
                    "category": getattr(item, "name", None),
                    "slug": getattr(item, "slug", None),
                    "key": getattr(item, "normalized_name", None),
                    "best_rate": safe_float(getattr(item, "best_rate", None)),
                    "min_rate": safe_float(getattr(item, "min_rate", None)),
                    "max_rate": safe_float(getattr(item, "max_rate", None)),
                    "offers_count": getattr(item, "offers_count", 0),
                    "banks_count": getattr(item, "banks_count", 0),
                    "is_online": safe_bool(getattr(item, "is_online", False)),
                }
            )

        return Response(result)


# ==========================================
# 💣 RECOMMENDATIONS
# ==========================================
class RecommendationsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("🔥 RecommendationsAPIView CALLED")

        products = get_top_recommendations(request.user, 5) or []

        return Response(
            {
                "total": len(products),
                "recommendations": [serialize_product(p) for p in products],
            }
        )


# ==========================================
# 💣 TOP RECOMMENDATIONS
# ==========================================
class TopRecommendationsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        products = get_top_recommendations(request.user, 100) or []

        return Response([serialize_product(p) for p in products])


# ==========================================
# 💣 MOBILE ANALYTICS
# ==========================================
class MobileBanksAnalyticsAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        data = get_mobile_banks_data()

        return Response(
            {
                "total_banks": len(data),
                "banks": data,
            }
        )


# ==========================================
# 💣 MARKET RATING
# ==========================================
class MarketRatingAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        rating = get_market_rating()

        return Response(
            {
                "total_banks": len(rating),
                "rating": rating,
            }
        )
