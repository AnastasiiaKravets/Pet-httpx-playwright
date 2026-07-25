from src.ui.admin_part.components.header import HeaderComponent
from src.ui.common.base_page import BasePage
from src.ui.common.calendar_component import CalendarComponent


class ReportPage(BasePage):
    url_part = 'admin/report'

    def __init__(self, page):
        super().__init__(page)
        self.header = HeaderComponent(page)
        self.calendar = CalendarComponent(page)
