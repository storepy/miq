
from django.contrib.sites.models import Site

from django.test import TransactionTestCase


from miq.models import Page
from miq.tests.mixins import TestMixin


class Mixin(TestMixin):
    pass


class TestPageModel(Mixin, TransactionTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_create(self):
        self.assertIsNotNone(self.site)
        page = Page.objects.create(site=self.site, label="label")

        self.assertEqual(f'{page}', 'example.com label page')
        self.assertIsNone(page.detail_url)

        self.assertIsNone(page.dt_published)
        page.publish()
        self.assertTrue(page.is_published)
        self.assertIsNotNone(page.dt_published)

        Page.objects.create(site=self.site)
        self.assertEqual(Page.objects.count(), 2)
        self.assertEqual(Page.objects.draft().count(), 1)
        self.assertEqual(Page.objects.published().count(), 1)
