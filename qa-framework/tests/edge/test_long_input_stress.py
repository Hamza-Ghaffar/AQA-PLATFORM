from pages_blueprint.login_page import LoginPage
import pytest
@pytest.mark.edge
def test_login_long_input(page):
    login = LoginPage(page)

    long_text = "A" * 300

    login.open()
    login.login_data(long_text, long_text)

    error = page.locator(".oxd-alert-content-text")
    error.wait_for(state="visible")
    assert error.is_visible()