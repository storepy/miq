
import logging
import datetime
from urllib.parse import urlparse, parse_qs
from user_agents import parse as _parse_

from django.utils import timezone

from ..core.utils import get_ip

from .models import Hit

# #  whatsapp

logger = logging.getLogger(__name__)
loginfo = logger.info
logerr = logger.error

exclude = ['/media/', '/favicon.ico', ]

# SESSION APP KEYS
cus_key = '_cus'
cart_key = '_cart'
cached_query_key = '_cqk'


flag_paths = [
    '/wp-login', '/wp-admin', '/install.php', '/netcat/', 'atilektcms', 'modx/manager',
    '/cgi-bin/mt/mt-check', '/engine/print', '/shell4.php', '/if.php',
]


def get_hit_is_bot(user_agent, *, path=None):
    if not user_agent:
        return True

    is_bot = _parse_(user_agent).is_bot or False
    if not is_bot:
        bots = [
            'bot', 'facebookexternalua', 'scrapy', 'expanse',
            'python', 'aiohttp', 'linkwalker', 'insomnia',
        ]

        for match in bots:
            if match in user_agent:
                is_bot = True
                break

    if not is_bot and isinstance(path, str) and 'robots.txt' in path:
        for match in flag_paths:
            if match in path:
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
    assert url and referrer and user_agent and session_data
    assert isinstance(session_data, dict), logerr('Session data must be a dict')

    parsed = {}
    data = {**session_data}
    parsed.update(data.pop('query', {}))

    if (ref := referrer) and (from_ref := urlparse(ref).netloc) and from_ref not in url:
        parsed['from_ref'] = from_ref

    for url in [referrer, url]:
        parsed.update(parse_qs(urlparse(url).query, keep_blank_values=True))

    parsed = {key: ','.join(value) if type(value) is list else value for key, value in parsed.items()}

    if ua_data := parse_ua(user_agent):
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


def create_hit(request, response, /, source: str = None) -> Hit:
    if request.method == 'OPTIONS':
        loginfo('skip option hit creation')
        return

    for match in exclude:
        if match in request.path:
            loginfo(f'skip match: {match} hit creation')
            return

    if not request.session.session_key:
        try:
            request.session.save()
            loginfo(f'new session: {request.session.session_key}')
        except Exception as e:
            logerr(f'error creating session\n{e}')
            return

    url = request.build_absolute_uri() \
        or request.get_full_path_info() \
        or request.get_full_path() \
        or request.path_info \
        or request.path

    #
    ip = get_ip(request)
    session = request.session.session_key
    path = request.path
    method = request.method
    site_id = request.site.id
    status = response.status_code
    referrer = request.META.get('HTTP_REFERER')
    user_agent = request.META.get('HTTP_USER_AGENT')

    data = {
        'ip': ip,
        'url': url,
        'session': session,
        'session_data': {},
        'path': path,
        'method': method,
        'site_id': site_id,
        'referrer': referrer,
        'user_agent': user_agent,
        'response_status': status,
    }

    # CART

    if cart := request.session.get(cart_key):
        data['session_data'][cart_key] = cart
        loginfo(f'added cart slug to session[{session}] data')

    # CUSTOMER

    if cus := request.session.get(cus_key):
        data['session_data'][cus_key] = cus
        loginfo(f'added customer slug to session[{session}] data')

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
        data['session_data'].update({
            **_d,
            'username': request.user.username
        })

    if source:
        data.update({'source_id': source})

    cached_query = request.session.get(cached_query_key) or {}
    query = {**cached_query, **parse_qs(urlparse(url).query)}
    if query:
        request.session.update({cached_query_key: query})
        data['session_data'].update({'query': query})

    last = Hit.objects.filter(
        ip=ip, session=session, url=url, path=path,
        method=method, site_id=site_id, response_status=status,
        created__gt=timezone.now() - datetime.timedelta(minutes=1),
    )
    if last.exists() and (hit := last.order_by('-created').first()):
        # hit.count += 1
        hit.session_data = {**hit.session_data, **data}
        hit.save()
        loginfo(f'updated hit: {hit.slug}')
    else:
        hit = Hit.objects.create(**{
            **data,
            'parsed_data': parse_hit_data(url, referrer, user_agent, data.get('session_data', {})),
            'is_parsed': True,
            'is_bot': get_hit_is_bot(user_agent, path=path),
        })
        loginfo(f'new hit: {hit.slug}')

    return hit
