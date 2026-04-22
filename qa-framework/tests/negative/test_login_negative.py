from pages_blueprint.login_page import LoginPage
import pytest
@pytest.mark.negative
def test_invalid_login(page):
    login = LoginPage(page)

    login.open()
    login.login_data("wrongUser", "wrongPass")
    error = page.locator(".oxd-alert-content-text")
    error.wait_for(state="visible")
    assert error.is_visible()