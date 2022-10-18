import os
import requests
from selenium import webdriver

from django.urls import reverse_lazy
from django.test import LiveServerTestCase


from miq.core.tests.utils import TestMixin

from miq.tests.selenium import BasePage


dirname = os.path.dirname(__file__)
driver_path = os.path.join(dirname, '../../../../chromedriver')
driver_path = '/Users/marqetintl/Dropbox/MIQ/projects/chromedriver'


class LoginPageMixin(BasePage):
    login_path = reverse_lazy('staff:login')


class LoginPage(LoginPageMixin):
    def get(self):
        return LoginPage(self.driver.get(f'{self.domain}{self.login_path}'))


class Mixin(TestMixin):
    pass


class TestStaffLogin(Mixin, LiveServerTestCase):
    port: int = 8001

    def setUp(self) -> None:
        super().setUp()
        self.site.save()
        self.domain = self.live_server_url
        self.login_path = reverse_lazy('staff:login')

    def test_login_success(self):
        r = requests.get(self.domain)
        self.assertEquals(r.status_code, 200)

        # self.get_user()
        with webdriver.Chrome(driver_path) as driver:
            import time

            time.sleep(60)
            driver.implicitly_wait(3000)

            # driver.get('http://192.168.1.231:8000/staff/login/')
            # driver.get(f'{self.domain}{self.login_path}')
            driver.save_screenshot('screenshot.png')

            # raise Exception(self.login_path)
            # driver.get('https://www.google.com')
            # page = LoginPage(driver).get()
            # print(page)
            # page.screenshot()
        # act_page = page.login(self.username, self.password)

        # assert 'AccountView' in act_page.driver.page_source
        # assert 'UserNav' in act_page.driver.page_source
