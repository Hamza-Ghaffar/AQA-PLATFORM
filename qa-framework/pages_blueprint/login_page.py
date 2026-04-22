class LoginPage:
    def __init__(self, page):
        self.page = page

        self.username = page.locator("input[name='username']")
        self.password = page.locator("input[name='password']")
        self.login_btn = page.locator("button[type='submit']")
        
        

    def open(self, url):
        self.page.goto(url)

    def login_data(self, user, pwd):
        self.username.fill(user)
        self.password.fill(pwd)
        self.login_btn.click()