from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', cache_page(60)(TourHome.as_view()), name='index'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('add_tour/', AddTour.as_view(), name='add_tour'),
    path('tour_category/<slug:cat_slug>', TourCategory.as_view(), name='tour_category'),
    path('show_tour/<slug:tour_slug>/', ShowPost.as_view(), name='show_tour'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
]