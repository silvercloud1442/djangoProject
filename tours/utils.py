from .models import *

menu = [
    {'title': 'Main page', 'url': 'index'},
    {'title': 'Add tour', 'url': 'add_tour'},
]
class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.all()
        context['menu'] = menu
        context['categories'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context