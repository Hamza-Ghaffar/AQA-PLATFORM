from pages_blueprint.login_page import LoginPage
from pages_blueprint.dashboard_page import DashboardPage
import pytest

@pytest.mark.smoke
def test_smoke_valid_login(page):
    login = LoginPage(page)
    dashboard = DashboardPage(page)

    # ARRANGE + ACT
    login.open()
    login.login_data("Admin", "admin123")
    assert dashboard.is_loaded()