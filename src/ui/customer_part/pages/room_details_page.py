from src.ui.common.base_page import BasePage
from src.ui.customer_part.components.booking import BookingDetailsComponent


class RoomDetailsPage(BasePage):
    url_part = "reservation"

    def __init__(self, page, room_id, date_from, date_to):
        super().__init__(page)
        self.url_part = f"{self.url_part}/{room_id}?checkin={date_from}&checkout={date_to}"

        self.booking_details = BookingDetailsComponent(self.page)
