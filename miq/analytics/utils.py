import logging
import datetime
from urllib.parse import urlparse, parse_qs

from django.utils import timezone

from ..core.utils import get_ip

from .models import Campaign, Hit, SearchTerm

logger = logging.getLogger(__name__)
loginfo = logger.info
logerr = logger.error

exclude = [
    '/admin/', 'staff',
    '/media/', '/favicon.ico',
]

# SESSION APP KEYS
cus_key = '_cus'
cart_key = '_cart'
cached_query_key = '_cqk'


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
    obj = ctx.get('object')

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
        hit = Hit.objects.create(**data)
        loginfo(f'new hit: {hit.slug}')

    return hit

    # for key in query.keys():
    #     if key == 'q':
    #         continue

    #     for value in query.get(key, []):
    #         Campaign.objects.get_or_create(key=key.lower(), value=value.lower(), ip=ip)

    # for q in query.get('q', []):
    #     if not q:
    #         continue

    #     term, new = SearchTerm.objects.get_or_create(session=session, value=q)
    #     if not new:
    #         term.count += 1
    #         term.save()
