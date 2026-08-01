from src.ui.admin_part.components.admin_header import AdminHeaderComponent
from src.ui.common.base_page import BasePage
from src.ui.common.calendar_component import CalendarComponent


class ReportPage(BasePage):
    url_part = 'admin/report'

    def __init__(self, page):
        super().__init__(page)
        self.header = AdminHeaderComponent(page)
        self.calendar = CalendarComponent(page)
