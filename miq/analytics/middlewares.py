
from django.contrib.sites.middleware import CurrentSiteMiddleware

from .utils import create_hit


class AnalyticsMiddleware(CurrentSiteMiddleware):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        try:
            create_hit(request, response)
        except Exception as e:
            print('\n\nError creating hit', e, '\n\n')

        return response
