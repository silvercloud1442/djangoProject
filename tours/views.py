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

    def get_context_data(self, *object_list, **kwargs):
        context = super().get_context_data(**kwargs)
        description = context['tour'].description
        description = description.split('fechs')
        main_text, fechs = description[0], description[1]
        fechs = fechs.split('|')
        dop_context = {
            'main_text': main_text,
            'fechs' : fechs,

        }
        c_def = self.get_user_context(**dop_context)
        context = dict(list(context.items()) + list(c_def.items()))

        return context

class HotelView(DataMixin, DetailView):
    model = Hotels
    template_name = 'tours/hotel_details.html'
    context_object_name = 'hotel'
    slug_url_kwarg = 'hotel_slug'

    def get_context_data(self, *object_list, **kwargs):
        context = super().get_context_data(**kwargs)

        images = HotelImages.objects.filter(hotel=context['hotel'])
        images_urls = [image.image.url for image in images]

        rooms = Rooms.objects.filter(hotel=context['hotel'])
        # room_main =



        description = context['hotel'].description
        description = description.split('fechs')
        main_text, fechs = description[0], description[1]
        fechs = fechs.split('|')


        dop_context = {
            'main_text': main_text,
            'fechs' : fechs,
            'rat': range(int(context['hotel'].rating)),
            'images_urls': images_urls,
            'rooms': rooms

        }
        c_def = self.get_user_context(**dop_context)
        context = dict(list(context.items()) + list(c_def.items()))

        return context

def base(request):
    return render(request, 'tours/base.html')