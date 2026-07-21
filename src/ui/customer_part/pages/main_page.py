from src.ui.common.base_page import BasePage
from src.ui.customer_part.components.footer_component import FooterComponent
from src.ui.customer_part.components.header import HeaderComponent
from src.ui.customer_part.components.rooms import RoomListComponent


class MainPage(BasePage):
    url_part = ''

    def __init__(self, page):
        super().__init__(page)

        self.header = HeaderComponent(self.page)
        self.room_list = RoomListComponent(self.page)
        self.footer = FooterComponent(self.page)

        self.heading = self.page.locator('.hero-content h1')
        self.heading_description = self.page.locator('.hero-content p')
        self.booking_button = self.page.locator('.hero-content').get_by_role('link', name='Book Now')
