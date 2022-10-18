
from django.contrib.sites.middleware import CurrentSiteMiddleware

from .utils import create_hit

from ..honeypot.utils import is_threat


class AnalyticsMiddleware(CurrentSiteMiddleware):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if '/media/' in request.path:
            return response

        try:
            create_hit(request, response, is_threat=is_threat(request))
        except Exception as e:
            print('\n\nError creating hit', e, '\n\n')

        return response
