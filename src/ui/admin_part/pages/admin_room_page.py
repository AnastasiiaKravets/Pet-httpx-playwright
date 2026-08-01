from src.ui.admin_part.components.admin_header import AdminHeaderComponent
from src.ui.common.base_page import BasePage


class AdminRoomPage(BasePage):
    url_part = "admin/rooms"

    def __init__(self, page):
        super().__init__(page)
        self.header = AdminHeaderComponent(page)
