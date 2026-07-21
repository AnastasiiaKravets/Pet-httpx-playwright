from src.ui.admin_part.components.header import HeaderComponent
from src.ui.common.base_page import BasePage


class LoginPage(BasePage):
    url_part = 'admin'

    def __init__(self, page):
        super().__init__(page)
        self.header = HeaderComponent(page)

        self.username_input = self.page.get_by_role('textbox', name='username')
        self.password_input = self.page.get_by_role('textbox', name='password')
        self.submit_button = self.page.get_by_role('button', name='login')

    def login(self, user_data):
        self.username_input.fill(user_data['username'])
        self.password_input.fill(user_data['password'])
        self.submit_button.click()
        return self

