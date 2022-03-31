import shutil
from django.urls import reverse_lazy
from django.test import override_settings

from rest_framework import status
from rest_framework.test import APITestCase

from miq.models import Image
from miq.tests.utils import get_temp_img

from miq.tests.mixins import TestMixin

TEST_MEDIA_DIR = 'test_media'
list_path = reverse_lazy('miq:image-list')

print(list_path)


class Mixin(TestMixin):
    pass


@override_settings(MEDIA_ROOT=(TEST_MEDIA_DIR))
class TestImageViewset(Mixin, APITestCase):
    def setUp(self) -> None:
        super().setUp()

        self.get_user()
        self.is_logged_in = self.client.login(
            username=self.username,
            password=self.password)

    def tearDown(self):
        try:
            shutil.rmtree(TEST_MEDIA_DIR)
        except Exception:
            pass

    def test_create(self):
        # TODO: Require site slug on create
        self.assertTrue(self.is_logged_in)

        r = self.client.post(
            list_path, data={'src': get_temp_img()},
            format='multipart'
        )
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        slug = r.data.get('slug')
        image = Image.objects.get(slug=slug)

        self.assertEqual(image.site, self.site)
        self.assertEqual(image.user.username, self.username)

        # thumbnails
        # self.assertEqual(image.thumbnails.count(), 1)

    # test_src_required

    def test_list(self):
        r = self.client.get(list_path)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_user_not_auth(self):
        self.client.logout()
        r = self.client.get(list_path)

        # Redirect
        self.assertEqual(r.status_code, status.HTTP_302_FOUND)
