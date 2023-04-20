from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView, ListView, CreateView, FormView
from django.contrib import messages

from tours.forms import *
from tours.mixin import DataMixin
from tours.models import *


class IndexPage(DataMixin, TemplateView):
    template_name = 'tours/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dop_context = {
            'section_type': 'main',
            'title': 'Lors du dernier voyage'
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
            'title': context['tour'].name

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
            'rooms': rooms,
            'title': context['hotel'].name
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

        dop_context = {
            'title': 'Доступные туры'
        }

        c_def = self.get_user_context(**dop_context)
        context = dict(list(context.items()) + list(c_def.items()))

        return context

class LoginUserView(DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'tours/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data()
        dop_context = {
            'section_type': 'log_sec',
            'title': 'Авторизация'
        }
        c_def = self.get_user_context(**dop_context)

        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Неверный логин или пароль')
        return super().form_invalid(form)
    def get_success_url(self):
        return reverse_lazy('index')
    
class BookingView(DataMixin, CreateView):
    form_class = BookingForm
    template_name = 'tours/booking.html'
    success_url = reverse_lazy('index')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(BookingView, self).get_form_kwargs()

        tour = Tours.objects.get(slug=self.kwargs['tour_slug'])
        hotel = Hotels.objects.get(tours__slug=tour.slug)

        kwargs['hotel'] = hotel
        kwargs['tour'] = tour
        user = User.objects.get(pk=self.request.user.id)
        kwargs['client'] = Clients.objects.get(user=user)

        if self.request.user.is_authenticated:
            client = Clients.objects.get(pk=self.request.user.id)
            kwargs['payment'] = Payment.objects.filter(client=client)
        else:
            kwargs['payment'] = Payment.objects.none()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tour = Tours.objects.get(slug=self.kwargs['tour_slug'])
        hotel = Hotels.objects.get(tours__slug=tour.slug)

        dop_context = {
            'hotel': hotel,
            'section_type': 'book_sec',
            'title': f'Оформление : {tour.name}'
        }

        c_def = self.get_user_context(**dop_context)
        context = dict(list(context.items()) + list(c_def.items()))

        return context

    def from_valid(self, form):
        form.save()
        return redirect('index')
    
class ProfileView(DataMixin, CreateView):
    form_class = PaymentForm
    template_name = 'tours/profile.html'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        if self.request.user.id != self.kwargs['user_id']:
            return redirect('index')
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ProfileView, self).get_form_kwargs()
        user = User.objects.get(pk=self.request.user.id)
        kwargs['client'] = Clients.objects.get(user=user)

        return kwargs

    def get_queryset(self):
        return Booking.objects.filter(client__user_id=self.request.user.id).\
                                    select_related('tour').\
                                    select_related('transit').\
                                    select_related('payment')

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        tours = Tours.objects.all()
        transit = Transit.objects.all()
        user = User.objects.get(pk=self.kwargs['user_id'])

        client = get_object_or_404(Clients, user=user)
        payments = Payment.objects.filter(client=client)
        bookings = Booking.objects.filter(client=client)

        context_bookings = []
        for book in bookings:
            tour = tours.get(id=book.tour.id)
            added = []
            added.append(tour)
            added.append(book.adults_count + book.kids_count)
            added.append(book.payment)
            added.append(book.total_price)
            added.append(transit.get(id=tour.transit_in.id))
            added.append(transit.get(id=tour.transit_back.id))
            context_bookings.append(added)
        dop_context = {
            'bookings': context_bookings,
            'payments': payments,
            'section_type': 'profile_sec',
            'title': 'Мой профиль'
        }
        c_def = self.get_user_context(**dop_context)
        context = dict(list(context.items()) + list(c_def.items()))

        return context

    def form_valid(self, form):
        form.save()
        user = User.objects.get(pk=self.kwargs['user_id'])
        return redirect('profile', user_id=user.id)


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
        'client': client_form,
        'section_type': 'reg_sec',
        'title': 'Регистрация'
    }
    print(context)
    return render(request, 'tours/register.html', context=context)

# def profile_view(request):
#     return render(request, 'tours/profile.html')

def logout_user(request):
    logout(request)
    return redirect('index')

def base(request):
    context = {
        'title': 'База кормит'
    }
    return render(request, 'tours/base.html', context=context)