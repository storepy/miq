import shutil
from django.test import override_settings
from django.test import TransactionTestCase

from miq.tests.mixins import TestMixin

from miq.models import Image
from miq.tests.utils import get_temp_img

TEST_MEDIA_DIR = 'test_media'


class Mixin(TestMixin):

    def tearDown(self):
        try:
            shutil.rmtree(TEST_MEDIA_DIR)
        except Exception:
            pass


@override_settings(MEDIA_ROOT=(TEST_MEDIA_DIR))
class TestImageModel(Mixin, TransactionTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.get_user()

    def test_user_manager(self):
        Image.objects.create(
            user=self.user,
            site=self.site,
            src=get_temp_img().name
        )
        new_user = self.create_user('new_username', 'new_password')
        Image.objects.create(
            user=new_user,
            site=self.site,
            src=get_temp_img().name
        )
        Image.objects.create(
            user=new_user,
            site=self.site,
            src=get_temp_img().name
        )
        self.assertEqual(Image.objects.user(new_user).count(), 2)

    def test_create(self):
        img = Image.objects.create(
            user=self.user,
            site=self.site,
            src=get_temp_img().name
        )
        self.assertEqual(img.src.name, f'{img}')
