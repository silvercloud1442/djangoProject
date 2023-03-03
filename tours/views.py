from django.shortcuts import render

def index(request):
    context = {
                'title': 'INDEX PAGE'
    }
    return render(request, 'tours/index.html', context=context)

def tours(requset):
    tours = [
        {'name': 'name 1', 'description': 'description 1', 'price': 100},
        {'name': 'name 2', 'description': 'description 2', 'price': 200},
        {'name': 'name 3', 'description': 'description 3', 'price': 300},
             ]
    context = {
                'title': 'TOURS PAGE',
                'tours': tours
    }
    return render(requset, 'tours/tours.html', context=context)