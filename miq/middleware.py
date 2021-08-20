from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.middleware import CurrentSiteMiddleware
from django.contrib.sites.shortcuts import get_current_site


class SiteMiddleware(CurrentSiteMiddleware):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # try:
        #     create_hit(request, response)

        # except Exception as e:
        #     print('\n\n==>', e, '\n\n')

        return response

    def process_request(self, request):
        request.site = get_current_site(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    def process_template_response(self, request, response):

        # DRF DATA
        # self.process_drf_response(request, response)

        # DJANGO CONTEXT DATA
        self.process_response_context_data(request, response)

        return response

    def process_drf_response(self, request, response):
        if not hasattr(response, 'data') or not response.data:
            return

    def process_response_context_data(self, request, response):
        ctx = response.context_data
        if not ctx:
            return response

        site = get_current_site(request)
        if not site:
            return response

        ctx['is_live'] = False

        site = Site.objects.filter(id=site.id).first()
        ctx['site'] = site

        if 'sharedData' not in ctx.keys():
            ctx['sharedData'] = {}

        # sD = ctx.get('sharedData')
        # sD['site'] = SiteSerializer(
        #     site, context={'request': request}, read_only=True).data

        # settings = Setting.objects.filter(site=site).first()
        # if settings:
        #     is_live = settings.is_live
        #     ctx['settings'] = settings
        #     ctx['is_live'] = is_live

        #     # TODO: '/login' path
        #     if not is_live and not request.user.is_authenticated:
        #         del ctx['sharedData']

        #     if settings.ga_tracking:
        #         ctx['ga_tracking'] = settings.ga_tracking.strip()

        return response


class CORSMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        self.process_response(request, response)

        # from pprint import pprint
        # pprint(request.headers.__dict__)

        return response

    def process_response(self, request, response):
        response["Access-Control-Allow-Origin"] = settings.CORS_ORIGIN
        response["Access-Control-Allow-Headers"] = "X-CSRFTOKEN, x-requested-with, Content-Type, Accept, Origin"
        response["Access-Control-Allow-Methods"] = "OPTIONS, GET, POST, PUT, DELETE, PATCH"
        response["Access-Control-Max-Age"] = 86400
        response["Access-Control-Allow-Credentials"] = 'true'
