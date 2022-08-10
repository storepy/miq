
from urllib.parse import urlparse, parse_qs

from ..core.utils import get_ip

from .models import Campaign, Hit, SearchTerm

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
        return
    for match in exclude:
        if match in request.path:
            return

    if not request.session.session_key:
        try:
            request.session.save()
        except Exception:
            return

    url = request.build_absolute_uri() \
        or request.get_full_path_info() \
        or request.get_full_path() \
        or request.path_info \
        or request.path

    #
    ip = get_ip(request)
    session = request.session.session_key
    data = {
        'ip': ip,
        'url': url,
        'session': session,
        'session_data': {},
        'path': request.path,
        'method': request.method,
        'site_id': request.site.id,
        'referrer': request.META.get('HTTP_REFERER'),
        'user_agent': request.META.get('HTTP_USER_AGENT'),
        'response_status': response.status_code,
    }

    # CART

    if cart := request.session.get(cart_key):
        data['session_data'][cart_key] = cart

    # CUSTOMER

    if cus := request.session.get(cus_key):
        data['session_data'][cus_key] = cus

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

    for key in query.keys():
        if key == 'q':
            continue

        for value in query.get(key, []):
            Campaign.objects.get_or_create(key=key.lower(), value=value.lower(), ip=ip)

    for q in query.get('q', []):
        if not q:
            continue

        term, new = SearchTerm.objects.get_or_create(session=session, value=q)
        if not new:
            term.count += 1
            term.save()

    return Hit.objects.create(**data)
