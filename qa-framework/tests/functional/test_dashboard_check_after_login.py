from pages_blueprint.login_page import LoginPage
from pages_blueprint.dashboard_page import DashboardPage
import pytest
@pytest.mark.functional
@pytest.mark.order(1)
@pytest.mark.p1
def test_dashboard_after_login(page):
    login = LoginPage(page)
    dashboard = DashboardPage(page)

    login.open()
    login.login_data("Admin", "admin123")
    assert dashboard.is_loaded()