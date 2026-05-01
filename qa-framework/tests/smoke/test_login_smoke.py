from pages_blueprint.login_page import LoginPage
from pages_blueprint.dashboard_page import DashboardPage
from utils.logger import TestLogger
import pytest

log = TestLogger(__name__)

@pytest.mark.smoke
@pytest.mark.p0
def test_smoke_valid_login(page):
    """
    Smoke test: Verify valid user can login successfully.
    
    Level 2 Reporting Features:
    - Step-by-step logging
    - Error capture
    - Result tracking
    """
    log.info("=" * 50)
    log.info("TEST: Smoke - Valid Login")
    log.info("=" * 50)
    
    login = LoginPage(page)
    dashboard = DashboardPage(page)

    # ARRANGE
    log.step("SETUP", "Initializing login and dashboard page objects")
    
    # ACT
    log.step("NAVIGATE", "Opening login page")
    login.open()
    
    log.step("LOGIN", "Entering credentials: username=Admin, password=admin123")
    login.login_data("Admin", "admin123")
    
    # ASSERT
    log.step("VERIFY", "Checking if dashboard is loaded")
    is_dashboard_loaded = dashboard.is_loaded()
    
    if is_dashboard_loaded:
        log.result("PASS", "Dashboard loaded successfully after login")
        assert is_dashboard_loaded
    else:
        log.result("FAIL", "Dashboard failed to load after login")
        assert is_dashboard_loaded, "Dashboard should be loaded after successful login"