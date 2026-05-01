import pytest
import logging
import os
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright
from pytest_html import extras

# ============================================================================
# LOGGING SETUP (SAFE, NO DUPLICATES)
# ============================================================================

logger = logging.getLogger("QA-AUTOMATION")


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    logs_dir = Path("logs")
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_file = logs_dir / f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)

    # IMPORTANT: prevent duplicate handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    logger.info("=" * 70)
    logger.info("TEST SESSION STARTED")
    logger.info("=" * 70)

    yield

    logger.info("=" * 70)
    logger.info("TEST SESSION ENDED")
    logger.info("=" * 70)


# ============================================================================
# PLAYWRIGHT FIXTURE
# ============================================================================

@pytest.fixture
def page(request):
    logger.info(f"Starting test: {request.node.name}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        logger.info(f"Browser launched: {request.node.name}")

        yield page

        logger.info(f"Closing browser: {request.node.name}")
        context.close()
        browser.close()


# ============================================================================
# SCREENSHOT FUNCTION
# ============================================================================

def capture_screenshot(page, test_name):
    screenshots_dir = Path("screenshots")
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = screenshots_dir / f"{test_name}_{timestamp}.png"

    page.screenshot(path=str(path))

    logger.error(f"[SCREENSHOT SAVED] {path}")
    logger.error(f"URL: {page.url}")
    logger.error(f"TITLE: {page.title()}")

    return str(path)


# ============================================================================
# PYTEST HOOK (FAILURE HANDLING + REPORT ATTACHMENT)
# ============================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    setattr(item, f"rep_{rep.when}", rep)

    if rep.when == "call":

        page = item.funcargs.get("page")

        # ---------------- FAILURE CASE ----------------
        if rep.failed and page:

            logger.error(f"[FAILED] {item.name}")
            logger.error(f"Duration: {rep.duration:.2f}s")

            screenshot_path = capture_screenshot(page, item.name)

            # 🔥 ATTACH TO PYTEST-HTML REPORT (FIX FOR "LINKS")
            if screenshot_path:
                rep.extra = getattr(rep, "extra", [])
                rep.extra.append(extras.png(screenshot_path))

        # ---------------- PASS CASE ----------------
        elif rep.passed:
            logger.info(f"[PASSED] {item.name} | {rep.duration:.2f}s")