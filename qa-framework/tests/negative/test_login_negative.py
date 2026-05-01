from pages_blueprint.login_page import LoginPage
from utils.logger import TestLogger
import pytest

log = TestLogger(__name__)

@pytest.mark.negative
@pytest.mark.p1
def test_invalid_login(page):
    """
    Negative test: Verify error message on invalid credentials.
    
    This test is designed to demonstrate screenshot capture on failure.
    If assertion fails, hook automatically captures screenshot.
    """
    log.info("=" * 50)
    log.info("TEST: Negative - Invalid Login")
    log.info("=" * 50)
    
    log.step("SETUP", "Initializing login page object")
    login = LoginPage(page)

    log.step("NAVIGATE", "Opening login page")
    login.open()
    
    log.step("LOGIN", "Entering invalid credentials (wrongUser/wrongPass)")
    login.login_data("wrongUser", "wrongPass")
    
    log.step("VERIFY", "Waiting for error message to appear")
    error = page.locator(".oxd-alert-content-text")
    error.wait_for(state="visible")
    
    log.step("VERIFY", "Checking if error message is visible")
    assert error.is_visible(), "Error message should be visible for invalid credentials"
    
    log.result("PASS", "Error message displayed correctly on invalid login")
    log.info("=" * 50)