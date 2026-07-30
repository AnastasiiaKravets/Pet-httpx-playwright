from playwright.sync_api import Locator, expect
from pydantic import BaseModel

from src.ui.admin_part.components.admin_header import AdminHeaderComponent
from src.ui.common.base_page import BasePage


class AdminRoomDetailsPage(BasePage):
    url_part = 'admin/room'

    def __init__(self, page):
        super().__init__(page)
        self.header = AdminHeaderComponent(page)

        self.booking_rows = self.page.locator('div.detail')

    def open(self, room_id):
        self.page.goto(f'{self.url_part}/{room_id}')
        expect(self.loading_text).not_to_be_visible()
        return self

    def _find_row(self, check_in: str, check_out: str) -> Locator:
        """
        Finds booking row by check-in/check-out dates.
        Raises AssertionError if row is not found.
        """
        for i in range(self.booking_rows.count()):
            row = self.booking_rows.nth(i)

            values = row.locator("p").all_inner_texts()

            if values[4] == check_in and values[5] == check_out:
                return row

        raise AssertionError(
            f"Booking with dates {check_in} - {check_out} was not found."
        )

    def get_all_bookings(self) -> list[BookingRow]:
        bookings = []

        for i in range(self.booking_rows.count()):
            values = self.booking_rows.nth(i).locator("p").all_inner_texts()

            bookings.append(
                BookingRow(
                    first_name=values[0],
                    last_name=values[1],
                    price=int(values[2]),
                    deposit_paid=values[3].lower() == "true",
                    check_in=values[4],
                    check_out=values[5],
                )
            )

        return bookings

    def get_booking(self, check_in: str, check_out: str) -> BookingRow:
        row = self._find_row(check_in, check_out)
        values = row.locator("p").all_inner_texts()

        return BookingRow(
            first_name=values[0],
            last_name=values[1],
            price=int(values[2]),
            deposit_paid=values[3].lower() == "true",
            check_in=values[4],
            check_out=values[5],
        )

    def edit_booking(self, check_in: str, check_out: str) -> None:
        row = self._find_row(check_in, check_out)

        row.locator(".bookingEdit").click()

    def delete_booking(self, check_in: str, check_out: str) -> None:
        row = self._find_row(check_in, check_out)

        row.locator(".bookingDelete").click()

    def contains_booking(self, check_in: str, check_out: str) -> bool:
        for booking in self.get_all_bookings():
            if (
                    booking.check_in == check_in
                    and booking.check_out == check_out
            ):
                return True

        return False

    def wait_at_least_one_booking(self, timeout: int = 1000) -> None:
        expect(self.booking_rows.first).to_be_visible(timeout=timeout), "There are no booking rows"


class BookingRow(BaseModel):
    first_name: str
    last_name: str
    price: int
    deposit_paid: bool
    check_in: str
    check_out: str
