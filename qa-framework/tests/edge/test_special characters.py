from pages_blueprint.login_page import LoginPage
import pytest
@pytest.mark.edge
@pytest.mark.order(2)
@pytest.mark.p2
def test_login_special_characters(page):
    login = LoginPage(page)

    login.open()
    login.login_data("@@@###", "!!!$$$")

    error = page.locator(".oxd-alert-content-text")
    error.wait_for(state="visible")
    assert error.is_visible()