from ...core.views import generic
from .mixins import StaffViewMixin


class View(StaffViewMixin, generic.View):
    pass


class ListView(StaffViewMixin, generic.ListView):
    pass


class DetailView(StaffViewMixin, generic.DetailView):
    pass


class TemplateView(StaffViewMixin, generic.TemplateView):
    pass


class FormView(StaffViewMixin, generic.FormView):
    pass


class CreateView(StaffViewMixin, generic.CreateView):
    pass


class UpdateView(StaffViewMixin, generic.UpdateView):
    pass
