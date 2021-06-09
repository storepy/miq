
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site

from miq.models import Page


from .generic import DetailView


class PageView(DetailView):
    model = Page
    template_name = 'miq/page.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(
            Page.objects.published(),
            slug=self.kwargs.get('slug'),
            site=get_current_site(self.request)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        instance = context.get('object')
        if instance:
            context['title'] = instance.title

        return context
