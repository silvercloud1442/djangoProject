from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('base/', base, name='base'),
    path('tour_details', TourView.as_view(), name='details')
]