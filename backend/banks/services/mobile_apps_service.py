from google_play_scraper import app
from django.core.cache import cache
import re

# =====================================================
# PACKAGE IDS GOOGLE PLAY
# =====================================================

BANK_APPS = {

    "Hamkorbank": "uz.hamkorbank.mobile",

    "Aloqabank": "uz.aloqabank.zoomrad",

    "SQB": "com.uzpsb.olam",

    "Uzum Bank": "uz.kapitalbank.android",

    "TBC Bank": "ge.space.app.uzbekistan"

}

CACHE_KEY = "mobile_bank_metrics"

# во время разработки лучше небольшой TTL
CACHE_TTL = 60 * 60  # 1 час


# =====================================================
# HELPERS
# =====================================================

def parse_installs(installs_string):
    """
    Преобразует строку installs из Google Play
    например: '10,000,000+' -> 10000000
    """

    if not installs_string:
        return None

    numbers = re.sub(r"[^\d]", "", installs_string)

    try:
        return int(numbers)
    except Exception:
        return None


# =====================================================
# FETCH SINGLE APP
# =====================================================

def fetch_playstore_metrics(package):

    try:

        result = app(
            package,
            lang="en",
            country="uz"
        )

        installs_raw = result.get("installs")

        return {

            "installs": installs_raw,
            "installs_value": parse_installs(installs_raw),

            "rating": result.get("score"),
            "reviews": result.get("ratings")

        }

    except Exception as e:

        return {

            "installs": None,
            "installs_value": None,

            "rating": None,
            "reviews": None,

            "error": str(e)

        }


# =====================================================
# MAIN SERVICE
# =====================================================

def get_mobile_banks_data():

    # ==========================================
    # CACHE
    # ==========================================

    cached = cache.get(CACHE_KEY)

    if cached:
        return cached

    # ==========================================
    # FETCH DATA
    # ==========================================

    data = []

    for bank, package in BANK_APPS.items():

        metrics = fetch_playstore_metrics(package)

        data.append({

            "bank": bank,

            "installs": metrics.get("installs"),
            "installs_value": metrics.get("installs_value"),

            "rating": metrics.get("rating"),
            "reviews": metrics.get("reviews")

        })

    # ==========================================
    # SAVE CACHE
    # ==========================================

    cache.set(CACHE_KEY, data, CACHE_TTL)

    return data