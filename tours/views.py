from django.shortcuts import render
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

def show_tour(request, tour_id):
    tour = Tour.objects.get(pk=tour_id)
    context = {
                'title': tour.name,
                'tour': tour
    }
    return render(request, 'tours/show_tour.html', context=context)