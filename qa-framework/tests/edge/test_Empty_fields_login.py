from pages_blueprint.login_page import LoginPage
import pytest
@pytest.mark.edge
def test_login_empty_fields(page):
    login = LoginPage(page)

    login.open()
    login.login_data("", "")

    required_msg = page.locator("text=Required")
    required_msg.first.wait_for(state="visible")
    assert required_msg.first.is_visible()