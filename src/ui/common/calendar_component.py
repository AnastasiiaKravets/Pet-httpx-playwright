from playwright.sync_api import Locator, Page

from src.ui.common.base_component import BaseComponent


class CalendarComponent(BaseComponent):
    def __init__(self, page: Page):
        component_locator = page.locator("div.rbc-calendar")
        super().__init__(component_locator)

        self.toolbar = self.page.locator(".rbc-toolbar")
        self.today_button = self.toolbar.get_by_role("button", name="Today")
        self.back_button = self.toolbar.get_by_role("button", name="Back")
        self.next_button = self.toolbar.get_by_role("button", name="Next")
        self.current_month_label = self.toolbar.locator(".rbc-toolbar-label")

        self.date_cells = self.page.locator(".rbc-date-cell:not(.rbc-off-range)")
        self.selected_events = self.page.locator(".rbc-event-content[title='Selected']")

    def date(self, day: int) -> Locator:
        return self.date_cells.get_by_role("button", name=f"{day:02d}")

    def select_range(self, day_from: int, day_to: int) -> None:
        start = self.date(day_from)
        end = self.date(day_to)

        start_box = start.bounding_box()
        end_box = end.bounding_box()

        if start_box is None or end_box is None:
            raise AssertionError("Unable to determine coordinates for the selected calendar dates.")

        self.page.page.mouse.move(
            start_box["x"] + start_box["width"] / 2,
            start_box["y"] + start_box["height"] / 2,
        )

        self.page.page.mouse.down()

        self.page.page.mouse.move(
            end_box["x"] + end_box["width"] / 2,
            end_box["y"] + end_box["height"] / 2,
            steps=15,
        )

        self.page.page.mouse.up()

    def get_selected_days(self, title="Selected") -> list[int]:
        """
        Returns all selected days of the current month.

        Example:
            [14, 15, 16, 17]
        """
        selected_days = []

        month_rows = self.page.locator(".rbc-month-row")

        for row_index in range(month_rows.count()):
            row = month_rows.nth(row_index)

            event = row.locator(f".rbc-event-content[title*='{title}']")

            if event.count() == 0:
                continue

            event_box = event.bounding_box()
            if event_box is None:
                continue

            event_left = event_box["x"]
            event_right = event_left + event_box["width"]

            date_cells = row.locator(".rbc-date-cell:not(.rbc-off-range)")

            for cell_index in range(date_cells.count()):
                cell = date_cells.nth(cell_index)

                cell_box = cell.bounding_box()
                if cell_box is None:
                    continue

                cell_center = cell_box["x"] + cell_box["width"] / 2

                if event_left <= cell_center <= event_right:
                    day = int(cell.locator("button").inner_text())
                    selected_days.append(day)

        return selected_days
