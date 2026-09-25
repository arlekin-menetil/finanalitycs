from collections import defaultdict



from django.db.models import Q



from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication



from .models import (

    Bank,

    BankProduct,

)



from .recommendation_engine import (

    get_best_products,

    get_top_recommendations,

)



# ==================================================

# HELPERS

# ==================================================





def get_field(

    obj,

    field,

    default=None,

):

    if isinstance(obj, dict):

        return obj.get(field, default)



    return getattr(

        obj,

        field,

        default,

    )





def safe_float(

    value,

    default=0.0,

):

    try:

        if value is None:

            return default



        return float(value)



    except Exception:

        return default





def get_product_bank(

    product,

):

    """

    Safely returns related bank object if it exists.

    """

    bank = getattr(

        product,

        "bank",

        None,

    )



    if bank:

        return bank



    return None





def get_product_bank_name(

    product,

):

    """

    Returns normalized bank name from a recommendation product.

    """

    bank = get_product_bank(product)



    if bank:

        bank_name = getattr(

            bank,

            "short_name",

            None,

        ) or getattr(

            bank,

            "name",

            None,

        )



        if bank_name:

            return str(bank_name)



    bank_name = get_field(

        product,

        "bank_name",

        None,

    )



    if bank_name:

        return str(bank_name)



    bank_value = get_field(

        product,

        "bank",

        None,

    )



    if bank_value and not hasattr(

        bank_value,

        "_meta",

    ):

        return str(bank_value)



    return "Unknown Bank"





def get_product_bank_id(

    product,

):

    """

    Returns related bank ID if available.

    """

    bank = get_product_bank(product)



    if bank:

        return getattr(

            bank,

            "id",

            None,

        )



    return get_field(

        product,

        "bank_id",

        None,

    )





# ==================================================

# LEGACY PRIORITY SORT

# ==================================================





def sort_with_priority(items):

    """

    Legacy helper kept for backward compatibility.



    It is intentionally NOT used for the new AI recommendation

    ranking. The recommendation engine is now the source of truth.

    """



    def priority(item):

        product = item.get("product") if isinstance(item, dict) else item



        bank_name = (

            get_field(

                product,

                "bank_name",

                "",

            )

            or ""

        ).lower()



        best_rate = safe_float(

            get_field(

                product,

                "best_rate",

                None,

            )

            or get_field(

                product,

                "interest_rate",

                999,

            ),

            999,

        )



        if "hamkor" in bank_name:

            return (

                0,

                best_rate,

            )



        if "aloqa" in bank_name:

            return (

                1,

                best_rate,

            )



        return (

            2,

            best_rate,

        )



    return sorted(

        items,

        key=priority,

    )





# ==================================================

# BANK LIST

# ==================================================





class BankListAPIView(APIView):



    authentication_classes = []



    permission_classes = [

        AllowAny,

    ]



    def get(

        self,

        request,

    ):

        search = request.GET.get(

            "search",

        )



        qs = Bank.objects.filter(

            type="bank",

        )



        if search:

            qs = qs.filter(

                Q(

                    name__icontains=search,

                )

                | Q(

                    short_name__icontains=search,

                )

            )



        qs = qs.order_by(

            "name",

        )



        data = [

            {

                "id": bank.id,

                "name": bank.name,

                "short_name": bank.short_name,

            }

            for bank in qs

        ]



        return Response(

            {

                "total": qs.count(),

                "banks": data,

            }

        )





# ==================================================

# RECOMMENDATIONS

# ==================================================





class RecommendationsAPIView(APIView):



    authentication_classes = [
        JWTAuthentication,
    ]



    permission_classes = [

        AllowAny,

    ]



    def get(

        self,

        request,

    ):

        try:

            limit = int(

                request.GET.get(

                    "limit",

                    500,

                )

            )



        except Exception:

            limit = 500



        if limit <= 0:

            limit = 500



        data = []



        user = request.user if request.user.is_authenticated else None



        # ==========================================

        # AUTHORIZED USER

        # ==========================================



        if user:



            products = get_top_recommendations(

                user,

                limit=limit,

            )



            for product in products:



                bank = get_product_bank(

                    product,

                )



                bank_name = get_product_bank_name(

                    product,

                )



                data.append(

                    {

                        "product_id": product.id,

                        "bank_id": get_product_bank_id(

                            product,

                        ),

                        "bank_name": bank_name,

                        "product_name": product.name,

                        "product_type": getattr(

                            product,

                            "product_type",

                            "loan",

                        ),

                        "loan_type": getattr(

                            product,

                            "loan_type",

                            getattr(

                                product,

                                "product_type",

                                "loan",

                            ),

                        ),

                        "interest_rate": safe_float(

                            getattr(

                                product,

                                "interest_rate",

                                0,

                            )

                        ),

                        "approval_probability": safe_float(

                            getattr(

                                product,

                                "approval_probability",

                                0,

                            )

                        ),

                        "ranking_score": safe_float(

                            getattr(

                                product,

                                "ranking_score",

                                0,

                            )

                        ),

                        "loan_limit_hint": safe_float(

                            getattr(

                                product,

                                "loan_limit_hint",

                                0,

                            )

                        ),

                        "term": getattr(

                            product,

                            "term",

                            None,

                        ),

                        "description": getattr(

                            product,

                            "description",

                            "",

                        ),

                        "website": getattr(

                            product,

                            "source_url",

                            "",

                        ),

                        "is_online": bool(

                            getattr(

                                product,

                                "is_online",

                                False,

                            )

                        ),

                        "offers_count": 1,

                        "banks_count": 1,

                        "is_featured": (

                            getattr(

                                bank,

                                "is_featured",

                                False,

                            )

                            if bank

                            else False

                        ),

                    }

                )



        # ==========================================

        # GUEST USER

        # ==========================================



        else:



            products = get_best_products(

                limit=5000,

            )



            for product in products:



                bank_name = (

                    get_field(

                        product,

                        "bank_name",

                    )

                    or get_field(

                        product,

                        "bank",

                    )

                    or "Unknown Bank"

                )



                data.append(

                    {

                        "product_id": get_field(

                            product,

                            "id",

                        ),

                        "bank_id": get_field(

                            product,

                            "bank_id",

                        ),

                        "bank_name": bank_name,

                        "product_name": (

                            get_field(

                                product,

                                "name",

                            )

                            or "Кредит"

                        ),

                        "product_type": get_field(

                            product,

                            "product_type",

                            "loan",

                        ),

                        "loan_type": get_field(

                            product,

                            "loan_type",

                            get_field(

                                product,

                                "product_type",

                                "loan",

                            ),

                        ),

                        "interest_rate": safe_float(

                            get_field(

                                product,

                                "interest_rate",

                            )

                        ),

                        "approval_probability": round(

                            safe_float(

                                get_field(

                                    product,

                                    "approval_probability",

                                    75,

                                )

                            ),

                            2,

                        ),

                        "ranking_score": round(

                            safe_float(

                                get_field(

                                    product,

                                    "ranking_score",

                                    get_field(

                                        product,

                                        "score",

                                        50,

                                    ),

                                )

                            ),

                            2,

                        ),

                        "loan_limit_hint": get_field(

                            product,

                            "max_amount",

                        ),

                        "term": get_field(

                            product,

                            "term",

                        ),

                        "description": get_field(

                            product,

                            "description",

                        ),

                        "website": (

                            get_field(

                                product,

                                "website",

                            )

                            or get_field(

                                product,

                                "source_url",

                            )

                            or get_field(

                                product,

                                "bank_url",

                            )

                        ),

                        "is_online": bool(

                            get_field(

                                product,

                                "is_online",

                                False,

                            )

                        ),

                        "offers_count": 1,

                        "banks_count": 1,

                        "is_featured": False,

                    }

                )



        return Response(

            {

                "total": len(data),

                "recommendations": data,

            }

        )





# ==================================================

# TOP BANKS

# ==================================================





class TopBanksAPIView(APIView):



    authentication_classes = [
        JWTAuthentication,
    ]



    permission_classes = [

        AllowAny,

    ]



    def get(

        self,

        request,

    ):

        try:

            limit = int(

                request.GET.get(

                    "limit",

                    5,

                )

            )



        except Exception:

            limit = 5



        if limit <= 0:

            limit = 5



        user = request.user if request.user.is_authenticated else None



        # ==================================================

        # AUTHORIZED USER

        #

        # IMPORTANT:

        # Top Banks uses exactly the same AI recommendation

        # engine as RecommendationsAPIView.

        #

        # No bank names are hardcoded here.

        # ==================================================



        if user:



            products = get_top_recommendations(

                user,

                limit=500,

            )



            bank_data = {}



            for product in products:



                bank_name = get_product_bank_name(

                    product,

                )



                if not bank_name:

                    continue



                bank_id = get_product_bank_id(

                    product,

                )



                ranking_score = safe_float(

                    getattr(

                        product,

                        "ranking_score",

                        0,

                    )

                )



                approval_probability = safe_float(

                    getattr(

                        product,

                        "approval_probability",

                        0,

                    )

                )



                interest_rate = safe_float(

                    getattr(

                        product,

                        "interest_rate",

                        0,

                    )

                )



                if bank_name not in bank_data:



                    bank_data[bank_name] = {

                        "bank": bank_name,

                        "bank_id": bank_id,

                        "score": ranking_score,

                        "ranking_score": ranking_score,

                        "approval_probability": approval_probability,

                        "interest_rate": interest_rate,

                        "offers": 1,

                    }



                    continue



                current = bank_data[bank_name]



                current["offers"] += 1



                # ------------------------------------------

                # Best AI product becomes bank score

                # ------------------------------------------



                if ranking_score > current["ranking_score"]:



                    current["score"] = ranking_score

                    current["ranking_score"] = ranking_score

                    current["approval_probability"] = approval_probability

                    current["interest_rate"] = interest_rate



            result = list(bank_data.values())



            # ==================================================

            # PRIMARY:

            # best AI ranking_score of the bank

            #

            # SECONDARY:

            # approval probability

            #

            # TERTIARY:

            # lower interest rate

            # ==================================================



            result.sort(

                key=lambda item: (

                    item["ranking_score"],

                    item["approval_probability"],

                    -item["interest_rate"],

                ),

                reverse=True,

            )



            return Response(result[:limit])



        # ==================================================

        # GUEST USER

        #

        # No personal profile exists, therefore we use the

        # public product ranking from get_best_products().

        # ==================================================



        products = get_best_products(

            limit=5000,

        )



        bank_data = {}



        for product in products:



            bank_name = (

                get_field(

                    product,

                    "bank_name",

                )

                or get_field(

                    product,

                    "bank",

                )

                or "Unknown Bank"

            )



            bank_id = get_field(

                product,

                "bank_id",

            )



            ranking_score = safe_float(

                get_field(

                    product,

                    "ranking_score",

                    get_field(

                        product,

                        "score",

                        0,

                    ),

                )

            )



            approval_probability = safe_float(

                get_field(

                    product,

                    "approval_probability",

                    75,

                )

            )



            interest_rate = safe_float(

                get_field(

                    product,

                    "interest_rate",

                    get_field(

                        product,

                        "best_rate",

                        0,

                    ),

                )

            )



            if bank_name not in bank_data:



                bank_data[bank_name] = {

                    "bank": bank_name,

                    "bank_id": bank_id,

                    "score": ranking_score,

                    "ranking_score": ranking_score,

                    "approval_probability": approval_probability,

                    "interest_rate": interest_rate,

                    "offers": 1,

                }



                continue



            current = bank_data[bank_name]



            current["offers"] += 1



            if ranking_score > current["ranking_score"]:



                current["score"] = ranking_score

                current["ranking_score"] = ranking_score

                current["approval_probability"] = approval_probability

                current["interest_rate"] = interest_rate



        result = list(bank_data.values())



        result.sort(

            key=lambda item: (

                item["ranking_score"],

                item["approval_probability"],

                -item["interest_rate"],

            ),

            reverse=True,

        )



        return Response(result[:limit])





# ==================================================

# BACKWARD COMPATIBILITY

# ==================================================





class RecommendationAPIView(RecommendationsAPIView):

    pass
