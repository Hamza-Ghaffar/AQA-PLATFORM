class DashboardPage:
    def __init__(self, page):
        self.page = page

    def is_loaded(self):
        return "dashboard" in self.page.url.lower()