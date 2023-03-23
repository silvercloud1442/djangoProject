from django.shortcuts import render

def base(request):
    return render(request, 'tours/base.html')

def index(requset):
    return render(requset, 'tours/index.html')