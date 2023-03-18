import time
import random

from .request import get_query_params_from_url, get_request_url


def get_fb_params(request, response=None):
    _fbp = get_fbp(request)
    _fbc = get_fbc(request, response=response)
    return _fbp, _fbc


def get_fbp(request):
    _fbp = request.COOKIES.get('_fbp')
    if not _fbp:
        return None
    return _fbp


def get_random_fbp():
    return f'fb.1.{int(time.time() * 1000)}.{random.randint(10000000000, 99999999999)}'


def get_fbc(request, response=None):
    _fbc = request.COOKIES.get('_fbc')
    if not _fbc:
        params = get_query_params_from_url(get_request_url(request))
        if fbclid := params.get('fbclid'):
            if isinstance(fbclid, list):
                fbclid = fbclid[0]
            _fbc = f'fb.1.{int(time.time() * 1000)}.{fbclid}'

            if response:
                response.set_cookie('_fbc', _fbc)

    if not _fbc:
        return None

    return _fbc
