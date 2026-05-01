class DashboardPage:
    def __init__(self, page):
        self.page = page

    def is_loaded(self):
        # Wait for the dashboard breadcrumb/header to be visible, then check
        locator = self.page.locator(".oxd-topbar-header-breadcrumb")
        try:
            locator.wait_for(state="visible", timeout=5000)
            return locator.is_visible()
        except Exception:
            return False
    
    
