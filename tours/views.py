from django.shortcuts import render
from tours.utils import DataMixin
from django.views.generic import TemplateView, DetailView
from tours.models import *


class IndexPage(DataMixin, TemplateView):
    template_name = 'tours/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dop_context = {
            'section_type': 'main'
        }
        c_def = self.get_user_context(**dop_context)

        print(c_def)
        context = dict(list(context.items()) + list(c_def.items()))
        print(context)
        return context

class TourView(DataMixin, DetailView):
    model = Tours
    template_name = 'tours/tour_details.html'
    context_object_name = 'tour'
    slug_url_kwarg = 'tour_slug'

    def get_context_data(self, *, object_list, **kwargs):
        context = super().get_context_data(**kwargs)
        description = context['tour'].descritpion
        main_text, fechs = set(description.split('fechs'))
        fechs.split('|')
        dop_context = {
            'main_text': main_text,
            'fechs' : fechs

        }
        c_def = self.get_user_context(**dop_context)
        context = dict(list(context.items()) + list(c_def.items()))

        print(context)
        return context


def base(request):
    return render(request, 'tours/base.html')

# def index(requset):
#     return render(requset, 'tours/index.html')
#
# def tour_details(request):
#     return render(request, 'tours/tour_details.html')