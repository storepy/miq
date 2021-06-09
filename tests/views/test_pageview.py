from django.test import TestCase
from django.urls import reverse_lazy

from miq.models import Page
from miq.tests.mixins import TestMixin


class Mixin(TestMixin):
    def get_detail_path(self, slug):
        return reverse_lazy('miq:page', args=[slug])


class TestPageView(Mixin, TestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_context(self):
        title = 'This is an about page'
        page = Page.objects.create(label='about', title=title, site=self.site)
        page.publish()
        path = self.get_detail_path(page.slug)
        r = self.client.get(path)
        self.assertEqual(r.context.get('title'), title)
        # print()

    def test_published(self):
        page = Page.objects.create(label='about', site=self.site)
        page.publish()
        path = self.get_detail_path(page.slug)
        r = self.client.get(path)
        self.assertEqual(r.status_code, 200)

    # TODO: Pages with source must return 404

    def test_unpublished(self):
        page = Page.objects.create(label='unpublished', site=self.site)
        path = self.get_detail_path(page.slug)
        r = self.client.get(path)
        self.assertEqual(r.status_code, 404)
