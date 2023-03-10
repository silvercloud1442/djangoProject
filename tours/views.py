from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from tours.forms import AddTourForm
from tours.models import *


def index(request):
    context = {
        'title': 'INDEX PAGE'
    }
    return render(request, 'tours/index.html', context=context)


def tours(requset):
    context = {
        'title': 'TOURS PAGE',
        'tours': Tour.objects.all(),
        'category': Category.objects.all()
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
        'form': form
    }
    return render(request, 'tours/add_tour.html', context=context)


def show_tour(request, tour_slug):
    tour = Tour.objects.get(slug=tour_slug)
    context = {
        'title': tour.name,
        'tour': tour
    }
    return render(request, 'tours/show_tour.html', context=context)
