def test_login(page):
    page.goto("https://opensource-demo.orangehrmlive.com")

    page.fill("input[name='username']", "Admin")
    page.fill("input[name='password']", "admin123")
    page.click("button[type='submit']")

    assert "dashboard" in page.url.lower()