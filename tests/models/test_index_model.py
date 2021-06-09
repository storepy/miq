
from django.contrib.sites.models import Site

from django.test import TransactionTestCase


from miq.models import Index
from miq.tests.mixins import TestMixin


class Mixin(TestMixin):
    pass


class TestIndexModel(Mixin, TransactionTestCase):
    def setUp(self) -> None:
        super().setUp()
        # Must save
        self.site.save()

    def test_exists(self):
        self.assertEqual(
            Index.objects.get(site=self.site), self.site.index)
