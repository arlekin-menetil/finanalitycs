import time
from banks.data_sources import load_all_sources


def run_all():
    print("\n" + "=" * 50)
    print("🚀 UNIFIED DATA PIPELINE START")
    print("=" * 50)

    start_time = time.time()

    total = 0
    status = "OK"

    try:
        print("🔄 Loading all sources...")
        total = load_all_sources()

        print(f"✅ Sources loaded: {total}")

    except Exception as e:
        status = "FAILED"
        print("\n❌ PIPELINE ERROR:", str(e))

    duration = round(time.time() - start_time, 2)

    print("\n" + "=" * 50)
    print("📊 PIPELINE SUMMARY")
    print("=" * 50)

    print(f"🔥 STATUS: {status}")
    print(f"💣 TOTAL CREATED/UPDATED: {total}")
    print(f"⏱ EXECUTION TIME: {duration}s")

    print("=" * 50 + "\n")

    return {
        "status": status,
        "total": total,
        "duration": duration
    }