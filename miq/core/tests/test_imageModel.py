import shutil
from django.test import override_settings
from django.test import TransactionTestCase

from miq.core.models import Image


from miq.core.tests.utils import TestMixin, get_temp_img

TEST_MEDIA_DIR = 'test_media'


class Mixin(TestMixin):

    def tearDown(self):
        try:
            shutil.rmtree(TEST_MEDIA_DIR)
        except Exception:
            pass


@override_settings(MEDIA_ROOT=(TEST_MEDIA_DIR))
class TestCoreImageModel(Mixin, TransactionTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.get_user()

    def test_user_manager(self):
        Image.objects.create(
            user=self.user, site=self.site, src=get_temp_img())

        new_user = self.create_user('new_username', 'new_password')
        Image.objects.create(user=new_user, site=self.site, src=get_temp_img())
        Image.objects.create(user=new_user, site=self.site, src=get_temp_img())
        self.assertEqual(Image.objects.user(new_user).count(), 2)

    def test_create(self):
        img = Image.objects.create(
            user=self.user,
            site=self.site,
            src=get_temp_img()
        )
        self.assertEqual(img.src.name, f'{img}')
