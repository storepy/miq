from django.test import TransactionTestCase

from miq.tests.mixins import TestMixin
from miq.models import Section, TextSection, MarkdownSection, ImageSection


class Mixin(TestMixin):
    pass


class TestSectionModel(Mixin, TransactionTestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_create(self):
        section = Section.objects.create(site=self.site)
        self.assertEqual(section.type, 'TXT')
        self.assertEqual(f'{section}', f'{section.pk}-TXT')


class TestImageSectionModel(Mixin, TransactionTestCase):
    def test_create(self):
        self.assertEqual(ImageSection.objects.create(
            site=self.site).type, 'IMG')


class TestMarkdownSectionModel(Mixin, TransactionTestCase):
    def test_create(self):
        self.assertEqual(MarkdownSection.objects.create(
            site=self.site).type, 'MD')


class TestTextSectionModel(Mixin, TransactionTestCase):
    def test_create(self):
        self.assertEqual(TextSection.objects.create(
            site=self.site).type, 'TXT')
