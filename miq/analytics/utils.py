
# from pprint import pprint
import logging
import datetime
from urllib.parse import urlparse, parse_qs
from user_agents import parse as _parse_

from django.conf import settings
from django.utils import timezone

from ..core.utils import get_ip

from .models import Hit, Visitor

# #  whatsapp

logger = logging.getLogger(__name__)
loginfo = logger.info
logerr = logger.error

exclude = ['/media/', '/favicon.ico', '/beat/', '/jsi18n/', ]

# SESSION APP KEYS

QUERY_CACHE_KEY = '_cqk'
CUSTOMER_SESSION_KEY = getattr(settings, 'CUSTOMER_SESSION_KEY', '_cus')
CART_SESSION_KEY = getattr(settings, 'CART_SESSION_KEY', '_cart')


bots = [
    'bot', 'facebookexternalua', 'python', 'aiohttp', 'scrapy',
    'insomnia', 'expanse', 'linkwalker',
]


def create_visitor(request, *, is_bot=False, ** kwargs):

    def set_user(visitor):
        if visitor and not visitor.user and request.user.is_authenticated:
            visitor.user = request.user
            visitor.save()

    visitor = None
    user = request.user if request.user.is_authenticated else None

    _vis = request.COOKIES.get('_vis', None)
    if _vis and (vis := Visitor.objects.filter(slug=_vis)).exists():
        visitor = vis.order_by('created').first()
        set_user(visitor)
        return visitor

    ua = request.META.get('HTTP_USER_AGENT')
    filter = {'ip': get_ip(request), 'user_agent': ua}

    visitor = Visitor.objects.filter(**filter)
    if not visitor.exists():
        visitor = Visitor.objects.create(
            **filter, user=user,
            is_bot=is_bot or get_hit_is_bot(ua, path=request.path)
        )
        loginfo(f'created visitor: {visitor}')
        return visitor

    visitor = visitor.order_by('created').first()
    set_user(visitor)
    return visitor


def get_hit_is_bot(user_agent, *, path=None):
    if 'robots.txt' in path or not isinstance(user_agent, str):
        return True

    is_bot = _parse_(user_agent).is_bot or False
    if not is_bot:
        for match in bots:
            if match in user_agent.lower():
                is_bot = True
                break

    return is_bot


def parse_ua(user_agent: str):
    if not user_agent:
        return {}

    ua = _parse_(user_agent)

    return {
        'os': ua.os.family,
        'browser': ua.browser.family,
        'device': ua.device.family,
        'device_brand': ua.device.brand,
        'device_model': ua.device.model,
        'is_mobile': ua.is_mobile,
        'is_pc': ua.is_pc,
        'is_tablet': ua.is_tablet,
        'is_email_client': ua.is_email_client,
    }


def parse_hit_data(url, referrer, user_agent, session_data):
    assert url
    assert isinstance(session_data, dict), logerr('Session data must be a dict')

    parsed = {}
    data = {**session_data}
    parsed.update(data.pop('query', {}))

    if (ref := referrer) and (from_ref := urlparse(ref).netloc) and from_ref not in url:
        parsed['from_ref'] = from_ref

    for url in [referrer, url]:
        parsed.update(parse_qs(urlparse(url).query, keep_blank_values=True))

    parsed = {key: ','.join(value) if type(value) is list else value for key, value in parsed.items()}

    if isinstance(user_agent, str) and (ua_data := parse_ua(user_agent)):
        parsed.update(ua_data)

    return parsed


def parse_hit(hit):
    hit.parsed_data = parse_hit_data(hit.url, hit.referrer, hit.user_agent, hit.session_data)
    hit.is_parsed = True

    if not hit.is_bot:
        hit.is_bot = get_hit_is_bot(hit.user_agent, path=hit.path)

    hit.save()
    loginfo(f'parsed hit: {hit}')


def parse_hits():
    hits = Hit.objects.filter(is_parsed=False)
    for hit in hits:
        parse_hit(hit)

    loginfo(f'parsed {hits.count()} hits')


def create_hit(request, response, /, source: str = None, ** kwargs) -> Hit:
    if skip_hit(request):
        return

    data = get_hit_data(request, response)

    # CART

    if cart := request.session.get(CART_SESSION_KEY):
        data['session_data'][CART_SESSION_KEY] = cart

    # CUSTOMER

    if cus := request.session.get(CUSTOMER_SESSION_KEY):
        data['session_data'][CUSTOMER_SESSION_KEY] = cus

    source = source or request.session.get('source')

    ctx = getattr(response, 'context_data', None) or {}
    obj = ctx.get('object', None)

    if obj:
        if (hit_data := obj.get_hit_data()) and (isinstance(hit_data, dict)):
            data['app'] = hit_data.pop('app', None)
            data['model'] = hit_data.pop('model', None)
            data['session_data'].update(hit_data)

        if not source:
            source = f'{obj.slug}'

    if not source and request.user.is_authenticated:
        source = f'{request.user.slug}'
        _d = request.user.get_hit_data()
        data.update({'app': _d.pop('app', None), 'model': _d.pop('model', None)})
        data['session_data'].update({**_d, 'username': request.user.username})

    if source:
        data.update({'source_id': source})

    url = data.get('url')

    if query := get_request_query(request, exclude=['r']):
        request.session.update({QUERY_CACHE_KEY: query})
        data['session_data'].update({'query': query})

    last = Hit.objects.filter(
        ip=data.get('ip'), session=data.get('session'), url=url, path=data.get('path'),
        method=data.get('method'), site_id=data.get('site_id'), response_status=data.get('status'),
        created__gt=timezone.now() - datetime.timedelta(minutes=1),
    )

    visitor = request.visitor
    if last.exists() and (hit := last.order_by('-created').first()):
        # hit.count += 1
        hit.session_data = {**hit.session_data, **data}
        if not hit.visitor:
            hit.visitor = visitor

        hit.save()
        loginfo(f'updated hit: {hit.slug}')
    else:
        hit = Hit.objects.create(**{
            **data,
            'visitor': visitor,
            'parsed_data': parse_hit_data(url, data.get('referrer'), data.get('user_agent'), data.get('session_data', {})),
            'is_parsed': True,
            'is_bot': visitor.is_bot,
        })
        loginfo(f'new hit: {hit.slug}')

    return hit


def get_request_query(request, *, exclude: list = None):
    cached_query = {key: value for key, value in request.session.get(QUERY_CACHE_KEY, {}).items()}

    query = {**cached_query, **parse_qs(urlparse(get_request_url(request)).query)}

    _exclude = [key for key in query.keys() if key.startswith('__')]
    if isinstance(exclude, list):
        _exclude.extend(exclude)

        for key in _exclude:
            query.pop(key, None)

    return query


def get_hit_data(request, response, /, source: str = None) -> dict:
    if not request.session.session_key:
        try:
            request.session.save()
            loginfo(f'new session: {request.session.session_key}')
        except Exception as e:
            logerr(f'error creating session\n{e}')
            return

    return {
        'site_id': request.site.id,
        'ip': get_ip(request),
        'session': request.session.session_key,
        'url': get_request_url(request),
        'path': request.path,
        'method': request.method,
        'referrer': request.META.get('HTTP_REFERER'),
        'user_agent': request.META.get('HTTP_USER_AGENT'),
        'response_status': response.status_code,
        'session_data': {},
    }


def get_request_url(request):
    return request.build_absolute_uri() \
        or request.get_full_path_info() \
        or request.get_full_path() \
        or request.path_info \
        or request.path


def skip_hit(request):

    if request.method == 'OPTIONS':
        logger.debug('skip option hit creation')
        return True

    for match in exclude:
        if match in request.path:
            logger.debug(f'skip match: {match} hit creation')
            return True

    return False
