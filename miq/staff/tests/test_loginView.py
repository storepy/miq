from selenium import webdriver

from django.urls import reverse_lazy
from django.test import LiveServerTestCase


from miq.tests.mixins import TestMixin

from miq.tests.selenium import BasePage


class LoginPageMixin(BasePage):
    login_path = reverse_lazy('staff:login')


class LoginPage(LoginPageMixin):
    def get(self):
        return LoginPage(self.driver.get(f'{self.domain}{self.login_path}'))


class Mixin(TestMixin):
    pass


class TestStaffLogin(Mixin, LiveServerTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.domain = self.live_server_url

    # def test_login_success(self):
        # self.get_user()
        # with webdriver.Chrome() as driver:
        # page = LoginPage(driver).get()
        # print(page)
        # page.screenshot()
        # act_page = page.login(self.username, self.password)

        # assert 'AccountView' in act_page.driver.page_source
        # assert 'UserNav' in act_page.driver.page_source
