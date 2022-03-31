from django.test import LiveServerTestCase
from selenium import webdriver

from miq.core.tests.mixins import TestMixin

driver_path = '../../../../../chromedriver'
driver_path = '/Users/marqetintl/Dropbox/MIQ/projetcs/py/chromedriver'


class Mixin(TestMixin):
    pass


class TestLogin(Mixin, LiveServerTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.domain = self.live_server_url

    def test_login_success(self):
        # self.get_user()
        with webdriver.Chrome(driver_path) as driver:
            # url = self.domain + self.login_path
            url = self.domain
            driver.get(url)
            # page = LoginPage(driver).get(url)
            # act_page = page.login(self.username, self.password)

            # assert 'AccountView' in act_page.driver.page_source
            # assert 'UserNav' in act_page.driver.page_source
