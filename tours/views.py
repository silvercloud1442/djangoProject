from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import AddTourForm, RegisterUserForm, LoginUserForm
from .models import *
from .utils import *


menu = [
    {'title': 'Main page', 'url': 'index'},
    {'title': 'Add tour', 'url': 'add_tour'},
]

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'tours/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dop_context = {
            'title': 'Register'
        }
        c_def = self.get_user_context(**dop_context)
        context = dict(list(context.items()) + list(c_def.items()))

        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect('index')




class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'tours/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dop_context = {
            'title': 'Login'
        }
        c_def = self.get_user_context(**dop_context)
        context = dict(list(context.items()) + list(c_def.items()))

        return context

    def get_success_url(self):
        return reverse_lazy('index')

class TourHome(DataMixin, ListView):
    paginate_by = 2
    model = Tour
    template_name = 'tours/index.html'
    context_object_name = 'tours'

    def get_queryset(self):

        return Tour.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        dop_context = {
                'title': 'Main page'
        }
        c_def = self.get_user_context(**dop_context)
        context = dict(list(context.items()) + list(c_def.items()))

        return context

class TourCategory(DataMixin, ListView):
    paginate_by = 2
    model = Tour
    template_name = 'tours/tours.html'
    context_object_name = 'tours'
    allow_empty = False

    def get_queryset(self):
        return Tour.objects.filter(category__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        dop_context = {
            'title' : 'Category - ' + str(context['tours'][0].category),
            'cat_selected' : context['tours'][0].category.slug
        }
        c_def = self.get_user_context(**dop_context)
        context = dict(list(context.items()) + list(c_def.items()))

        return context

class ShowPost(DataMixin, DetailView):
    model = Tour
    template_name = 'tours/show_tour.html'
    context_object_name = 'tour'
    slug_url_kwarg = 'tour_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        dop_context = {
            'title' : context['tour'],
            'cat_selected': context['tour'].category.slug
        }
        c_def = self.get_user_context(**dop_context)
        context = dict(list(context.items()) + list(c_def.items()))

        return context

class AddTour(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddTourForm
    template_name = 'tours/add_tour.html'
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dop_context = {
            'title': 'Add tour'
        }
        c_def = self.get_user_context(**dop_context)
        context = dict(list(context.items()) + list(c_def.items()))

        return context

def logout_user(request):
    logout(request)
    return redirect('index')


# def login(request):
#     context = {
#         'title': 'login',
#         'menu' : menu
#     }
#     return render(request, 'tours/login.html', context=context)


# def tour_category(requset, cat_slug):
#     category = Category.objects.get(slug=cat_slug)
#     tours = Tour.objects.filter(category=category)
#     context = {
#         'title': 'TOURS PAGE',
#         'tours': tours,
#         'categories': Category.objects.all(),
#         'cat_selected': cat_slug,
#         'menu' : menu,
#
#     }
#     return render(requset, 'tours/tours.html', context=context)


# @csrf_exempt
# def add_tour(request):
#     if request.method == 'POST':
#         form = AddTourForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         form = AddTourForm()
#     context = {
#         'title': 'ADD TOUR',
#         'form': form,
#         'categories': Category.objects.all(),
#         'cat_selected': None,
#         'menu' : menu,
#     }
#     return render(request, 'tours/add_tour.html', context=context)


# def show_tour(request, tour_slug):
#     tour = Tour.objects.get(slug=tour_slug)
#     context = {
#         'title': tour.name,
#         'tour': tour,
#         'categories': Category.objects.all(),
#         'cat_selected': 0,
#         'menu': menu,
#     }
#     return render(request, 'tours/show_tour.html', context=context)
