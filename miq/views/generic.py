from django.views import generic


class SharedDataMixin(object):
    def update_sharedData(self, ctx, data):
        if 'sharedData' not in ctx.keys():
            ctx['sharedData'] = {}

        sharedData = ctx.get('sharedData')
        sharedData.update({**data})


class ViewMixin(SharedDataMixin):
    pass


class ListView(ViewMixin, generic.ListView):
    pass


class DetailView(ViewMixin, generic.DetailView):
    pass


class TemplateView(ViewMixin, generic.TemplateView):
    pass
