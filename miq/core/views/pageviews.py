
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site

from ..models import Page, SiteSetting

from .generic import DetailView


class SettingPageViewMixin(DetailView):
    _object = None
    field = None  # type: str
    field_html = None  # type: str
    content = None  # type: str
    title = None  # type: str
    model = SiteSetting
    template_name = 'setting-page.django.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        field = f'{self.field_html}' or f'{self.field}_html'
        self.content = getattr(obj, f'{field}', getattr(obj, self.field, None))
        if not self.content:
            raise Http404('Content not found')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        data = {'title': f'{self.title}', 'content': self.content}

        # if self.field_html and (content := getattr(self.object, f'{self.field_html}')):
        #     data.update({'content': content, 'is_html': True})
        # elif self.field and (content := getattr(self.object, f'{self.field}')):
        #     data.update({'content': content})

        ctx.update(data)
        self.update_sharedData(ctx, data)

        return ctx

    def get_object(self):
        if self._object:
            return self._object

        self._object = get_object_or_404(SiteSetting, site=get_current_site(self.request))
        return self._object

    def get_template_names(self):
        return [self.template_name, 'core/setting-page.django.html']

    def __init__(self, **kwargs) -> None:
        if not isinstance(self.field, str):
            raise Exception('Field required and must be a string')
        super().__init__(**kwargs)


class AboutPage(SettingPageViewMixin):
    field = 'about'
    title = 'About us'


class PageView(DetailView):
    model = Page
    template_name = 'core/page.html'

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
