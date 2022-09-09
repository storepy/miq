import os
import subprocess
from bs4 import BeautifulSoup

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.management.base import BaseCommand


output_path = os.path.join(settings.TEMPLATES_DIR, 'base-react.html')


class Command(BaseCommand):
    help = 'Collect React index.html and static files'

    def handle(self, *args, **kwargs):
        # First build
        if (site := Site.objects.first()) and not hasattr(site, 'settings'):
            site.save()

        client_dir = getattr(settings, 'CLIENT_DIR', 'client')
        if not os.path.isdir(client_dir):
            self.stdout.write(self.style.ERROR('No client directory found'))
            raise Exception('No client directory')

        self.stdout.write('Building client app ...')
        subprocess.run(['yarn', 'build'], cwd=client_dir, check=True)

        if not os.path.isdir(settings.BUILD_DIR):
            raise Exception('No build directory')

        index_path = os.path.join(settings.BUILD_DIR, 'index.html')
        if not os.path.exists(index_path):
            # print or raise error
            self.stdout.write(self.style.ERROR('No index path'))
            raise Exception('No index path')

        self.stdout.write('Collecting static files ...')
        call_command(
            'collectstatic', interactive=False,
            clear=True, verbosity=0
        )

        #

        html = open(index_path).read()
        soup = BeautifulSoup(html, 'html.parser')

        soup.title.replace_with("{% block head %}{% endblock head %}")

        root = soup.find("div", id="root")
        root.insert_before(
            "{% block pre_react %}{% endblock pre_react %}{% block react %}")
        root.insert_after(
            "{% endblock react %}{% block post_react %}{% endblock post_react %}")

        style = soup.new_tag('style', type="text/css", id='page-css')
        style.string = "{% block css %}{% endblock css %}"
        soup.head.insert(len(soup.head.contents), style)

        style = soup.find("style", id="page-css")

        style.insert_before("{% block css_links %}{% endblock css_links %}")

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))

        self.stdout.write(
            self.style.SUCCESS(f'Exported file: {output_path}')
        )
