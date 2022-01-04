from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.middleware import CurrentSiteMiddleware
from django.contrib.sites.shortcuts import get_current_site

from miq.models import SiteSetting


class SiteMiddleware(CurrentSiteMiddleware):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)

        response = self.get_response(request)
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

        # SITE

        site = Site.objects.filter(id=site.id).first()
        ctx['site'] = site

        # SITE SETTING

        settings = SiteSetting.objects.filter(site=site).first()
        if settings:
            ctx['is_live'] = settings.is_live
            ctx['close_template'] = {
                'html': settings.ct_html,
                'title': settings.ct_title,
                'text': settings.ct_text
            }

            if number := settings.contact_number:
                ctx['contact_number'] = number
                ctx['contact_number_display'] = settings.contact_number_display or number
                ctx['contact_number_title'] = settings.contact_number_title or ''

            if email := settings.contact_email:
                ctx['contact_email'] = email

            if link := settings.whatsapp_link:
                ctx['whatsapp_link'] = link
                ctx['whatsapp_link_title'] = settings.whatsapp_link_title or ''

            if ga := settings.ga_tracking:
                ctx['ga_tracking'] = ga.strip()
            if fb := settings.fb_pixel:
                ctx['fb_pixel'] = fb.strip()

        # SHARED DATA

        if 'sharedData' not in ctx.keys():
            ctx['sharedData'] = {}

        sD = ctx.get('sharedData')
        if 'site' not in sD:
            ctx.get('sharedData').update({
                'site': {'name': site.name, 'domain': site.domain}
            })

        # sD['site'] = SiteSerializer(
        #     site, context={'request': request}, read_only=True).data

        # if settings:
        #     is_live = settings.is_live
        #     ctx['settings'] = settings
        #     ctx['is_live'] = is_live

        #     # TODO: '/login' path
        #     if not is_live and not request.user.is_authenticated:
        #         del ctx['sharedData']

        return response


class CORSMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.process_response(response)

        # from pprint import pprint
        # pprint(request.headers.__dict__)

        return response

    def process_response(self, response):
        response["Access-Control-Allow-Origin"] = settings.CORS_ORIGIN
        response["Access-Control-Allow-Headers"] = "X-CSRFTOKEN, x-requested-with, Content-Type, Accept, Origin"
        response["Access-Control-Allow-Methods"] = "OPTIONS, GET, POST, PUT, DELETE, PATCH"
        response["Access-Control-Max-Age"] = 86400
        response["Access-Control-Allow-Credentials"] = 'true'
