from django.core.cache import cache
from django.db.models import Count

from .models import *

menu = [
    {'title': 'Main page', 'url': 'index'},
    {'title': 'Add tour', 'url': 'add_tour'},
    {'title': 'Contact', 'url': 'contact'},
    # {'title': 'Login', 'url': 'login'}
]
class DataMixin:
    paginate_by = 2
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('categories')
        if not cats:
            cats = Category.objects.annotate(Count('tour'))
            cache.set('categories', cats, 60)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['categories'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0

        return context