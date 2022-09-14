

from django.test import TestCase, RequestFactory
from django.urls import reverse_lazy

from rest_framework import status


from miq.analytics.models import Hit
from miq.analytics.middlewares import AnalyticsMiddleware
from miq.core.tests.utils import TestMixin

indexpath = reverse_lazy('index')


class Mixin(TestMixin):
    pass


class TestHitModel(Mixin, TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.site.save()

    def test_create_hit(self):
        headers = dict(
            HTTP_USER_AGENT='test',
            HTTP_REFERER='http://example.com'
        )
        r = self.client.get(indexpath, **headers)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        hit = Hit.objects.order_by('created').last()
        self.assertEqual(hit.response_status, status.HTTP_200_OK)
        self.assertEqual(hit.method, 'GET')
        self.assertEqual(hit.user_agent, headers['HTTP_USER_AGENT'])
        self.assertEqual(hit.referrer, headers['HTTP_REFERER'])
        self.assertEqual(hit.parsed_data['from_ref'], 'example.com')

        last_path = None
        session_key = self.client.session.session_key

        for i in range(20):
            last_path = f'{indexpath}?i={i}'
            self.client.get(last_path)
            self.assertEquals(self.client.session.session_key, session_key)

        hit = Hit.objects.order_by('created').last()
        self.assertNotIn('?i=999', hit.path)
        self.assertIn('?i=999', last_path)
        self.assertIn('?i=999', hit.url)
        self.assertGreater(Hit.objects.filter(session=hit.session).count(), 20)

        self.client.get('/does-not-exist/')
        hit = Hit.objects.order_by('created').last()
        self.assertEqual(hit.response_status, status.HTTP_404_NOT_FOUND)

        r = self.client.post(indexpath, data={})
        hit = Hit.objects.order_by('created').last()
        self.assertEqual(hit.method, 'POST')
        self.assertEqual(hit.response_status, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_middleware(self):
        headers = dict(
            HTTP_USER_AGENT='test',
            HTTP_REFERER='http://example.com')

        request = RequestFactory().get(indexpath, **headers)
        request.session = self.client.session
        # request.site = self.site
        # request.user = self.user

        response = AnalyticsMiddleware(lambda x: x).process_request(request)
        self.assertIsNone(response)
