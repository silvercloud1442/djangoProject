from django.shortcuts import render

def index(request):
    return render(request, 'tours/index.html')

def tours(requset):
    return render(requset, 'tours/tours.html')