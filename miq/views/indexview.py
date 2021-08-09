
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site

from miq.models import Index, Section

from .generic import ListView


class IndexView(ListView):
    object = None
    paginate_by = 50
    template_name = 'miq/page.html'

    def get_queryset(self):
        site = get_current_site(self.request)
        self.object = get_object_or_404(Index, site=site)
        return Section.objects.order_by('position')\
            .filter(source=self.object.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if (obj := self.object) is not None:
            context['object'] = obj
            context['title'] = obj.title

        return context
