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