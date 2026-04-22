import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture
def page():
    """
    Fixture that provides a Playwright browser page for testing.
    Launches a chromium browser in non-headless mode, creates a new page,
    yields it for test use, and closes the browser after test completion.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()