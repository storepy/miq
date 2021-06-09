from django.test import TestCase
from django.urls import reverse_lazy

from miq.models import Page
from miq.tests.mixins import TestMixin

path = reverse_lazy('miq:index')


class Mixin(TestMixin):
    pass


class TestIndexView(Mixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.site.save()

    def test_context(self):
        r = self.client.get(path)
        self.assertEqual(r.context.get('title'), 'Welcome')
        # print()
