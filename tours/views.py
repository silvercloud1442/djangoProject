from django.shortcuts import render
from tours.utils import DataMixin
from django.views.generic import TemplateView, DetailView


class IndexPage(DataMixin, TemplateView):
    template_name = 'tours/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dop_context = {
            'section_type': 'main'
        }
        c_def = self.get_user_context(**dop_context)

        context = dict(list(context.items()) + list(c_def.items()))

        return context

class TourView(DataMixin, TemplateView):
    template_name = 'tours/tour_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()

        context = dict(list(context.items()) + list(c_def.items()))

        return context


def base(request):
    return render(request, 'tours/base.html')

# def index(requset):
#     return render(requset, 'tours/index.html')
#
# def tour_details(request):
#     return render(request, 'tours/tour_details.html')