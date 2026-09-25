from rest_framework.decorators import api_view
from rest_framework.response import Response
from banks.merge_engine import run_merge


@api_view(["GET"])
def aggregated_products(request):
    data = run_merge()

    # 🔥 сортировка (по умолчанию)
    sort_by = request.GET.get("sort", "min_rate")

    if sort_by == "min_rate":
        data.sort(key=lambda x: x["min_rate"] or 999)

    elif sort_by == "max_rate":
        data.sort(key=lambda x: x["max_rate"] or 0)

    elif sort_by == "offers":
        data.sort(key=lambda x: x["count"], reverse=True)

    elif sort_by == "banks":
        data.sort(key=lambda x: x["banks_count"], reverse=True)

    return Response(data)