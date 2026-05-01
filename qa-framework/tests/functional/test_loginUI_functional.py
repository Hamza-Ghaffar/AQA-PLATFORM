from pages_blueprint.login_page import LoginPage
import pytest

@pytest.mark.functional
@pytest.mark.order(2)
@pytest.mark.p1
def test_login_ui_elements(page):
    login = LoginPage(page)

    login.open()
    page.wait_for_selector("input[name='username']")
    assert login.username.is_visible()
    assert login.password.is_visible()
    assert login.login_btn.is_visible()