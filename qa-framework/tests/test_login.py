from pages_blueprint.login_page import LoginPage
from pages_blueprint.dashboard_page import DashboardPage

def test_valid_login(page):
    login = LoginPage(page)
    dashboard = DashboardPage(page)

    login.open("https://opensource-demo.orangehrmlive.com")
    login.login_data("Admin", "admin123")

    assert dashboard.is_loaded()