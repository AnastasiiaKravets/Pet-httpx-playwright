from config import settings


class PlaywrightManager:

    def __init__(self, playwright):
        self.playwright = playwright

    def create_browser(self):
        browser_type = self._get_browser_type()
        return browser_type.launch(**self._launch_options())

    def create_context(self, browser):
        return browser.new_context(**self._context_options())

    def _get_browser_type(self):
        return getattr(self.playwright, settings.BROWSER)

    @staticmethod
    def _launch_options() -> dict:
        return {
            "headless": settings.HEADLESS,
            "slow_mo": settings.SLOW_MO,
        }

    def _context_options(self) -> dict:
        options = {
            "base_url": settings.BASE_UI_URL,
            # "ignore_https_errors": False,
            # "viewport": {
            #     "width": settings.viewport_width,
            #     "height": settings.viewport_height,
            # },
            # "locale": settings.locale,
        }

        if settings.DEVICE:
            device = self.playwright.devices[settings.DEVICE]
            options.update({**device})

        return options
