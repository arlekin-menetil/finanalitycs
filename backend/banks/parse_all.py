from banks.data_sources import load_all_sources


def run_all():
    """
    💣 Главный pipeline загрузки данных

    Теперь:
    - не парсим всё подряд
    - используем единый слой интеграции
    """

    print("🚀 UNIFIED DATA PIPELINE")

    try:
        total = load_all_sources()
    except Exception as e:
        print("❌ data sources error:", e)
        total = 0

    print(f"\n💣 TOTAL CREATED: {total}")

    return total