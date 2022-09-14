from django.test import TestCase
from django.urls import reverse_lazy

from miq.core.tests.utils import TestMixin

path = reverse_lazy('index')


class Mixin(TestMixin):
    pass


class TestCoreIndexView(Mixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.site.save()

    def test_context(self):
        r = self.client.get(path)
        self.assertEqual(r.context.get('title'), 'Welcome')
