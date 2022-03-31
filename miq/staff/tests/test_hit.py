
from django.test import TestCase

from rest_framework import status

from miqanalytics.models import Hit


class TestHitModel(TestCase):

    def test_create_hit(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        qs = Hit.objects.filter(session=self.client.session.session_key)

        self.assertGreater(qs.count(), 0)

        hit = qs.first()
        self.assertEqual(hit.method, 'GET')
        self.assertEqual(hit.response_status, status.HTTP_200_OK)

        for i in range(1000):
            self.client.get(f'/?i={i}')

        hit = Hit.objects.last()
        self.assertIn('?i=999', hit.path)
        self.assertGreater(Hit.objects.filter(session=hit.session).count(), 1000)

        self.client.get('/does-not-exist/')
        hit = Hit.objects.last()
        self.assertEqual(hit.response_status, status.HTTP_404_NOT_FOUND)

        self.assertEqual(hit.session, Hit.objects.last().session)

        r = self.client.post('/', data={})
        hit = Hit.objects.last()
        self.assertEqual(hit.method, 'POST')
        self.assertEqual(hit.response_status, status.HTTP_200_OK)
