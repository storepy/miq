
from django.urls import reverse_lazy

from rest_framework import status
from rest_framework.test import APITestCase

from miq.core.models import Section

from miq.tests.mixins import TestMixin

path = reverse_lazy('miq:index-detail', args=['current'])


class Mixin(TestMixin):
    pass


class TestIndexViewset(Mixin, APITestCase):
    def setUp(self) -> None:
        super().setUp()

        self.site.save()
        self.user = self.create_staffuser(self.username, self.password)
        self.add_user_perm(self.user, 'change_index')

        self.client.login(
            username=self.username,
            password=self.password
        )

    def test_on_section_add(self):
        self.assertTrue(self.user.has_perm('miq.change_index'))
        path = reverse_lazy('miq:index-section', args=['current'])

        # Add section
        r = self.client.post(path, data={}, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        index = self.site.index

        # Retriev page sections
        section_list_path = reverse_lazy('miq:section-list')
        r = self.client.get(section_list_path, {'source': index.slug})
        self.assertEqual(r.data.get('count'), 1)

    def test_sections_is_readonly(self):
        section = Section.objects.create(site=self.site)

        r = self.client.patch(
            path, data={'sections': [section.slug]}, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data.get('sections')), 0)

    def test_index_partial_update(self):
        self.assertTrue(self.user.has_perm('miq.change_index'))

        title = 'Index 1'
        r = self.client.patch(
            path, data={'title': title}, format='json')

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(self.site.index.title, title)


class TestIndexNotAuthUserViewset(Mixin, APITestCase):
    def setUp(self) -> None:
        super().setUp()

        self.get_user()
        self.site.save()
        self.client.login(
            username=self.username,
            password=self.password)

    def test_index_partial_update_no_perm(self):
        self.user.is_staff = True
        self.user.save()

        self.assertFalse(self.user.has_perm('miq.change_index'))

        r = self.client.patch(
            path, data={'title': 'Index 1'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_not_staff(self):
        r = self.client.get(path)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_not_auth(self):
        self.client.logout()

        r = self.client.get(path)
        self.assertEqual(r.status_code, status.HTTP_302_FOUND)
