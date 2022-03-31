from django.views import generic


class SharedDataMixin(object):
    def update_sharedData(self, ctx, data):
        if 'sharedData' not in ctx.keys():
            ctx['sharedData'] = {}

        sharedData = ctx.get('sharedData')
        sharedData.update({**data})


class ViewMixin(SharedDataMixin):
    pass


class View(ViewMixin, generic.View):
    pass


class ListView(ViewMixin, generic.ListView):
    pass


class DetailView(ViewMixin, generic.DetailView):
    pass


class TemplateView(ViewMixin, generic.TemplateView):
    pass


class FormView(ViewMixin, generic.FormView):
    pass


class CreateView(ViewMixin, generic.CreateView):
    pass


class UpdateView(ViewMixin, generic.UpdateView):
    pass
