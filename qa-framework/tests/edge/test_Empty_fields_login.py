from pages_blueprint.login_page import LoginPage
import pytest

@pytest.mark.edge
@pytest.mark.p2
@pytest.mark.order(1)
def test_login_empty_fields(page):

    login = LoginPage(page)

    login.open()
    login.login_data("", "")

    required_msg = page.locator("text=Required")
    required_msg.first.wait_for(state="visible")

    # ✔ this assertion is TRUE (UI works)
    assert required_msg.first.is_visible()

    # ❌ FORCE FAILURE to trigger screenshot hook
    assert False, "FORCED FAILURE TO TEST SCREENSHOT HOOK"