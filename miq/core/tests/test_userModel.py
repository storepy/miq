
from django.test import TransactionTestCase

from miq.core.tests.utils import UserMixin


class TestCoreUser(UserMixin, TransactionTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_create(self):
        usr = 'usr'
        user = self.create_user(usr, 'pwd')
        self.assertEqual(usr, f'{user}')
