
from urllib.parse import urlparse, parse_qs
# TODO: replace urlparse with urlsplit


def get_query_params_from_url(url):
    return parse_qs(urlparse(url).query)


def get_request_url(request):
    return request.build_absolute_uri() \
        or request.get_full_path_info() \
        or request.get_full_path() \
        or request.path_info \
        or request.path
