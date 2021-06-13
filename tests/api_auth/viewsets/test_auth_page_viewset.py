from django.urls import reverse_lazy

from rest_framework import status
from rest_framework.test import APITestCase

from miq.models import Page
from miq.models.section import Section

from miq.tests.mixins import UserMixin, SiteMixin

list_path = reverse_lazy('miq:page-list')


class Mixin(SiteMixin, UserMixin):
    def get_detail_path(self, slug):
        return reverse_lazy('miq:page-detail', args=[slug])


class TestPageViewset(Mixin, APITestCase):
    def setUp(self) -> None:
        super().setUp()

        self.get_user()
        self.client.login(
            username=self.username,
            password=self.password)

    def test_on_slug_update(self):
        # All section slugs should update as well
        pass

    def test_on_section_add(self):
        slug = Page.objects.create(
            label='Section test page', site=self.site).slug
        path = reverse_lazy('miq:page-section', args=[slug])

        # No slug
        r = self.client.post(path, data={}, format='json')
        # Adds text section
        # self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        # Add section
        r = self.client.post(path, data={'type': "MD"}, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        # self.assertIn(f'{section_slug}', r.data.get('sections'))

        # update_sections_source
        # section = Page.objects.get(slug=slug).sections.get(slug=section_slug)
        # self.assertEqual(section.source, f'{slug}')

        # Retriev page sections
        section_list_path = reverse_lazy('miq:section-list')
        r = self.client.get(section_list_path, {'source': slug})
        self.assertEqual(r.data.get('count'), 2)

    def test_sections_is_readonly(self):
        slug = Page.objects.create(
            label='Section test page', site=self.site).slug
        path = self.get_detail_path(slug)

        section = Section.objects.create(site=self.site)

        r = self.client.patch(
            path, data={'sections': [section.slug]}, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data.get('sections')), 0)

    def test_partial_update(self):
        slug = Page.objects.create(label='Old label', site=self.site).slug
        path = self.get_detail_path(slug)

        label = 'New label'
        r = self.client.patch(
            path, data={'label': label}, format='json')

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        page = Page.objects.draft().get(slug=slug)
        self.assertEqual(page.label, label)

        r = self.client.patch(
            path, data={'is_published': True}, format='json')
        self.assertTrue(Page.objects.published().get(slug=slug).is_published)

    def test_create(self):
        r = self.client.post(list_path, data={}, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        r = self.client.post(
            list_path, data={'label': 'page label'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        self.assertFalse(r.data.get('is_published'))

    def test_list(self):
        Page.objects.create(label='Page', site=self.site)
        r = self.client.get(list_path)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data.get('results')), 1)

    def test_user_not_auth(self):
        self.client.logout()

        r = self.client.get(list_path)
        # self.assertEqual(r.status_code, 403)
        self.assertEqual(r.status_code, status.HTTP_302_FOUND)
