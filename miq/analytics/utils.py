
from ..core.utils import get_ip

from .models import Hit


def create_hit(request, response, /, source: str = None) -> Hit:
    if not request.session.session_key:
        try:
            request.session.save()
        except Exception:
            return

    path = request.build_absolute_uri() \
        or request.get_full_path_info() \
        or request.get_full_path() \
        or request.path_info \
        or request.path

    #
    source = source or request.session.get('source')
    # if not source and request.user.is_authenticated:
    #     source = request.user.slug

    data = {
        'site_id': '',
        'ip': get_ip(request),
        'path': path,
        'referrer': request.META.get('HTTP_REFERER'),
        'source': source,
        'method': request.method,
        'user_agent': request.META.get('HTTP_USER_AGENT'),
        'session': request.session.session_key,
        'session_data': request.session.get_decoded(),
        'response_status': response.status_code,
    }

    return Hit.objects.create(**data)
