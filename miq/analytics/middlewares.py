from django.utils.functional import SimpleLazyObject
from django.contrib.sites.middleware import CurrentSiteMiddleware

from .utils import create_hit, create_visitor

from ..honeypot.utils import is_threat


def get_visitor(request):
    if not hasattr(request, '_cached_visitor'):
        request._cached_visitor = create_visitor(request)
    return request._cached_visitor


class AnalyticsMiddleware(CurrentSiteMiddleware):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request.is_threat = is_threat(request)
        request.visitor = SimpleLazyObject(lambda: get_visitor(request))

        response = self.get_response(request)

        if '/media/' in request.path:
            return response

        try:
            create_hit(request, response)
        except Exception as e:
            print('\n\nError creating hit', e, '\n\n')

        return response
