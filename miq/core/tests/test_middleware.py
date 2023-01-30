from django.test import TestCase, LiveServerTestCase


from miq.tests.utils import get_or_create_site


class TestCoreMiddleware(LiveServerTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.site = get_or_create_site(is_live=True)


    def test_context_is_live(self):
        self.assertTrue(self.site.settings.is_live)

        r = self.client.get(self.live_server_url)
        ctx = r.context

        self.assertTrue(ctx['is_live'])
        self.assertTrue(ctx['display_live'])


class TestCoreMiddlewareIsNotLive(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.site = get_or_create_site()

    def test_context_is_not_live(self):
        self.assertFalse(self.site.settings.is_live)

        r = self.client.get('/')
        ctx = r.context

        self.assertFalse(ctx['is_live'])
        self.assertFalse(ctx['display_live'])
        self.assertEqual(ctx['title'], 'Welcome')

        shared_data = ctx['sharedData']

        assert 'view_mode' in shared_data

        assert shared_data['site'] is not None

        assert 'name' in shared_data.get('site')
        assert 'domain' in shared_data.get('site')
        
        template = ctx['close_template']
        assert template['html'] is None
        assert template['title'] is None
        assert template['text'] is None


    