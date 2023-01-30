import shutil

from django.test import override_settings
from django.test import TransactionTestCase

from miq.core.models import Image
from miq.core.services import user_create
from miq.tests.utils import get_temp_img, get_random_user_data, get_or_create_site

TEST_MEDIA_DIR = 'test_media'


class Mixin:

    def tearDown(self):
        try:
            shutil.rmtree(TEST_MEDIA_DIR)
        except Exception:
            pass


@override_settings(MEDIA_ROOT=(TEST_MEDIA_DIR))
class TestCoreImageModel(Mixin, TransactionTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.site = get_or_create_site()

    # @classmethod
    # def setUpTestData(cls):
    # def tearDownClass(cls):


    def _test_user_manager(self):
        user = user_create(**get_random_user_data())

        Image.objects.create(user=user, site=self.site, src=get_temp_img())

        user2 = user_create(**get_random_user_data())
        Image.objects.create(user=user2, site=self.site, src=get_temp_img())
        Image.objects.create(user=user2, site=self.site, src=get_temp_img())
        self.assertEqual(Image.objects.user(user2).count(), 2)

    def test_create(self):
        img = Image.objects.create(
            user=user_create(**get_random_user_data()),
            site=self.site,src=get_temp_img()
        )
        self.assertEqual(img.src.name, f'{img}')
