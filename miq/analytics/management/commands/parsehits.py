
from django.core.management.base import BaseCommand

from ...utils import parse_hits


class Command(BaseCommand):
    help = 'Parse Hits'

    def handle(self, *args, **kwargs):
        parse_hits()
