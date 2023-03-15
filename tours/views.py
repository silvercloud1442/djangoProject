from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from tours.forms import AddTourForm
from tours.models import *



menu = [
    {'title': 'Main page', 'url': 'index'},
    {'title': 'Add tour', 'url': 'add_tour'},
    # {'title': 'Tours', 'url' : 'tours'}
]

class TourHome(ListView):
    model = Tour
    template_name = 'tours/index.html'
    context_object_name = 'tours'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Main page'
        context['categories'] = Category.objects.all()
        context['cat_selected'] = 0
        return context
    def get_queryset(self):
        return Tour.objects.all()

# def index(request):
#     context = {
#         'title': 'INDEX PAGE',
#         'menu' : menu
#     }
#     return render(request, 'tours/index.html', context=context)


def tour_category(requset, cat_slug):
    context = {
        'title': 'TOURS PAGE',
        'tours': Tour.objects.fillter(cat_slug='cat_slug'),
        'categories': Category.objects.all(),
        'cat_selected': cat_slug,
        'menu' : menu,

    }
    return render(requset, 'tours/tours.html', context=context)


@csrf_exempt
def add_tour(request):
    if request.method == 'POST':
        form = AddTourForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AddTourForm()
    context = {
        'title': 'ADD TOUR',
        'form': form,
        'categories': Category.objects.all(),
        'cat_selected': 0,
        'menu' : menu,
    }
    return render(request, 'tours/add_tour.html', context=context)


def show_tour(request, tour_slug):
    tour = Tour.objects.get(slug=tour_slug)
    context = {
        'title': tour.name,
        'tour': tour,
        'categories': Category.objects.all(),
        'cat_selected': 0,
        'menu': menu,
    }
    return render(request, 'tours/show_tour.html', context=context)
