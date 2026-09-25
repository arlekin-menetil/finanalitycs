import time
import random

from playwright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
)

from .logger import log

# ==========================================
# 💣 REAL USER AGENTS
# ==========================================
USER_AGENTS = [
    (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/124.0.0.0 "
        "Safari/537.36"
    ),
    (
        "Mozilla/5.0 "
        "(Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/124.0.0.0 "
        "Safari/537.36"
    ),
]


# ==========================================
# 💣 RANDOM USER AGENT
# ==========================================
def random_user_agent():

    return random.choice(USER_AGENTS)


# ==========================================
# 💣 HUMAN DELAY
# ==========================================
def human_delay(
    min_ms=1200,
    max_ms=4500,
):

    return random.randint(
        min_ms,
        max_ms,
    )


# ==========================================
# 💣 HUMAN MOUSE
# ==========================================
def human_mouse_move(page):

    try:

        page.mouse.move(
            random.randint(200, 1400),
            random.randint(150, 900),
            steps=random.randint(10, 30),
        )

    except Exception:

        pass


# ==========================================
# 💣 HUMAN SCROLL
# ==========================================
def human_scroll(page):

    try:

        for _ in range(random.randint(1, 3)):

            page.mouse.wheel(
                0,
                random.randint(300, 1200),
            )

            page.wait_for_timeout(
                random.randint(
                    700,
                    1800,
                )
            )

    except Exception:

        pass


# ==========================================
# 💣 STEALTH PATCH
# ==========================================
def apply_stealth(page):

    try:

        page.add_init_script("""
            Object.defineProperty(
                navigator,
                'webdriver',
                {
                    get: () => undefined
                }
            );

            window.chrome = {
                runtime: {}
            };

            Object.defineProperty(
                navigator,
                'languages',
                {
                    get: () => ['ru-RU', 'ru', 'en-US']
                }
            );

            Object.defineProperty(
                navigator,
                'plugins',
                {
                    get: () => [1,2,3,4,5]
                }
            );

            Object.defineProperty(
                navigator,
                'hardwareConcurrency',
                {
                    get: () => 8
                }
            );

            Object.defineProperty(
                navigator,
                'deviceMemory',
                {
                    get: () => 8
                }
            );
        """)

    except Exception as e:

        log(f"⚠️ stealth patch failed: {e}")


# ==========================================
# 💣 BLOCK DETECTION
# ==========================================
def detect_blocked_page(page):

    try:

        html = page.content().lower()

        blocked_signs = [
            "access denied",
            "cf-challenge",
            "checking your browser",
            "security check",
            "temporarily blocked",
            "unusual traffic",
            "verify you are human",
        ]

        hits = 0

        for sign in blocked_signs:

            if sign in html:
                hits += 1

        if hits >= 2:
            return True

    except Exception:

        pass

    return False


# ==========================================
# 💣 PREPARE PAGE
# ==========================================
def prepare_page(page):

    try:

        apply_stealth(page)

        # ======================================
        # 💣 HEADERS
        # ======================================
        try:

            page.set_extra_http_headers(
                {
                    "accept-language": ("ru-RU,ru;q=0.9,en-US;q=0.8"),
                    "cache-control": "max-age=0",
                    "upgrade-insecure-requests": "1",
                }
            )

        except Exception:

            pass

        # ======================================
        # 💣 VIEWPORT
        # ======================================
        try:

            page.set_viewport_size(
                {
                    "width": random.randint(
                        1280,
                        1920,
                    ),
                    "height": random.randint(
                        720,
                        1080,
                    ),
                }
            )

        except Exception:

            pass

    except Exception as e:

        log(f"⚠️ prepare page failed: {e}")


# ==========================================
# 💣 WARMUP SESSION
# ==========================================
def warmup_session(page):

    try:

        log("🔥 session warmup")

        page.goto(
            "https://bank.uz",
            wait_until="domcontentloaded",
            timeout=45000,
        )

        page.wait_for_timeout(
            random.randint(
                3000,
                6000,
            )
        )

        human_mouse_move(page)

        human_scroll(page)

        return True

    except Exception as e:

        log(f"⚠️ warmup failed: {e}")

        return False


# ==========================================
# 💣 SAFE GOTO
# ==========================================
def safe_goto(
    page,
    url,
    retries=5,
    timeout=90000,
):

    prepare_page(page)

    for attempt in range(retries):

        try:

            log(f"🌐 goto attempt " f"{attempt + 1}/{retries}: " f"{url}")

            # ==============================
            # 💣 PRE DELAY
            # ==============================
            time.sleep(
                random.uniform(
                    2.5,
                    6.5,
                )
            )

            # ==============================
            # 💣 OPEN PAGE
            # ==============================
            response = page.goto(
                url,
                timeout=timeout,
                wait_until="domcontentloaded",
            )

            # ==============================
            # 💣 WAIT NETWORK
            # ==============================
            try:

                page.wait_for_load_state(
                    "networkidle",
                    timeout=15000,
                )

            except Exception:

                pass

            # ==============================
            # 💣 HUMAN ACTIONS
            # ==============================
            human_mouse_move(page)

            page.wait_for_timeout(
                human_delay(
                    1500,
                    3500,
                )
            )

            human_scroll(page)

            # ==============================
            # 💣 URL CHECK
            # ==============================
            current_url = str(page.url or "")

            if "bank.uz" not in current_url:

                log(f"⚠️ invalid redirect: " f"{current_url}")

                continue

            # ==============================
            # 💣 STATUS CHECK
            # ==============================
            try:

                if response:

                    status = response.status

                    if status >= 400:

                        log(f"⚠️ bad status: " f"{status}")

                        continue

            except Exception:

                pass

            # ==============================
            # 💣 BLOCK CHECK
            # ==============================
            if detect_blocked_page(page):

                log("🚫 blocked page detected")

                continue

            # ==============================
            # 💣 BODY CHECK
            # ==============================
            try:

                body = page.locator("body")

                if body.count() == 0:

                    raise Exception("body not found")

            except Exception as e:

                log(f"⚠️ body validation failed: " f"{e}")

                continue

            # ==============================
            # 💣 SUCCESS
            # ==============================
            log(f"✅ SUCCESS GOTO: {url}")

            return True

        except PlaywrightTimeoutError:

            log(f"⚠️ timeout attempt " f"{attempt + 1}/{retries}")

        except Exception as e:

            error_text = str(e).lower()

            # ==============================
            # 💣 CONNECTION REFUSED
            # ==============================
            if (
                "err_connection_refused" in error_text
                or "net::err_connection_refused" in error_text
            ):

                log("⚠️ connection refused " "- cooldown")

                time.sleep(
                    random.uniform(
                        15,
                        30,
                    )
                )

            else:

                log(f"⚠️ retry " f"{attempt + 1}/{retries} " f"for {url}: {e}")

        # ==============================
        # 💣 RETRY DELAY
        # ==============================
        try:

            page.wait_for_timeout(
                random.randint(
                    4000,
                    9000,
                )
            )

        except Exception:

            pass

        time.sleep(
            random.uniform(
                4.0,
                8.0,
            )
        )

    log(f"❌ FAILED GOTO: {url}")

    return False
