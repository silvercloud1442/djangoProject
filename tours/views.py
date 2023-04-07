from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView, ListView, CreateView, FormView

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

class BookingView(DataMixin, FormView):
    form_class = BookingForm
    template_name = 'tours/booking.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tour = Tours.objects.get(slug=self.kwargs['tour_slug'])
        hotel = Hotels.objects.get(tours__slug=tour.slug)

        form = BookingForm()
        form.fields['room'].queryset = Rooms.objects.filter(hotel=hotel)
        if self.request.user.is_authenticated:
            print(self.request.user.id)
            client = Clients.objects.get(pk=self.request.user.id)
            form.fields['payment'].queryset = Payment.objects.filter(client=client)
        else:
            form.fields['payment'].queryset = Payment.objects.none()

        dop_context = {
            'hotel': hotel,
            'form': form
        }
        c_def = self.get_user_context(**dop_context)
        context = dict(list(context.items()) + list(c_def.items()))

        return context

class TourView(DataMixin, DetailView):
    model = Tours
    template_name = 'tours/tour_details.html'
    context_object_name = 'tour'
    slug_url_kwarg = 'tour_slug'

    def get_context_data(self, *object_list, **kwargs):
        context = super().get_context_data(**kwargs)

        hotel = Hotels.objects.get(name=context['tour'].hotel)

        # form = BookingForm()
        # form.fields['room'].queryset = Rooms.objects.filter(hotel=hotel)
        # if self.request.user.is_authenticated:
        #     client = Clients.objects.get(user=self.request.user.id)
        #     form.fields['payment'].queryset = Payment.objects.filter(client=client)
        # else:
        #     form.fields['payment'].queryset = Payment.objects.none()

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
            'images_urls': images_urls,
            # 'form': form

        }
        c_def = self.get_user_context(**dop_context)
        context = dict(list(context.items()) + list(c_def.items()))

        return context
    # def post(self, request, *args, **kwargs):
    #     form = BookingForm(request.POST)
    #     print(form)
    #     if form.is_valid():
    #         booking = form.save(commit=False)
    #         booking.client = self.client
    #         booking.payment_status = 'Оплачен'
    #         booking.tour = self.context['tour']
    #         booking.save()
    #         return HttpResponse('good')
    #     return HttpResponse('bad')

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

def logout_user(request):
    logout(request)
    return redirect('index')

def base(request):
    return render(request, 'tours/base.html')