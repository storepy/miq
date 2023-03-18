
from django.utils.functional import SimpleLazyObject
from django.contrib.sites.middleware import CurrentSiteMiddleware

from .utils import create_hit, create_visitor, get_hit_data
from .utils.fb import get_fb_params

from ..honeypot.utils import is_threat


def get_visitor(request):
    if not hasattr(request, '_cached_visitor'):
        request._cached_visitor = create_visitor(request)
    return request._cached_visitor


class AnalyticsMiddleware(CurrentSiteMiddleware):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        cookies = request.COOKIES
        _vis = cookies.get('_vis')

        request.is_threat = is_threat(request)

        visitor = SimpleLazyObject(lambda: get_visitor(request))
        request.visitor = visitor

        response = self.get_response(request)

        if '/media/' in request.path:
            return response

        if not _vis:
            response.set_cookie('_vis', f'{visitor.slug}')

        try:
            create_hit(request, response)
        except Exception as e:
            print('\n\nError creating hit', e, '\n\n')

        # print_request(request, response)

        return response


def print_request(request, response):
    print('\n\n=>fbparams', get_fb_params(request, response=response))

    data = get_hit_data(request, response)
    print('=>url', data.get('url'))
    print('=>ip', data.get('ip'))
    print('=>session', data.get('session'))
    print('=>referrer', data.get('referrer'))
    print('=>user_agent', data.get('user_agent'))
    print()
