import pytest
from playwright.sync_api import sync_playwright

#THIS is called dependency injection
@pytest.fixture
def page():
    """
    Fixture that provides a Playwright browser page for testing with strict isolation.
    Launches a chromium browser in non-headless mode, creates a new context and page,
    yields it for test use, and closes the context and browser after test completion.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()