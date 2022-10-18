# from pprint import pprint

import logging

from ..core.utils import get_ip

from .PATHS import PATHS
from .models import Attempt

# whatsapp

logger = logging.getLogger(__name__)
loginfo = logger.info
logerr = logger.error

ips = set()
paths = set(PATHS)


def add_ip(ip):
    """
    Add ip to cache. Max size: 1000
    """

    if ip in ips:
        return

    if len(ips) > 1000:
        ips.pop()
    ips.add(ip)


def is_threat(request) -> bool:
    """
    Detect if request is threat based on path or ip
    """

    _ = False

    if request.path.lower() in paths:
        _ = True

    ip = get_ip(request)
    if _ is False and (ip in ips or Attempt.objects.filter(ip=ip).exists()):
        _ = True

    if _:
        add_ip(ip)
        logger.warning(f'Threat detected: [{ip}]')

    return _
