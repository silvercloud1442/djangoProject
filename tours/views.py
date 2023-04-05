from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView, ListView

from tours.forms import *
from tours.utils import DataMixin
from tours.models import *


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

class TourView(DataMixin, DetailView):
    model = Tours
    template_name = 'tours/tour_details.html'
    context_object_name = 'tour'
    slug_url_kwarg = 'tour_slug'

    def get_success_url(self):
        return reverse_lazy('index')

    def get_context_data(self, *object_list, **kwargs):
        context = super().get_context_data(**kwargs)

        hotel = Hotels.objects.get(name=context['tour'].hotel)

        images = TourImages.objects.filter(tour=context['tour'])
        images_urls = [image.image.url for image in images]

        description = context['tour'].description
        description = description.split('fechs')
        main_text, fechs = description[0], description[1]
        fechs = fechs.split('|')

        dop_context = {
            'hotel': hotel,
            'main_text': main_text,
            'fechs' : fechs,
            'images_urls': images_urls

        }
        c_def = self.get_user_context(**dop_context)
        context = dict(list(context.items()) + list(c_def.items()))

        return context

class HotelView(DataMixin, DetailView):
    model = Hotels
    template_name = 'tours/hotel_details.html'
    context_object_name = 'hotel'
    slug_url_kwarg = 'hotel_slug'

    def get_success_url(self):
        return reverse_lazy('index')

    def get_context_data(self, *object_list, **kwargs):
        context = super().get_context_data(**kwargs)

        images = HotelImages.objects.filter(hotel=context['hotel'])
        images_urls = [image.image.url for image in images]

        rooms = Rooms.objects.filter(hotel=context['hotel'])

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

class ToursView(DataMixin, ListView):
    paginate_by = 2
    model = Tours
    template_name = 'tours/tours.html'
    context_object_name = 'tours'

    def get_success_url(self):
        return reverse_lazy('index')

    def get_queryset(self):
        return Tours.objects.all().select_related('hotel').select_related('transit_in').select_related('transit_back')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ToursView, self).get_context_data(**kwargs)

        dop_context = {}

        c_def = self.get_user_context()
        context = dict(list(context.items()) + list(c_def.items()))

        return context

class LoginUserView(DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'tours/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data()
        dop_context = {
        }
        c_def = self.get_user_context(**dop_context)

        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_success_url(self):
        return reverse_lazy('index')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        client_form = RegisterClientForm(request.POST)
        if form.is_valid() and client_form.is_valid():
            user = form.save()
            client = client_form.save(commit=False)
            client.user = user
            client.save()

    else:
        form = RegisterUserForm()
        client_form = RegisterClientForm()
    context = {
        'user': form,
        'client': client_form
    }
    return render(request, 'tours/register.html', context=context)

def base(request):
    return render(request, 'tours/base.html')